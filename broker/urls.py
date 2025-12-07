from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmers/new/', views.farmer_create, name='farmer_create'),
    path('farmers/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('farmers/<int:pk>/edit/', views.farmer_update, name='farmer_update'),
    path('farmers/<int:pk>/delete/', views.farmer_delete, name='farmer_delete'),
    path('collections/new/', views.collection_create, name='collection_create'),
    path('collections/history/', views.collection_history, name='collection_history'),
]
