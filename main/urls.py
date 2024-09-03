from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category>/', views.category_page, name='category_page'),
    path('constructor/', views.constructor, name='constructor'),
]
