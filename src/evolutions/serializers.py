from rest_framework import serializers

from .models import Evolution


class EvolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evolution
        fields = "__all__"
        read_only_fields = ("doctor", "created_at")