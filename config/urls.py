from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views

urlpatterns = [
    # ✅ 스플래시 & 온보딩 테스트용 URL
    path("splash/", user_views.splash, name="splash"),
    path("onboarding/", user_views.onboarding, name="onboarding"),

    path('', include('hankki.urls')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)