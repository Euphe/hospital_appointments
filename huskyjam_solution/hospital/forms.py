from django import forms
from hospital.models import Appointment
from django.contrib.admin import widgets 
from datetimewidget.widgets import DateTimeWidget 
from django.core.exceptions import ValidationError
from hospital.settings import WORK_STARTS_HOUR, WORK_ENDS_HOUR, APPOINTMENT_DURATION
from hospital.validators import unique_for_time_range_validator, not_in_past_validator, within_work_hours_validator
from datetime import datetime, timedelta
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        self.fields['appointment_datetime'] = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=DateTimeWidget(bootstrap_version=3), validators=[not_in_past_validator, within_work_hours_validator])

    def clean_appointment_datetime(self):
        appointment_datetime = self.cleaned_data['appointment_datetime']
        if self.instance.pk is None: #An instance is being created, not updated
            unique_for_time_range_validator(appointment_datetime, appointment_datetime-timedelta(hours=APPOINTMENT_DURATION), appointment_datetime+timedelta(hours=APPOINTMENT_DURATION), self.instance.pk)
        return appointment_datetime

    class Meta:
        model = Appointment
        exclude = ('pk',)
