from rest_framework import serializers
from user.serializers import CitizenSerializer, SecuritySerializer
from .models import Emergency, EmergencyTrack

class EmergencySerializer(serializers.ModelSerializer):
    citizen = CitizenSerializer(required=False)
    security = SecuritySerializer(required=False)

    class Meta:
        model = Emergency
        fields = ["id", "status", "citizen", "security"] 
        read_only_fields = ["id"]

    def create(self, validated_data):
        citizen = self.context["user"].citizen
        emergency = Emergency.objects.create(citizen=citizen)
        emergency_track = EmergencyTrack.objects.create(emergency=emergency, status=emergency.status)
        
        return emergency