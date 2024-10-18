from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_detail/<int:pk>/<str:name>/', views.product_detail, name='product_detail'),
    path('category/<slug:category>/', views.category_page, name='category_page'),
    path('constructor/', views.constructor, name='constructor'),
    path('get-bisquit-description/<int:bisquit_id>/', views.get_bisquit_description, name='get_bisquit_description'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('del_cart/', views.del_cart, name='del_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('del_from_cart/<int:cart_id>', views.del_from_cart, name='del_from_cart'),
    path('add_quant_cart/<int:cart_id>', views.add_quant_cart, name='add_quant_cart'),
]
