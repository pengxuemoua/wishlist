from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required 
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating a form from data
        place = form.save(commit=False) # creating a model object from form. get data but don't save yet
        place.user = request.user
        if form.is_valid(): # validation againsts DB constraints
            place.save() # saves place to db
            return redirect('place_list') # reloads home place

    # if no post is made, display unvisited places according to name
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_placce = NewPlaceForm()
    #render to wishlist.html and send data for display
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_placce})

@login_required
def places_visited(request):
    # display places that are visited according to name
    visited = Place.objects.filter(visited=True).order_by('name')
    #render to visited.html and send data for display
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get() will return one object
        
        place = get_object_or_404(Place, pk=place_pk) # attempt to make query to db, if pk not found return 404 error
        if place.user == request.user: # make sure place.user is the same as request.user
            place.visited = True # checks that visited is checked
            place.save() # save changes to the database
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list') #redirect to place_list to refresh page

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does place belong to current user?
    if place.user != request.user:
        return HttpResponseForbidden

    # if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place) # read the form data by making a new TripReviewForm from the request.post and FILES uploaded data
        if form.is_valid(): # check if data is valid
            form.save() # update data
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary message, refine later
        
        return redirect('place_details', place_pk=place_pk)

    else:
        # if Get request, show Place info and optional form
        # if place is visited, show form; if place is not visited, no form
        if place.visited: 
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place':place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place':place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
            return HttpResponseForbidden()


@login_required
def about(request):
    author = 'Pengxue'
    about = 'A website to create a list of places to visit'
    #render about.html and send data for display
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})



