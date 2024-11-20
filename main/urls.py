from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('product_detail/<int:pk>/<str:name>/', views.product_detail, name='product_detail'),
    path('category/<slug:category>/', views.category_page, name='category_page'),
    path('constructor/', views.constructor, name='constructor'),
    path('constructor_ajax/', views.constructor_ajax, name='constructor_ajax'),
    path('get-bisquit-description/<int:bisquit_id>/', views.get_bisquit_description, name='get_bisquit_description'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('del_cart/', views.del_cart, name='del_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('del_from_cart/<str:type>/<int:cart_id>', views.del_from_cart, name='del_from_cart'),
    path('add_quant_cart/<str:type>/<int:cart_id>', views.add_quant_cart, name='add_quant_cart'),
# 
    path('order_processing/', views_admin.order_processing, name='order_processing'),
    path('order_ready/<int:pk>/', views_admin.order_ready, name='order_ready'),
    path('order_status/<int:pk>/', views_admin.order_status, name='order_status'),
    path('moderate_comments/', views_admin.moderate_comments, name='moderate_comments'),
    path('app_del_comments/<str:fun>/<int:pk>/', views_admin.app_del_comments, name='app_del_comments'),

]
