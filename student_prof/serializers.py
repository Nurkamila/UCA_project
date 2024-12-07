from rest_framework import serializers, response
from .models import StudentProfile, Grade, Subject
from account.models import School, Region

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject_name')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('first_name', 'last_name', 'middle_name', 'photo', 'grades')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['teacher'] = user  
        validated_data['school'] = School.objects.get(name=user.school.name)
        validated_data['region'] = Region.objects.get(name=user.region.name)
        return super().create(validated_data)
    
    def to_representation(self, instance: StudentProfile):
        rep = super().to_representation(instance)
        grades = Grade.objects.filter(student_profile=instance)

        grades_data = []
        for grade in grades:
            grades_data.append({
                "school_name": grade.student_profile.school.name,
                "class_name": grade.class_number,
                "subject": grade.subject.subject_name,
                "quarter_1": grade.quarter_1,
                "quarter_2": grade.quarter_2,
                "quarter_3": grade.quarter_3,
                "quarter_4": grade.quarter_4,
            })

        rep['grades'] = grades_data

        return rep



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def update(self, instance, validated_data):
        
        for field, value in validated_data.items():
            if value is not None:
                setattr(instance, field, value)

        quarters = [instance.quarter_1, instance.quarter_2, instance.quarter_3, instance.quarter_4]
        valid_quarters = [q for q in quarters if q is not None]
        if valid_quarters:
            instance.year_average = sum(valid_quarters) / len(valid_quarters)

        instance.save()
        return instance


class StudentTransferSerializer(serializers.Serializer):
    new_school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())