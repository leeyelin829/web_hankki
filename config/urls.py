"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views  # ✅ 추가: users 쪽 뷰 가져오기

urlpatterns = [
    # ✅ 스플래시 & 온보딩 테스트용 URL
    path("splash/", user_views.splash, name="splash"),
    path("onboarding/", user_views.onboarding, name="onboarding"),

    path('', include('hankki.urls')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]
