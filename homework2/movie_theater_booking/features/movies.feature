Feature: Movie Management
    As a user
    I want to view movies
    So that I can choose one to book seats for

    Scenario: View list of all now playing movies
        Given I am on the movies page
        And a movie exists with title "Forrest Gump"
        When I select the movie
        Then I should see the movie details page
        And the movie's duration is 142 minutes
        And the response status should be 200

    Scenario: Admin can add a new movie
        Given I am logged in as an administrator
        When I create a new movie "Toy Story"
        Then the movie "Toy Story" should exist in the database

   