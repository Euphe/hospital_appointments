from django.db import models
from django.conf import settings

class Doctor(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    def __str__(self):
        return self.name


class Appointment(models.Model):
    appointment_datetime = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100)