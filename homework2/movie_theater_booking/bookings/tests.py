from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from django.urls import reverse
from .models import Movie, Seat, Booking

class MovieModelTest(TestCase):
    """Test suite for the Movie model."""

    def setUp(self):
        """Set up test fixtures for each test."""
        self.movie = Movie.objects.create(
            title="The Dark Knight",
            description="A superhero crime thriller",
            release_date=date(2008, 7, 18),
            duration=152
        )

    def test_create_movie(self):
        """
        Test that a Movie instance is created correctly with all fields.
        Verifies title, description, release_date, and duration are saved
        and retrieved accurately from the database.
        """
        self.assertEqual(self.movie.title, "The Dark Knight")
        self.assertEqual(self.movie.description, "A superhero crime thriller")
        self.assertEqual(self.movie.release_date, date(2008, 7, 18))
        self.assertEqual(self.movie.duration, 152)

    def test_movie_str(self):
        """
        Test that the Movie __str__ method returns the movie title.
        """
        self.assertEqual(str(self.movie), "The Dark Knight")

    def test_title_length(self):
        """
        Test that title length validation works correctly using subtests.
        Titles exceeding the max_length of 300 characters should raise a
        ValidationError on full_clean(). Titles within the limit should not.
        """
        cases = [
            ("exceeds_max_length", "A" * 301, True),
            ("exact_max_length",   "A" * 300, False),
            ("within_max_length",  "A" * 299, False),
        ]
        for name, title, should_raise in cases:
            with self.subTest(name=name, title_length=len(title)):
                movie = Movie.objects.create(
                    title=title,
                    description="Test description",
                    release_date=date.today(),
                    duration=90,
                )
                if should_raise:
                    with self.assertRaises(ValidationError):
                        movie.full_clean()
                else:
                    try:
                        movie.full_clean()
                    except ValidationError:
                        self.fail(f"full_clean() raised ValidationError for title of length {len(title)}")

    def test_optional_description(self):
        """
        Test that a movie can be created without a description
        since the description field allows blank values.
        """
        movie = Movie.objects.create(
            title="No Description Movie",
            release_date=date.today(),
            duration=90
        )
        self.assertEqual(movie.description, "")

class SeatModelTest(TestCase):
    """
    Test cases for the Seat model.
    """
    def setUp(self):
        """Set up a test seat instance."""
        self.seat = Seat.objects.create(seat_number="A1")

    def test_create_seat(self):
        """
        Test that a Seat is created with the correct seat number
        and defaults to not booked.
        """
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertFalse(self.seat.is_booked)

    def test_seat_str_available(self):
        """
        Test that the Seat __str__ method shows 'Available'
        when the seat is not booked.
        """
        self.assertEqual(str(self.seat), "A1 - Available")

    def test_seat_str_booked(self):
        """
        Test that the Seat __str__ method shows 'Booked'
        when the seat is booked.
        """
        self.seat.is_booked = True
        self.seat.save()
        self.assertEqual(str(self.seat), "A1 - Booked")

    def test_seat_number_unique(self):
        """
        Test that two seats cannot share the same seat number.
        Creating a duplicate should raise an IntegrityError.
        """
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Seat.objects.create(seat_number="A1")

class BookingModelTest(TestCase):
    """Test suite for the Booking model."""

    def setUp(self):
        """
        Set up test fixtures for each test.
        Creates a test movie and seat to be used across all tests in this class.
        """
        self.movie = Movie.objects.create(
            title="Avatar",
            description="Epic sci-fi",
            release_date=date(2009, 12, 18),
            duration=162
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_create_booking(self):
        """
        Test that a Booking instance is created correctly with movie and seat fields.
        Verifies that the booking is linked to the correct movie and seat.
        """
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
        )
        self.assertEqual(booking.movie.title, "Avatar")
        self.assertEqual(booking.seat.seat_number, "A1")

    def test_booking_date_auto_set(self):
        """
        Test that booking_date is automatically set on creation
        and is not None.
        """
        booking = Booking.objects.create(movie=self.movie, seat=self.seat)
        self.assertIsNotNone(booking.booking_date)

    def test_no_double_booking(self):
        """
        Test that the same seat cannot be booked twice due to the
        OneToOneField constraint on Seat, which raises an IntegrityError.
        """
        from django.db import IntegrityError
        Booking.objects.create(movie=self.movie, seat=self.seat)
        with self.assertRaises(IntegrityError):
            Booking.objects.create(movie=self.movie, seat=self.seat)

    def test_booking_deleted_on_movie_delete(self):
        """
        Test that bookings are deleted when the associated movie is deleted
        due to CASCADE on_delete behavior.
        """
        Booking.objects.create(movie=self.movie, seat=self.seat)
        self.movie.delete()
        self.assertEqual(Booking.objects.count(), 0)

class SeatBookingViewTest(TestCase):
    """Test suite for the seat_booking view."""

    def setUp(self):
        """
        Set up test client, movie, and seats for view tests.
        """
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space epic",
            release_date=date(2014, 11, 7),
            duration=169
        )
        self.seat = Seat.objects.create(seat_number="B1")

    def test_seat_booking_page_loads(self):
        """
        Test that the seat booking page returns a 200 status code
        and uses the correct template.
        """
        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/seat_booking.html")

    def test_seat_booking_post_creates_booking(self):
        """
        Test that submitting a valid seat selection via POST creates
        a Booking record in the database.
        """
        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        response = self.client.post(url, {"seat_ids": [self.seat.id]})
        self.assertEqual(Booking.objects.count(), 1)
        self.assertRedirects(response, reverse("booking_history"))

    def test_seat_booking_post_no_seats_selected(self):
        """
        Test that submitting a POST with no seats selected does not
        create a booking and redirects back to the seat booking page.
        """
        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        response = self.client.post(url, {"seat_ids": []})
        self.assertEqual(Booking.objects.count(), 0)

    def test_double_booking_blocked(self):
        """
        Test that attempting to book an already booked seat
        does not create a duplicate booking.
        """
        Booking.objects.create(movie=self.movie, seat=self.seat)
        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        self.client.post(url, {"seat_ids": [self.seat.id]})
        self.assertEqual(Booking.objects.count(), 1)

    def test_invalid_movie_id_returns_404(self):
        """
        Test that requesting seat booking for a non-existent movie
        returns a 404 response.
        """
        url = reverse("seat_booking", kwargs={"movie_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class BookingAPITest(TestCase):
    """
    Integration tests for the Booking API endpoints.
    Tests creation, retrieval, and double-booking prevention.
    """

    def setUp(self):
        """
        Set up test client, movie, and seat data for each test.
        """
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title="Avatar",
            description="Epic sci-fi",
            release_date=date(2009, 12, 18),
            duration=162
        )
        self.seat = Seat.objects.create(seat_number="B1")
        self.list_url = reverse("booking-list")

    def test_list_bookings_returns_200(self):
        """
        Test that GET /api/bookings/ returns a 200 status code.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking_returns_201(self):
        """
        Test that POST /api/bookings/ with valid data returns a 201 status code
        and creates a new booking in the database.
        """
        payload = {"movie": self.movie.id, "seat": self.seat.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_data_format(self):
        """
        Test that the booking response contains the expected fields:
        id, movie, seat, and booking_date.
        """
        payload = {"movie": self.movie.id, "seat": self.seat.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertIn("id", response.data)
        self.assertIn("movie", response.data)
        self.assertIn("seat", response.data)
        self.assertIn("booking_date", response.data)

    def test_create_booking_missing_fields_returns_400(self):
        """
        Test that POST /api/bookings/ with missing required fields
        returns a 400 Bad Request status code.
        """
        payload = {"movie": self.movie.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_booking_returns_204(self):
        """
        Test that DELETE /api/bookings/<id>/ returns a 204 status code
        and removes the booking from the database.
        """
        booking = Booking.objects.create(movie=self.movie, seat=self.seat)
        url = reverse("booking-detail", kwargs={"pk": booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)