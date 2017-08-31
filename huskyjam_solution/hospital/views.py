from django.shortcuts import render
from hospital.forms import AppointmentForm
from django.contrib import messages


def book_appointment(request):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'You have succesfully booked an appointment!')

	if request.method == 'GET':
		form = AppointmentForm()
	return render(request, "appointment_form.html",  context={'form': form})
