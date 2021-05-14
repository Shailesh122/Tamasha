from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.index),
    path('', views.index),
    path('searchpage/', views.searchpage),
    path('bookingpage/', views.BookingPage),
    path('bookingpage/success/', views.BookingSuccess),
    path('mybookings/', views.myBookings),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register")
]
