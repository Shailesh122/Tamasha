from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class theater(models.Model):
    theater_id = models.AutoField(primary_key=True)
    theater_name = models.CharField(max_length=1000)
    address = models.CharField(max_length=2000)
    pin_code = models.CharField(max_length=10)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)


class movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=255)
    duration_minutes = models.IntegerField()
    url = models.CharField(max_length=2038, default="")


class users(models.Model):
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=255, primary_key=True, null=False)


class user_bookings(models.Model):
    user_bookings_id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    transaction_number = models.IntegerField()
    transaction_mode = models.CharField(max_length=100)
    amount_paid = models.IntegerField()


class theater_movies_rel(models.Model):
    theater_movies_id = models.AutoField(primary_key=True)
    theater_id = models.ForeignKey(theater, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(movie, on_delete=models.CASCADE)
    show_start = models.DateTimeField()
    price = models.IntegerField()


class theater_seats(models.Model):
    theater_seats_id = models.AutoField(primary_key=True)
    theater_movies_id = models.ForeignKey(theater_movies_rel, on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=10, default="NA")


class user_seats(models.Model):
    user_seats_id = models.AutoField(primary_key=True)
    user_bookings_id = models.ForeignKey(
        user_bookings, on_delete=models.CASCADE)
    theater_seats_id = models.ForeignKey(
        theater_seats, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="NA")
