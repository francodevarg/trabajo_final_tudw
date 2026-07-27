from django.contrib.auth.models import Group, User

from authapp.models import Profile
from patients.models import PatientUser
from rest_framework.exceptions import ValidationError


class PatientService:
    @staticmethod
    def get_or_create(email: str):
        INVALID_GROUPS = ["DOCTOR", "ADMIN"]

        if User.objects.filter(
            email=email,
            groups__name__in=INVALID_GROUPS,
        ).exists():
            raise ValidationError(
                {
                    "email": "This email belongs to a doctor or administrator account."
                }
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

            Profile.objects.create(
                user=user,
                phone_number="",
                date_of_birth=None,
                address="",
            )

            patient_group = Group.objects.get(name="PATIENT")
            user.groups.add(patient_group)

        return user, created

    @staticmethod
    def link_patient_to_user(user, patient, role="self", is_primary=False):
        link, created = PatientUser.objects.get_or_create(
            user=user,
            patient=patient,
            defaults={
                "role": role,
                "is_primary": is_primary,
            },
        )
        return link, created
