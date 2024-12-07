from django.db import models
from account.models import User, Region, School

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.subject_name

class StudentProfile(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='students_prof', null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', null=False, blank=False)
    pending_transfer_school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="pending_transfers")
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Grade(models.Model):
    GRADE_CHOICES = (
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
    )

    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    age = models.IntegerField()
    school_year = models.CharField(max_length=10)
    class_number = models.CharField(max_length=10)
    quarter_1 = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)  
    quarter_2 = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True) 
    quarter_3 = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True) 
    quarter_4 = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True) 
    year_average = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('student_profile', 'subject', 'school_year', 'class_number')

    def __str__(self):
        return f"{self.student_profile.first_name} - {self.subject.subject_name} Year {self.school_year}, Class {self.class_number}"