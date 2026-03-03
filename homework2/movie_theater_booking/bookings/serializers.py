from rest_framework import serializers  
from .models import Movie, Seat, Booking
# https://www.w3tutorials.net/blog/django-rest-framework-use-different-serializers-in-the-same-modelviewset/#understanding-modelviewset 

# Define serializer classes: map Django models to JSON representations and validate API endpoints

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        # Use movie model from models.py
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', "is_booked"]
        # is_booked is determined by booking logic, users cannot manually change it
        read_only_fields = ['is_booked']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date']
        # User not allowed to manually modifiy booking date AND user ID
        read_only_fields = ['booking_date', 'user']
