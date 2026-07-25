from django.contrib.auth.models import Group, User

from authapp.models import Profile


class PatientService:

    @staticmethod
    def get_or_create(email: str):
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