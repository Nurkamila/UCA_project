from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import StudentProfile, Grade
from account.models import User
from .serializers import StudentProfileSerializer, GradeSerializer, StudentTransferSerializer
from .my_permissions import IsDirector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('first_name', 'last_name')

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'director':
            return StudentProfile.objects.filter(school=user.school)
        else:
            return StudentProfile.objects.filter(teacher=user)
    
        
    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated, IsDirector])
    def assign_teacher(self, request, pk=None):

        try:
            student_profile = StudentProfile.objects.get(pk=pk)
            director = request.user
            teacher_id = request.data.get('teacher_id')
            teacher = User.objects.get(pk=teacher_id, role='teacher', school=director.school)

            
            student_profile.teacher = teacher
            student_profile.save()

            return Response({
                'message': f"Teacher {teacher.first_name} {teacher.last_name} assigned to student {student_profile.first_name} {student_profile.last_name}."
            }, status=status.HTTP_200_OK)

        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found in your school or invalid role'}, status=status.HTTP_404_NOT_FOUND)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Grade.objects.filter(student_profile__teacher=user)
        elif user.role == 'director':
            return Grade.objects.filter(student_profile__school=user.school)
        return Grade.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        student_profile = serializer.validated_data['student_profile']
        if student_profile.teacher != user:
            raise serializers.ValidationError("You can only modify grades for your students.")
        serializer.save()


class StudentTransferViewSet(viewsets.ViewSet):
    permission_classes = [IsDirector]

    @swagger_auto_schema(request_body=StudentTransferSerializer())
    @action(detail=True, methods=['post'])
    def transfer_student(self, request, pk=None):

        try:
            student_profile = StudentProfile.objects.get(pk=pk)

            if student_profile.school != request.user.school:
                return Response({'error': 'You are not authorized to transfer this student'}, status=status.HTTP_403_FORBIDDEN)

        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_school = serializer.validated_data['new_school']

        student_profile.pending_transfer_school = new_school
        student_profile.save()

        return Response({'message': 'Transfer initiated. Access for current staff will be revoked.'}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def complete_transfer(self, request, pk=None):
        try:
            student_profile = StudentProfile.objects.get(pk=pk)

            if not student_profile.pending_transfer_school:
                return Response({'error': 'No pending transfer for this student'}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.school != student_profile.pending_transfer_school:
                return Response({'error': 'You are not authorized to complete this transfer'}, status=status.HTTP_403_FORBIDDEN)

            new_school = student_profile.pending_transfer_school
            student_profile.school = new_school
            student_profile.region = new_school.region  
            student_profile.pending_transfer_school = None
            student_profile.teacher = None  
            student_profile.save()

            return Response({'message': 'Transfer completed. Access updated for the new school staff.'}, status=status.HTTP_200_OK)

        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)