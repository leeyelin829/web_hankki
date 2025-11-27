from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.post_list, name='post_list'),
    path('community/create/', views.post_create, name='post_create'),
    path('community/<int:post_id>/', views.post_detail, name='post_detail'),
    path('community/<int:post_id>/like/', views.post_like, name='post_like'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('mypage/', views.mypage, name='mypage'),  # 🆕 마이페이지 추가
]