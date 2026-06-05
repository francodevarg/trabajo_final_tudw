from rest_framework import serializers
from doctor.models import Availability, Doctor, Specialty, Insurance
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError


class NextAvailableSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField(format="%H:%M")


class AvailableSlotSerializer(serializers.Serializer):
    time = serializers.TimeField(format="%H:%M")
    available = serializers.BooleanField()

User = get_user_model()

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError({
                "code": "NAME_REQUIRED",
                "message": "Name is required"
            })

        if Specialty.objects.filter(name=value).exists():
            raise serializers.ValidationError({
                "code": "SPECIALTY_ALREADY_EXISTS",
                "message": "Specialty already exists"
            })

        return value

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["day_of_week", "start_time", "end_time"]


class DoctorReadSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    specialty = serializers.StringRelatedField()

    insurances = serializers.StringRelatedField(
        many=True
    )

    availabilities = AvailabilitySerializer(
        many=True
    )

    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialty",
            "insurances",
            "license_number",
            "phone",
            "description",
            "consultation_fee",
            "is_active",
            "availabilities",
        ]


class DoctorCreateSerializer(serializers.ModelSerializer):

    # USER DATA
    email = serializers.EmailField(write_only=True)

    name = serializers.CharField(
        write_only=True
    )

    specialty_id = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(),
        source="specialty",
        write_only=True
    )

    insurance_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Insurance.objects.all(),
        source="insurances",
        write_only=True,
        required=False
    )

    availabilities = AvailabilitySerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Doctor
        fields = [
            "email",
            "name",

            "specialty_id",
            "insurance_ids",

            "license_number",
            "phone",
            "description",
            "consultation_fee",
            "availabilities",
        ]

    def validate_availabilities(self, value):
        errors = []

        # 1. Validar rangos inválidos
        for i, a in enumerate(value):
            if a["start_time"] >= a["end_time"]:
                errors.append({
                    "code": "INVALID_TIME_RANGE",
                    "field": "availabilities",
                    "index": i,
                })

        # 2. Agrupar por día
        by_day = {}

        for i, a in enumerate(value):
            day = a["day_of_week"]

            if day not in by_day:
                by_day[day] = []

            by_day[day].append({
                "index": i,
                "start_time": a["start_time"],
                "end_time": a["end_time"],
            })

        # 3. Ordenar y comparar solo vecinos
        for day, availabilities in by_day.items():

            # O(n log n)
            availabilities.sort(key=lambda x: x["start_time"])

            # O(n)
            for i in range(len(availabilities) - 1):
                current = availabilities[i]
                next_one = availabilities[i + 1]

                overlaps = (
                    current["end_time"] > next_one["start_time"]
                )

                if overlaps:
                    errors.append({
                        "code": "OVERLAPPING_AVAILABILITY",
                        "field": "availabilities",
                        "index": current["index"],
                        "conflicts_with": next_one["index"],
                    })

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def create(self, validated_data):

        availabilities_data = validated_data.pop(
            "availabilities",
            []
        )

        insurances_data = validated_data.pop(
            "insurances",
            []
        )

        email = validated_data.pop("email")
        name = validated_data.pop("name")

        # Create user
        user = User.objects.create(
            username=email,
            email=email,
            first_name=name,
        )

        # Create doctor
        doctor = Doctor.objects.create(
            user=user,
            **validated_data
        )


        if insurances_data:
            doctor.insurances.set(insurances_data)

        # Bulk availabilities
        availability_objects = []

        for availability_data in availabilities_data:

            availability = Availability(
                doctor=doctor,
                **availability_data
            )

            availability.clean()

            availability_objects.append(
                availability
            )

        Availability.objects.bulk_create(
            availability_objects
        )

        return doctor