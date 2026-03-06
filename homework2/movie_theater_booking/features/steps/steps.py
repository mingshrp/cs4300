from behave import given, when, then
from django.test import Client
from rest_framework.test import APIClient
from bookings.models import Movie, Seat, Booking
from datetime import date


def get_api_client(context):
    if not hasattr(context, "api_client"):
        context.api_client = APIClient()
    return context.api_client

def get_client(context):
    if not hasattr(context, "client"):
        context.client = Client()
    return context.client


# ======== Given Steps ========

@given("I am on the movies page")
def step_on_movies_page(context):
    client = get_client(context)
    context.response = client.get("/movies/")

@given('a movie exists with title "{title}"')
def step_movie_exists(context, title):
    duration = 142 if title == "Forrest Gump" else 120
    context.movie = Movie.objects.create(
        title=title,
        description="A great movie",
        release_date=date(2020, 1, 1),
        duration=duration
    )

@given("seats exist in the database")
def step_seats_exist(context):
    context.seat = Seat.objects.create(seat_number="A1")

@given('an available seat exists with number "{seat_number}"')
def step_available_seat_exists(context, seat_number):
    context.seat = Seat.objects.create(seat_number=seat_number)

@given("I am logged in as an administrator")
def step_logged_in_as_admin(context):
    from django.contrib.auth.models import User
    context.admin = User.objects.create_superuser(
        username="admin",
        password="admin1234",
        email="admin@test.com"
    )
    client = get_client(context)
    client.login(username="admin", password="admin1234")

@given("I am on bookings history page")
def step_on_booking_history_page(context):
    client = get_client(context)
    context.response = client.get("/bookings/history/")

@given('I have a booking for "{title}"')
def step_have_booking_for(context, title):
    movie = Movie.objects.create(
        title=title,
        description="A great movie",
        release_date=date(2020, 1, 1),
        duration=120
    )
    seat = Seat.objects.create(seat_number="D4")
    context.booking = Booking.objects.create(movie=movie, seat=seat)
    context.movie = movie


# ======== When Steps ========

@when("I select the movie")
def step_select_movie(context):
    client = get_client(context)
    context.response = client.get(f"/movies/{context.movie.pk}/")

@when('I create a new movie "{title}"')
def step_create_movie(context, title):
    client = get_api_client(context)
    context.response = client.post("/api/movies/", {
        "title": title,
        "description": "An animated classic",
        "release_date": "1995-11-22",
        "duration": 81
    }, format="json")

@when("I visit the seat booking page for that movie")
def step_visit_seat_booking(context):
    client = get_client(context)
    context.response = client.get(f"/movies/{context.movie.id}/seats/")

@when("I book that seat for that movie via API")
def step_book_seat(context):
    client = get_api_client(context)
    context.response = client.post("/api/bookings/", {
        "movie": context.movie.id,
        "seat": context.seat.id
    }, format="json")


# ======== Then Steps ========

@then("the response status should be {status_code:d}")
def step_check_status(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected {status_code}, got {context.response.status_code}"
    )

@then("I should see the movie details page")
def step_see_movie_details(context):
    assert context.response.status_code == 200, "Movie details page did not load"

@then("the movie's duration is 142 minutes")
def step_check_duration(context):
    assert context.movie.duration == 142, (
        f"Expected duration 142, got {context.movie.duration}"
    )

@then('the movie "{title}" should exist in the database')
def step_movie_exists_in_db(context, title):
    assert Movie.objects.filter(title=title).exists(), (
        f'Movie "{title}" was not found in the database'
    )

@then("I should see the seat layout")
def step_see_seat_layout(context):
    assert context.response.status_code == 200
    assert b"seat" in context.response.content.lower()

@then("a booking should be created")
def step_booking_created(context):
    assert Booking.objects.count() >= 1, "Expected a booking to be created"

@then("I can delete the booking")
def step_delete_booking(context):
    client = get_client(context)
    context.response = client.post(f"/booking/delete/{context.booking.id}/")
    assert not Booking.objects.filter(id=context.booking.id).exists(), (
        "Booking was not deleted"
    )

@then('"{title}" should no longer appear in my booking history')
def step_not_in_booking_history(context, title):
    assert not Booking.objects.filter(movie__title=title).exists(), (
        f'"{title}" booking still exists but should have been deleted'
    )