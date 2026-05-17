from rest_framework import serializers
from doctor.models import Availability, Doctor, Specialty
from django.core.exceptions import ValidationError as DjangoValidationError


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



class DoctorSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True)
    class Meta:
        model = Doctor
        fields = ["id", "name", "email", "specialty", "phone", "availabilities"]

    def validate_availabilities(self, value):
        errors = []

        # validar start < end
        for i, a in enumerate(value):
            if a["start_time"] >= a["end_time"]:
                errors.append({
                    "code": "INVALID_TIME_RANGE",
                    "field": "availabilities",
                    "index": i,
                    "meta": {
                        "start_time": a["start_time"],
                        "end_time": a["end_time"]
                    }
                })

        # validar solapamientos internos
        seen = set()

        for i in range(len(value)):
            for j in range(i + 1, len(value)):
                a = value[i]
                b = value[j]

                if (
                    a["day_of_week"] == b["day_of_week"] and
                    a["start_time"] < b["end_time"] and
                    a["end_time"] > b["start_time"]
                ):
                    key = (i, j)
                    if key not in seen:
                        errors.append({
                            "code": "OVERLAPPING_AVAILABILITY",
                            "field": "availabilities",
                            "index": i,
                            "meta": {
                                "conflicts_with_index": j,
                                "day_of_week": a["day_of_week"],
                                "range_1": {
                                    "start": a["start_time"],
                                    "end": a["end_time"]
                                },
                                "range_2": {
                                    "start": b["start_time"],
                                    "end": b["end_time"]
                                }
                            }
                        })
                        seen.add(key)

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def create(self, validated_data):
        availabilities_data = validated_data.pop("availabilities")

        doctor = Doctor.objects.create(**validated_data)

        Availability.objects.bulk_create([
            Availability(doctor=doctor, **availability_data)
            for availability_data in availabilities_data
        ])

        return doctor