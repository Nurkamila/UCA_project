from rest_framework import serializers
from .models import User, Region, School

class RegistrationSerializer(serializers.ModelSerializer):
    school_code = serializers.CharField(max_length = 100, required = True)

    region = serializers.SlugRelatedField(queryset = Region.objects.all(), slug_field = 'name')
    school = serializers.SlugRelatedField(queryset = School.objects.all(), slug_field = 'name')

    class Meta:
        model = User
        fields = ('email', 'password', 'region', 'school', 'school_code')
        
    def validate(self, attrs):
        region = attrs.get('region')
        school = attrs.get('school')
        school_code = attrs.pop('school_code')

        # print('ATTRS -> ', attrs)

        if school.region != region:
            raise serializers.ValidationError('Selected school does not belong to the selected region.')
        
        if school.code != school_code:
            # print('SCHOOL CODE FROM DB -> ', school.code)
            # print('SCHOOL CODE FROM THE REQUEST -> ', school_code)
            raise serializers.ValidationError('Wrong school code')

        return attrs
    
    def create(self, validated_data):
        # print('VALID DATA -> ', validated_data)

        user = User.objects.create_user(

            email=validated_data['email'],
            password=validated_data['password'],
            region=validated_data['region'],
            school=validated_data['school'],
            role = 'teacher',
            
        )

        return user
    

# ValueError: Cannot assign "[<School: Средняя школа №8 им. Буйлаш у. А. -> (Нарын), code->(903861032100)>]": "User.school" must be a "School" instance.
# ATTRS ->  {'email': 'user@example.com', 'password': 'Lalisa18$', 'region': <Region: Нарын>, 'school': <School: Средняя школа №8 им. Буйлаш у. А. -> (Нарын), code->(903861032100)>, 'school_code': '903861032100'}

# VALID DATA ->  {'email': 'user@example.com', 'password': 'Lalisa18$', 'region': <Region: Нарын>, 'school': <School: Средняя школа №8 им. Буйлаш у. А. -> (Нарын), code->(903861032100)>, 'school_code': '903861032100'}