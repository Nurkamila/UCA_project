from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import action
from .serializers import RegistrationSerializer, UserSerializer
from student_prof.my_permissions import IsDirector
from .models import User
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListTeachers(generics.ListAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(school=user.school, role='teacher')