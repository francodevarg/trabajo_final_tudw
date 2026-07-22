from __future__ import annotations

from datetime import date
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from patients.models import Patient

User = get_user_model()


class PatientUserSerializer(serializers.Serializer):
    """Writable nested serializer for User email updates."""

    email = serializers.EmailField()


class PatientListSerializer(serializers.ModelSerializer):
    """ Lightweight serializer for list views. """

    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    last_appointment = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = (
            "id",
            "full_name",
            "first_name",
            "last_name",
            "dni",
            "sex",
            "age",
            "last_appointment",
            "user",
        )

    def get_full_name(self, obj: Patient) -> str:
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj: Patient) -> int | None:
        if obj.date_of_birth is None:
            return None
        today = date.today()
        return (
            today.year
            - obj.date_of_birth.year
            - (
                (today.month, today.day)
                < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        )

    def get_last_appointment(self, obj: Patient) -> dict[str, Any] | None:
        last_date = getattr(obj, "last_appointment_date", None)
        if last_date is None:
            return None
        last_status = getattr(obj, "last_appointment_status", None)
        return {
            "date": last_date,
            "status": last_status,
        }

    def get_user(self, obj: Patient) -> dict[str, str] | None:
        if obj.user is None:
            return None
        return {"email": obj.user.email}


class PatientDetailSerializer(serializers.ModelSerializer):
    """ Full serializer for retrieve / update views.

        Accepts ``{"user": {"email": "..."}}`` on write (PATCH/PUT).
        Returns ``{"email": "..."}`` on read.
    """

    age = serializers.SerializerMethodField()
    user = PatientUserSerializer(required=False)

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "dni",
            "sex",
            "age",
            "user",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance: Patient) -> dict[str, Any]:
        data = super().to_representation(instance)
        if instance.user is not None:
            data["user"] = {"email": instance.user.email}
        else:
            data["user"] = None
        return data

    def get_age(self, obj: Patient) -> int | None:
        if obj.date_of_birth is None:
            return None
        today = date.today()
        return (
            today.year
            - obj.date_of_birth.year
            - (
                (today.month, today.day)
                < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user_data = attrs.get("user")
        if user_data and self.instance and self.instance.user:
            new_email = user_data["email"]
            if new_email != self.instance.user.email:
                if User.objects.filter(email=new_email).exclude(pk=self.instance.user.pk).exists():
                    raise serializers.ValidationError(
                        {"user": {"email": "This email is already registered."}}
                    )
        return attrs

    def update(self, instance: Patient, validated_data: dict[str, Any]) -> Patient:
        user_data = validated_data.pop("user", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data is not None and instance.user is not None:
            instance.user.email = user_data["email"]
            instance.user.username = user_data["email"]
            instance.user.save(update_fields=["email", "username"])

        return instance
