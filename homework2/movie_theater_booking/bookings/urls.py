# App-level urls.py 
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

# use the router's generated URLs
urlpatterns = router.urls