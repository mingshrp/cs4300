# Homework 2

This project implements a movie theater booking system using Django and Django REST Framework.

## Project Structure
```
movie_theater_booking/
├── manage.py
├── requirements.txt
├── movie_theater_booking/        
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── bookings/                     # Main app
│   ├── models.py                 # Movie, Seat, Booking models
│   ├── views.py                  # HTML + API views
│   ├── serializers.py            # DRF serializers
│   ├── urls.py                   # URL routing
│   ├── tests.py                  
│   ├── admin.py                  
│   └── templates/
│       └── bookings/
│           ├── base.html
│           ├── movie_list.html
│           ├── movie_detail.html
│           ├── seat_booking.html
│           └── booking_history.html
├── features/                     # BDD tests
│   ├── environment.py
│   ├── movies.feature
│   ├── bookings.feature
│   ├── booking_history.feature
│   └── steps/
│       └── steps.py
└── media/                        # Uploaded images
    ├── movie_posters/
    └── movie_banners/
```

## How to Run the Project

**1.** Create a virtual environment and activate it:

```bash
python3 -m venv <name_of_virtual_environment> --system-site-packages
source <name_of_virtual_environment>/bin/activate
```

**2.** Clone this repository and move into the project's directory containing `manage.py`:

```bash
git clone https://github.com/mingshrp/cs4300.git
cd cs4300/homework2/movie_theater_booking
```

**3.** Install dependencies:
```bash
pip install -r requirements.txt
```

**4.** Run migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
**5.** Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

You will be prompted to enter a username, email, and password. Once created, you can log in at `/admin/`.

**6.** Start the development server:
```bash
python manage.py runserver 0.0.0.0:3000
```

The application will be available at `http://localhost:3000`.

## How to Run Tests

**Unit & Integration Tests:**
```bash
python manage.py test
```

**BDD Tests:**
```bash
python manage.py behave

# Run a specific feature file
python manage.py behave features/movies.feature
python manage.py behave features/bookings.feature
```

## AI Usage

**ChatGPT** was used during the planning and design phase of the project.
- Planning the overall project structure and architecture of the Django application.
- Deciding how to organize models, views, serializers, and URLs.
- Thinking through the relationships between the `Movie`, `Seat`, and `Booking` models before writing any code.
- Some of the CSS styling 

**Claude.ai** was used to assist in generating the test suite for this project (edge cases, writing feature files, debugging failed tests)
