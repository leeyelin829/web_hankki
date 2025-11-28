from django.urls import path
from . import views

app_name = 'hankki'

urlpatterns = [
    # path('', views.index, name='index'),
    
    path('lunch_detail/', views.lunch_detail, name='lunch_detail'),
    path('lunch_reserve/', views.lunch_reserve, name='lunch_reserve'),
    path('lunch_complete/', views.lunch_complete, name='lunch_complete'),
    path('charge/', views.charge, name='charge'),  # 충전 페이지

    path('supplier/', views.supplier, name='supplier'),

    path('write_health_category/', views.write_health_category, name='write_health_category'),
    path('write_health_category/<int:id>/', views.write_health_category, name='write_health_category'),
    path('write_lunchbox/', views.write_lunchbox, name='write_lunchbox'),
    path('write_lunchbox/<int:id>/', views.write_lunchbox, name='write_lunchbox'),

    path('order/', views.order, name='order'),
    path('order/<int:id>/', views.order, name='order'),

    # path('order', views.create_order_with_formset, name='order'),
    # path('order/<int:id>/', views.create_order_with_formset, name='order'),

    path('list/', views.lunchbox_list, name='lunchbox_list'),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('cart/<int:id>/<int:quantity>/', views.cart, name='cart'),
]