# App-level urls.py 
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import views

# Create a router 
router = DefaultRouter()

# Register API endpoints
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

# all the URLs for API will come from the router
urlpatterns = router.urls
