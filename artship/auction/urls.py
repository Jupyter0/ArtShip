from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction, name='auction'),
    path('<slug:slug>/', views.auction_detail, name="auction_detail")
]