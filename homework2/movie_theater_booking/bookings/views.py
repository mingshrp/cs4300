from django.shortcuts import render
from rest_framework import viewsets, status, permissions 
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create class based views using viewsets.ModelViewSet

class MovieViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Movie model with standard CRUD operations
    - List movies
    - Retrieve a movie
    - Create a movie
    - Update a movie
    - Delete a movie
    """ 
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeatViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Seat model.
    - View seat availability
    - Retrieve seat details
    Seat booking status is managed through BookingViewSet.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Booking model.

    Allows authenticated users to:
    - Create a booking
    - View their booking history

    Ensures a seat cannot be double-booked.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only bookings belonging to the logged-in user.
        """
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a booking for the authenticated user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seat = serializer.validated_data["seat"]
        if seat.is_booked:
            return Response({"detail": "This seat is already booked. Please choose another."}, status=status.HTTP_409_CONFLICT)

        booking = serializer.save(user=request.user)
        seat.is_booked = True
        seat.save()

        return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)