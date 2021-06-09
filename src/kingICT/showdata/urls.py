from django.urls import path

from . import views

app_name = 'showdata'

urlpatterns = [
	       path('', views.home, name="home")
	       ]
