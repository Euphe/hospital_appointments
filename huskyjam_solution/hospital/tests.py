from django.test import TestCase, override_settings
from hospital.models import Doctor, Appointment
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import exceptions 
from hospital.forms import AppointmentForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

class AppointmentFormRenderTestCase(TestCase):
    def test_form_template_used(self):
        response = self.client.get(reverse('book_appointment'))
        self.assertTemplateUsed(response, 'appointment_form.html')

@override_settings(WORK_STARTS_HOUR=9, WORK_ENDS_HOUR=18, APPOINTMENT_DURATION=1)
class AppointmentFormValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.time_now = timezone.now() #time at start of test
        cls.doctor = Doctor.objects.create(name='Dr. Bar Foo')
        cls.patient_name ='Foo Bar'
        cls.invalid_dt_format = '%d-%m-%Y %H:%M'
        cls.valid_dt_format = '%d/%m/%Y %H:%M'
        cls.valid_db_dt_format = '%Y-%m-%d %H:%M'

    def test_can_make_valid_appointment(self):
        time = (self.time_now + timedelta(days=1)).replace(hour=15, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)

        self.assertTrue(Appointment.objects.get(doctor__pk=self.doctor.pk, patient_name=self.patient_name,appointment_datetime=time.strftime(self.valid_db_dt_format)))

    def test_cant_book_in_past(self):
        time = (self.time_now - timedelta(days=10)).replace(hour=15, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('Please select an appointment time in future.'))

    def test_cant_book_before_hospital_opens(self):
        time = (self.time_now + timedelta(days=1)).replace(hour=8, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('The earliest possible time an appointment can be booked at is 9:00.'))


    def test_cant_book_after_hospital_closes(self):
        time = (self.time_now + timedelta(days=1)).replace(hour=19, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('The latest possible time an appointment can be booked at is 17:00.'))


    def test_cant_book_at_same_time(self):
        #First do a valid booking
        time = (self.time_now + timedelta(days=1)).replace(hour=15, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertTrue(Appointment.objects.get(doctor__pk=self.doctor.pk, patient_name=self.patient_name,appointment_datetime=time.strftime(self.valid_db_dt_format)))

        #Attempt to make another, on same time
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('Specified time is unavailable for booking.'))

    def test_cant_book_shortly_before_other_booking(self):
        #First do a valid booking
        time = (self.time_now + timedelta(days=1)).replace(hour=15, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertTrue(Appointment.objects.get(doctor__pk=self.doctor.pk, patient_name=self.patient_name,appointment_datetime=time.strftime(self.valid_db_dt_format)))

        #Attempt to make another, 30 minutes earlier
        time = (self.time_now + timedelta(days=1)).replace(hour=14, minute=30)
        input_data['appointment_datetime'] = time.strftime(self.valid_dt_format)
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('Specified time is unavailable for booking.'))


    def test_cant_book_shortly_after_other_booking(self):
        #First do a valid booking
        time = (self.time_now + timedelta(days=1)).replace(hour=15, minute=0)
        input_data = {'doctor': self.doctor.pk, 'patient_name': self.patient_name,'appointment_datetime':time.strftime(self.valid_dt_format) }
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertTrue(Appointment.objects.get(doctor__pk=self.doctor.pk, patient_name=self.patient_name,appointment_datetime=time.strftime(self.valid_db_dt_format)))

        #Attempt to make another, 30 minutes later
        time = (self.time_now + timedelta(days=1)).replace(hour=15, minute=30)
        input_data['appointment_datetime'] = time.strftime(self.valid_dt_format)
        response = self.client.post(reverse('book_appointment'), input_data)
        self.assertFormError(response,'form', field='appointment_datetime', errors=_('Specified time is unavailable for booking.'))