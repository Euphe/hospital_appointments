from django.contrib import admin
from hospital.models import Doctor, Appointment
from django import forms
from django.contrib.admin import widgets   

class AppointmentInline(admin.StackedInline):
	model = Appointment

class DoctorAdmin(admin.ModelAdmin):
    fields = ('name', )
    list_display = ('name', )

    inlines = [
        AppointmentInline,
    ]

admin.site.register(Doctor, DoctorAdmin)