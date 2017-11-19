from django.shortcuts import render, redirect
from models import User, Travel
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "belt_exam_app/index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors) <= 0:
        name = request.POST["name"]
        username = request.POST["username"]
        hashed_password = bcrypt.hashpw((request.POST['password'].encode()), bcrypt.gensalt(5))
        
        User.objects.create(name = name, username = username, password=hashed_password)

        request.session["username"] = username
        messages.success(request, "You have registered successfully, {}!".format(username))
        return redirect("/travels")
    else:
        for x in errors:
            messages.error(request, errors[x])
        return redirect("/")

def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) <= 0:
        #get the users name to send a greet message
        user = User.objects.get(username=request.POST["username"])
        user_name = user.username

        request.session["username"] = user_name

        messages.success(request, "Thanks for logging in, {}!".format(request.session["username"]))
        return redirect("/travels")
    else:
        for x in errors:
            messages.error(request, errors[x])
        return redirect("/")

#this view is for admin use and should be deleted or secured before deployment
def show(request):
    #dict to hold db data to display on show.html page
    db_dict = {
        "user_key" : User.objects.all()
    }
    return render(request, "belt_exam_app/show.html", db_dict)


def travels(request):
    user = User.objects.get(username=request.session["username"])

    db_dict = {
        "travels_key" : user.travels.all(),
        "travels_key2" : Travel.objects.all()
    }

    return render(request, "belt_exam_app/travels.html", db_dict)


def new_trip(request):
    return render(request, "belt_exam_app/new_trip.html")


def create_trip(request):
    errors = User.objects.create_trip_validator(request.POST) #create a new trip validtor

    if len(errors) <= 0:
        destination = request.POST["destination"]
        desc = request.POST["desc"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        
        # Insert the new trip into the db.
        Travel.objects.create(destination = destination, desc = desc, start_date = start_date, end_date = end_date)
        
        # Create a relationship between the user and the newly created trip.
        trip = Travel.objects.last()
        user = User.objects.get(username=request.session["username"])
        # users is the column name of the ManyToManyField.
        trip.users.add(user)

        messages.success(request, "You've created a new trip!")
        return redirect("/travels")
    else:
        for x in errors:
            messages.error(request, errors[x])
        return redirect("/new_trip")


def join(request, travel_id):
    trip = Travel.objects.get(id=travel_id)
    user = User.objects.get(username=request.session["username"])
    trip.users.add(user)
    return redirect("/destination/{}".format(travel_id))


def destination(request, travel_id):
    db_dict = {
        "travels_key" : Travel.objects.get(id=travel_id)
    }
    trip_planner_temp = Travel.objects.get(id=travel_id)
    trip_planner = trip_planner_temp.users.first()

    # This is to see all the users who are on this trip.
    this_trip = Travel.objects.get(id=travel_id)
    this_trip.users.all()
    return render(request, "belt_exam_app/destination.html",  db_dict, trip_planner) #Not able to pass extra variables through, trip_planner is not going through, I tried sending through in a dictionary but didn't have enough time to make it work. Same problem is on /travel page where it doesn't display the names of the users who began/planned the trips.
    


def logout(request):
    #delete session data?
    messages.success(request, "You've logged out.")
    return redirect("/")

#this view is for admin use and should be deleted or secured before deployment
def destroy(request, user_id):
    User.objects.get(id=user_id).delete()
    messages.success(request, "That user has been deleted!")
    return redirect("/show")