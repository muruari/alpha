from __future__ import unicode_literals
import bcrypt, time
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime

def current_user(request):
	return User.objects.get(id = request.session['user_id'])


def registration(request):
	return render(request, 'exam/registration.html')


def register(request):
    check = User.objects.validate(request.POST)
    if request.method != 'POST':
		return redirect('/')
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="register")
            return redirect('/')

    passwd = request.POST['password']
    if len(check) == 0:
		hashed_pw = bcrypt.hashpw(str(passwd).encode(), bcrypt.gensalt())

    #Creates a new user in the database:
		user = User.objects.create(
			name = request.POST['name'],
			username = request.POST['username'],
			password = hashed_pw
		)


    username = request.POST['username']
    user = User.objects.get(username = username) # THIS LINE results in JSON serializable error because I was capturing the ENTIRE user object into session.
    request.session['user_id'] = user.id
    request.session['name'] = user.name

    return redirect('/dashboard')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    user = User.objects.filter(username = request.POST.get('username')).first()
    if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        return redirect('/dashboard')
    else: 
        messages.add_message(request, messages.INFO, 'Your credentials are invalid! Please try again.', extra_tags="login")
        return redirect('/')
    return redirect('/dashboard')

	

def logout(request):
		request.session.clear()
		return redirect('/')


def dashboard(request):
	context = {
        'available_trips' : Trip.objects.exclude(trips = User.objects.get(id = request.session['user_id'])),
        'my_trips' : Trip.objects.filter(trips = User.objects.get(id = request.session['user_id']))

    }
        return render(request, 'exam/dashboard.html', context)


def add_trip_page(request):
    return render(request, 'exam/add_plan.html')


def create_trip(request):

    #Creates a new user in the database:

    check = Trip.objects.validate_trip(request.POST)
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="create_trip")
            return redirect('/add_trip')


    if len(check) == 0:

        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            depart_date = request.POST['depart_date'],
            return_date = request.POST['return_date'],
            created_by = user
        )
    return redirect('/dashboard')


def reserve_trip(request, id):
    user = User.objects.get(id = request.session['user_id'])
    trip = Trip.objects.get (id = id)
    trip.trips.add(user)
    trip.save()
    return redirect('/dashboard')

def remove_trip(request, id):
    user = User.objects.get(id = request.session['user_id'])
    trip = Trip.objects.get (id = id)
    trip.trips.remove(user)
    return redirect('/dashboard')

def trip_info(request, id):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'trip' : Trip.objects.get(id=id),
        'planned_by' : User.objects.get(user_trips = Trip.objects.get(id = id)),
        'reserved' : User.objects.filter(all_trips = Trip.objects.get(id = id)).exclude(id = request.session['user_id']),
    }
    return render(request, 'exam/user.html', context)

        # if request.method == 'POST':
    #     # request.session['username'] = request.POST.get('username')

    #     username = request.POST['username']
    #     user = User.objects.get(username = username) # THIS LINE results in JSON serializable error because I was capturing the ENTIRE user object into session.
    #     request.session['user_id'] = user.id
    #     request.session['name'] = user.name
    #     # passwd = request.POST.get('login_password')
        
    #     if user and bcrypt.checkpw(str(request.POST.get('login_password')).encode(), user.password.encode()): # was saying password.encode() was a NoneType, converted the passwd variable into a string.
    #         return redirect('/dashboard')
        
        
    #     else:
    #         messages.add_message(request, messages.INFO, 'Your credentials are invalid! Please try again.', extra_tags="login")
    #         return redirect('/')
