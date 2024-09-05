from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_detail/<int:pk>/<str:name>/', views.product_detail, name='product_detail'),
    path('category/<slug:category>/', views.category_page, name='category_page'),
    path('constructor/', views.constructor, name='constructor'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('del_cart/', views.del_cart, name='del_cart'),
]
