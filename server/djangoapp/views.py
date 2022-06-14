from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealer_by_id, get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
import logging
import json
###############################################

# Getting an instance of a logger
logger = logging.getLogger(__name__)


# View to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://e845b9da.eu-gb.apigw.appdomain.cloud/api/dealership"
        context["dealerships"] = get_dealers_from_cf(url)
        # dealer_names = ' '.join([dealer.short_name for dealer in context["dealerships"]])
        return render(request, 'djangoapp/index.html', context)

# View to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# View to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# View to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# View to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Logging out `{}`...".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')


# View to handle sign up request
def registration_request(request):
    context = {}
    # If GET request
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If POST request
    elif request.method == 'POST':
        # Get information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not
            logger.debug("{} is new user".format(username))
        # If it is new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login use-redirect to list page
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/registration.html', context)


# View to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://e845b9da.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context = {
            "reviews":  reviews, 
            "dealer_id": dealer_id
        }
        return render(request, 'djangoapp/dealer_details.html', context)


# View to submit a new review
def add_review(request, dealer_id):
    # User must be logged inw
    if request.user.is_authenticated:
        # GET request renders the page with the form to fill the review
        if request.method == "GET":
            # το άλλαξα ως παρακάτω. Να βλεπω με δοκιμη πως το διαβαζω στο web και να βαζω αυτην την διευθυνση
            url = f"https://e845b9da.eu-gb.apigw.appdomain.cloud/api/dealership?id={dealer_id}"
            # Get dealer details from API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)

        # POST request posts the content in the review form to the CloudantDB using the post_review Cloud Function
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
            
            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            # API Cloud Function
            url = "https://e845b9da.eu-gb.apigw.appdomain.cloud/api/review"
            json_payload = {"review": review}  # Create a JSON payload
            # POST request with the review
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting back to dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    else:
        # If user not logged in, redirect to login
        print("User must be authenticated before posting a review. Please log in.")
        return redirect("/djangoapp/login")
