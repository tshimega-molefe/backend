from rest_framework import serializers

from user.models import Citizen
from .models import Emergency

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = ["id", "status"] 
        read_only_fields = ["id"]

    def create(self, validated_data):
        citizen = self.context["user"].citizen
        return Emergency.objects.create(citizen=citizen)