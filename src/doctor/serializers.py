from rest_framework import serializers
from doctor.models import Availability, Doctor, Specialty, Insurance
from django.contrib.auth import get_user_model


class NextAvailableSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField(format="%H:%M")


class AvailableSlotSerializer(serializers.Serializer):
    time = serializers.TimeField(format="%H:%M")
    available = serializers.BooleanField()


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name","slug"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError({
                "code": "NAME_REQUIRED",
                "message": "Name is required"
            })

        queryset = Specialty.objects.filter(name=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "code": "SPECIALTY_ALREADY_EXISTS",
                "message": "Specialty already exists"
            })

        return value

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ["id", "name", "slug"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError({
                "code": "NAME_REQUIRED",
                "message": "Name is required"
            })

        queryset = Insurance.objects.filter(name=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "code": "INSURANCE_ALREADY_EXISTS",
                "message": "Insurance already exists"
            })

        return value

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["day_of_week", "start_time", "end_time"]

class DoctorReadSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )
    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    specialty = SpecialtySerializer(read_only=True)

    insurances = InsuranceSerializer(many=True, read_only=True)

    availabilities = AvailabilitySerializer(many=True, read_only=True)


    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
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

    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

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
            "first_name",
            "last_name",
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
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        User = get_user_model()
        # Create user
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
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

class DoctorUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True, required=False)

    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    specialty_id = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(),
        source="specialty",
        write_only=True,
        required=False
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
            "first_name",
            "last_name",
            "specialty_id",
            "insurance_ids",
            "license_number",
            "phone",
            "description",
            "consultation_fee",
            "availabilities",
        ]

    def validate_availabilities(self, value):
        if not value:
            return value
        errors = []

        for i, a in enumerate(value):
            if a["start_time"] >= a["end_time"]:
                errors.append({
                    "code": "INVALID_TIME_RANGE",
                    "field": "availabilities",
                    "index": i,
                })

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

        for day, availabilities in by_day.items():
            availabilities.sort(key=lambda x: x["start_time"])
            for i in range(len(availabilities) - 1):
                current = availabilities[i]
                next_one = availabilities[i + 1]
                if current["end_time"] > next_one["start_time"]:
                    errors.append({
                        "code": "OVERLAPPING_AVAILABILITY",
                        "field": "availabilities",
                        "index": current["index"],
                        "conflicts_with": next_one["index"],
                    })

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def update(self, instance, validated_data):

        availabilities_data = validated_data.pop(
            "availabilities",
            None
        )

        insurances_data = validated_data.pop(
            "insurances",
            None
        )

        email = validated_data.pop("email", None)
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)

        if email or first_name or last_name:
            user = instance.user
            if email:
                user.email = email
                user.username = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if insurances_data is not None:
            instance.insurances.set(insurances_data)

        if availabilities_data is not None:
            instance.availabilities.all().delete()
            objs = []
            for a in availabilities_data:
                availability = Availability(
                    doctor=instance,
                    **a
                )
                availability.clean()
                objs.append(availability)
            Availability.objects.bulk_create(objs)

        return instance