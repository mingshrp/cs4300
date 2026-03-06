from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    # Poster field added to allow storing and displaying movie poster images
    poster = models.ImageField(upload_to="movie_posters/", blank=True, null=True)  
    # Wide poster to fit slideshow of movies

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)  
    is_booked = models.BooleanField(default=False)              # Booking status (False=available vs True=booked)

    def __str__(self):
        return f"{self.seat_number} - {'Booked' if self.is_booked else 'Available'}"

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, related_name="booking") # Prevents same seat being booked twice
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} booked {self.seat} for {self.movie}"

