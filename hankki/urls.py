from django.urls import path
from . import views

app_name = 'hankki'

urlpatterns = [
    # path('', views.index, name='index'),

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