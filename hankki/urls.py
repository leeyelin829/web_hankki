from django.urls import path
from . import views

app_name = 'hankki'

urlpatterns = [
    path('lunch_detail/', views.lunch_detail, name='lunch_detail'),
    path('lunch_reserve/', views.lunch_reserve, name='lunch_reserve'),
    path('lunch_complete/', views.lunch_complete, name='lunch_complete'),
]