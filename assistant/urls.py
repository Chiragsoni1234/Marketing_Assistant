from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/marketing-assistant/', views.marketing_api, name='marketing_api'),  # ✅ new API endpoint
]
