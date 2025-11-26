from django.urls import path
from . import views

app_name = 'hankki'

urlpatterns = [
    # path('', views.index, name='index'),

    path('supplier/', views.supplier, name='supplier'),

    path('write_health_category/', views.write_health_category, name='write_health_category'),
    path('write_health_category/<int:id>', views.write_health_category, name='write_health_category'),
    path('write_lunchbox/', views.write_lunchbox, name='write_lunchbox'),
    path('write_lunchbox/<int:id>', views.write_lunchbox, name='write_lunchbox'),
]