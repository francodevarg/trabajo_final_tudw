from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authapp.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Usamos el email como username
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, phone_number="", date_of_birth=None, address="")
        
        
        # Asignar grupo "PATIENT" por regla de negocio
        group, created = Group.objects.get_or_create(name='PATIENT')
        user.groups.add(group)
        return user
    

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Un solo grupo
        group = user.groups.first()
        token['role'] = group.name if group else None

        # Permisos efectivos (incluye los del grupo)
        token['permissions'] = list(user.get_all_permissions())

        return token