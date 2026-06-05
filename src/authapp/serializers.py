from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authapp.models import Profile
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    group = serializers.CharField(write_only=True)

    ALLOWED_REGISTER_GROUPS = [
        'PATIENT',
        'DOCTOR',
        'ADMIN'
    ]

    class Meta:
        model = User

        fields = [
            'email',
            'group'
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                'Email already exists.'
            )

        return value

    def validate_group(self, value):

        if value not in self.ALLOWED_REGISTER_GROUPS:

            raise serializers.ValidationError(
                'Invalid group.'
            )

        if not Group.objects.filter(name=value).exists():

            raise serializers.ValidationError(
                'Group does not exist.'
            )

        return value

    def create(self, validated_data):

        group_name = validated_data.pop('group')

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email']
        )

        user.set_unusable_password()

        user.save()

        Profile.objects.create(
            user=user,
            phone_number='',
            date_of_birth=None,
            address=''
        )

        group = Group.objects.get(name=group_name)

        user.groups.add(group)

        return user

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Un solo grupo
        group = user.groups.first()
        token['group'] = group.name if group else None

        # Permisos efectivos (incluye los del grupo)
        token['permissions'] = list(user.get_all_permissions())

        return token
    

class RequestOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)