from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'), 
    path('about-us', views.about, name='about'), 
    path('contact', views.contact, name='contact'), 
    path('Auth/user/login/', views.login, name='login'),
    path('Auth/user/register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user/dashboard/', views.dashboard, name='dashboard'),
    path('user/dashboard/<str:pk>/deposit/', views.deposit, name='deposit'),
    path('user/dashboard/<str:pk>/profile/', views.profile, name='profile'),
    path('user/dashboard/<str:pk>/edit/profile/', views.editProfile, name='editprofile'),
    path('user/dashboard/payment/method/', views.payment, name='payment'),
    path('user/dashboard/<str:pk>/Investment/', views.invest, name='invest'),
    path('user/dashboard/Investment/plan/', views.plan, name='plan'),
    path('user/dashboard/Investment/history/', views.investments, name='history'),
    path('user/dashboard/withdraw/', views.withdrawal, name='withdraw'),
]