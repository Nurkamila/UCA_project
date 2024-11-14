from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import StudentProfile, Grade, School, Notification
from account.models import User
from .serializers import StudentProfileSerializer, GradeSerializer, NotificationSerializer
from .my_permissions import IsDirector


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Доступ только для аутентифицированных пользователей

    def perform_create(self, serializer):
        # Установим текущего пользователя как учителя профиля ученика
        serializer.save(teacher=self.request.user)

    def get_queryset(self):
        # Показываем только профили, принадлежащие учителю
        user = self.request.user
        return StudentProfile.objects.filter(teacher=user)
    

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтруем оценки по профилям, принадлежащим текущему учителю
        user = self.request.user
        return Grade.objects.filter(student_profile__teacher=user)

    def perform_create(self, serializer):
        serializer.save()

class StudentTransferViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAdminUser]  # Ограничиваем доступ только для директоров
    permission_classes = [IsDirector]

    @action(detail=True, methods=['post'])
    def transfer_student(self, request, pk=None):
        try:
            student_profile = StudentProfile.objects.get(pk=pk)
            new_school_id = request.data.get('new_school')
            new_school = School.objects.get(pk=new_school_id)

            # Назначаем новую школу в поле `pending_transfer_school`
            student_profile.pending_transfer_school = new_school
            student_profile.save()

            # Находим директора новой школы
            new_school_director = User.objects.get(school=new_school, is_director=True)

            # Создаем уведомление
            Notification.objects.create(
                recipient=new_school_director,
                student_profile=student_profile,
                school=new_school,
                message=f"Transfer request for {student_profile.first_name} {student_profile.last_name} to your school."
            )

            return Response({'message': 'Transfer initiated. Access for current staff will be revoked.'}, status=status.HTTP_200_OK)
        
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except School.DoesNotExist:
            return Response({'error': 'New school not found'}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=True, methods=['post'])
    def complete_transfer(self, request, pk=None):
        try:
            student_profile = StudentProfile.objects.get(pk=pk)

            if not student_profile.pending_transfer_school:
                return Response({'error': 'No pending transfer for this student'}, status=status.HTTP_400_BAD_REQUEST)

            # Завершаем перевод: меняем основную школу и удаляем временную
            student_profile.school = student_profile.pending_transfer_school
            student_profile.pending_transfer_school = None
            student_profile.save()

            # Логика сброса доступа у предыдущих учителей и назначения новому директору
            # (здесь может потребоваться дополнительная настройка прав доступа)
            
            return Response({'message': 'Transfer completed. Access updated for the new school staff.'}, status=status.HTTP_200_OK)

        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Получаем уведомления только для текущего директора
        return Notification.objects.filter(recipient=self.request.user, is_read=False).order_by('-created_at')