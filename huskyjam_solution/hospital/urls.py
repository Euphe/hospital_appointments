from django.conf.urls import url
from hospital.views import book_appointment
urlpatterns = [
    url(r'^$', book_appointment, name='book_appointment'),
]
