from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from hankki import views

urlpatterns = [
    path('', RedirectView.as_view(url='/lunch_detail/', permanent=False)),
    path('lunch_detail/', views.lunch_detail, name='lunch_detail'),
    path('lunch_reserve/', views.lunch_reserve, name='lunch_reserve'),
    path('lunch_complete/', views.lunch_complete, name='lunch_complete'),
    path('charge/', views.charge, name='charge'),  # 충전 페이지
    path('admin/', admin.site.urls),
]