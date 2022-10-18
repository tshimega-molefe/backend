import uuid
from django.db import models
from django.urls import reverse
from user.models import Citizen, Security

class Emergency(models.Model):
    class Status(models.IntegerChoices):
        REQUESTED = 0, "REQUESTED"
        ACCEPTED = 1, "ACCEPTED"
        IN_PROGRESS = 2, "IN PROGRESS"
        COMPLETED = 3, "COMPLETED",
        CANCELLED = 4, "CANCELLED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    updated = models.DateTimeField(auto_now=True, editable=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.REQUESTED)
    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT, related_name='emergencys_as_citizen', blank=True, null=True)
    security = models.ForeignKey(Security, on_delete=models.PROTECT, related_name='emergencys_as_security', blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('emergency:emergency_id', kwargs={'emergency_id': self.id})

class EmergencyTrack(models.Model):
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=Emergency.Status.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.emergency} - {self.status}'