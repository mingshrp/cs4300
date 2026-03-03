from django.shortcuts import render
from rest_framework import viewsets, status, permissions 
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
# Create your views here.
