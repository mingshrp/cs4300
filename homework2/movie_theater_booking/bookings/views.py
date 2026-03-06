from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, permissions 
from rest_framework.response import Response
from django.contrib import messages

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
        return Booking.objects.all()
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
    seats = Seat.objects.all().order_by("seat_number")

     # Build rows for the seat map (same idea you already have)
    rows = []
    row_letters = "ABCDEF"
    for letter in row_letters:
        row_seats = [s for s in seats if str(s.seat_number).startswith(letter)]
        row_seats.sort(key=lambda s: int(str(s.seat_number)[1:]) if str(s.seat_number)[1:].isdigit() else 0)
        rows.append((letter, row_seats))

    if request.method == "POST":
        seat_ids = request.POST.getlist("seat_ids")  

        if not seat_ids:
            messages.error(request, "Please select at least one seat.")
            return redirect("seat_booking", movie_id=movie.id)

        selected_seats = list(Seat.objects.filter(id__in=seat_ids))

        # block double-booking
        already = [str(s.seat_number) for s in selected_seats if Booking.objects.filter(seat=s, movie=movie).exists()]
        if already:
            messages.error(request, f"These seats are already booked: {', '.join(already)}")
            return redirect("seat_booking", movie_id=movie.id)

        # create bookings + mark seats booked
        for seat in selected_seats:
            Booking.objects.create(
                movie=movie,
                seat=seat,
                user=request.user if request.user.is_authenticated else None  # remove if your Booking has no user
            )
            seat.is_booked = True
            seat.save()

        messages.success(request, "Booking confirmed!")
        return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {"movie": movie, "rows": rows})

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

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, "bookings/movie_detail.html", {"movie": movie})