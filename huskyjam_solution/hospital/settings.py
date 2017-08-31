from django.conf import settings

#Default custom settings, can be overriden from project settings
WORK_STARTS_HOUR = getattr(settings, 'WORK_STARTS_HOUR', 9)
WORK_ENDS_HOUR = getattr(settings, 'WORK_ENDS_HOUR', 18)
APPOINTMENT_DURATION = getattr(settings, 'APPOINTMENT_DURATION', 1)