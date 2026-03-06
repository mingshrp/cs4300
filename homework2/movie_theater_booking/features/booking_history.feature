Feature: Seat Booking
    As a user
    I want to book seats for a movie
    So that I can reserve my spot

    Scenario: View available seats for a movie
        Given a movie exists with title "KPop Demon Hunters"
        And seats exist in the database
        When I visit the seat booking page for that movie
        Then I should see the seat layout
        And the response status should be 200

    Scenario: Book an available seat
        Given a movie exists with title "Avatar"
        And an available seat exists with number "A1"
        When I book that seat for that movie via API
        Then a booking should be created
        And the response status should be 201

    Scenario: A user can delete created bookings 
        Given I am on bookings history page
        And I have a booking for "KPop Demon Hunters"
        Then I can delete the booking
        Then "KPop Demon Hunters" should no longer appear in my booking history