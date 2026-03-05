from django.shortcuts import render, get_object_or_404, redirect
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
    permission_classes = [permissions.AllowAny]

class SeatViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Seat model.
    - View seat availability
    - Retrieve seat details
    Seat booking status is managed through BookingViewSet.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

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


# ======== Views for HTML Template Pags ============

def movie_list(request):
    """
    Display list of all movies.

    param: 
        request (HttpRequest): The incoming HTTP request object.
    return:
        HttpResponse: Rendered HTML page displaying all movies from the database.
    """
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})

def seat_booking(request, movie_id):
    """
    Display seat availability for a selected movie.

    params:
        request (HttpRequest): The incoming HTTP request object.
        movie_id: ID of the selected movie.

    return:
        HttpResponse: HTML page showing seat numbers and booking status for movie.

    ERROR:
        Http404: If a movie with the given ID does not exist.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.all()

    return render(request, "bookings/seat_booking.html", {
        "movie": movie, 
        "seats": seats
    })

def booking_history(request):
    """
    Show booking history for user.

    param:
        request (HttpRequest): The incoming HTTP request object.

    return:
        HttpResponse: HTML page showingvuser's booking history. 
    """
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = [] # pass empty list if user is not authenticated

    return render(request, "bookings/booking_history.html", {
        "bookings": bookings
    })

