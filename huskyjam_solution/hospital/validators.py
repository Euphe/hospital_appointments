from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django.utils import timezone
from hospital.models import Appointment
from hospital.settings import WORK_STARTS_HOUR, WORK_ENDS_HOUR, APPOINTMENT_DURATION

def within_work_hours_validator(appointment_datetime):
    # Don't allow appointments in non-work hours
    hour = appointment_datetime.hour
    minute = appointment_datetime.minute
    # The start of the appointment should not be earlier than WORK_STARTS_HOUR
    if hour < 9:
        raise ValidationError(_('The earliest possible time an appointment can be booked at is {}:00.'.format(WORK_STARTS_HOUR)), code='booking_time_earlier_than_working_hours')

    # The end of the appointment should not be later than (WORK_ENDS_HOUR - APPOINTMENT_DURATION)
    if (hour > WORK_ENDS_HOUR - APPOINTMENT_DURATION) or ( (hour == WORK_ENDS_HOUR) and  minute > 0 ):
        raise ValidationError(_('The latest possible time an appointment can be booked at is {}:00.'.format(WORK_ENDS_HOUR - APPOINTMENT_DURATION)), code='booking_time_later_than_working_hours')

def not_in_past_validator(appointment_datetime):
    if appointment_datetime < timezone.now():
        raise ValidationError(_('Please select an appointment time in future.'), code='booking_time_in_past')


def unique_for_time_range_validator(appointment_datetime, left_border, right_border, pk=None):
    appointments_at_that_time = Appointment.objects.filter(appointment_datetime__gte=left_border, appointment_datetime__lte=right_border)
    if pk:
        appointments_at_that_time = appointments_at_that_time.exclude(pk=pk)

    if appointments_at_that_time:
        raise ValidationError(_('Specified time is unavailable for booking.'), code='booking_time_is_occupied')