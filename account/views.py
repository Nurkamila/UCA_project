from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from .models import User
from .serializers import RegistrationSerializer
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