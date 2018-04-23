from django.urls import path

from . import views

app_name = 'webinterface'

urlpatterns = [
    path('', views.index, name='index'),
    path('addtask/', views.addtask, name='addtask'),
]