from django.urls import path
from . import views

urlpatterns = [
    path('myinfo/', views.my_info_view, name='my_info'),  # URL для нашего GET-запроса
]