from rest_framework import serializers
from .models import StudentProfile, Grade, Subject, Notification
from account.models import School, Region

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject_name')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('first_name', 'last_name', 'middle_name', 'photo', 'age')  # Убедимся, что учитель устанавливается автоматически

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['teacher'] = user  # Получаем текущего пользователя из запроса
        validated_data['school'] = School.objects.get(name=user.school.name)
        validated_data['region'] = Region.objects.get(name=user.region.name)
        return super().create(validated_data)


class GradeSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(queryset=Subject.objects.all(), slug_field='subject_name')
    
    class Meta:
        model = Grade
        fields = ('student_profile', 'subject', 'grade', 'school_year', 'class_number')



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('message', 'created_at', 'is_read')

    # def validate(self, attrs):
    #     # Дополнительная валидация при необходимости
    #     return attrs
