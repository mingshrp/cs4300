# App-level urls.py 
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import views

# Create a router 
router = DefaultRouter()

# Register API endpoints
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    # HTML routes
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/seats/", views.seat_booking, name="seat_booking"),
    path("history/", views.booking_history, name="booking_history"),
]

# Add API routes under /api/
urlpatterns += [
    path("api/", include(router.urls)),
]