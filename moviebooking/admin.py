from django.contrib import admin
from .models import city, movie, theater_movies_rel, theater, theater_seats, user_seats, users, user_bookings
# Register your models here.

admin.site.register(city)
admin.site.register(movie)
admin.site.register(theater)
admin.site.register(theater_movies_rel)
admin.site.register(theater_seats)
admin.site.register(users)
admin.site.register(user_seats)
admin.site.register(user_bookings)
