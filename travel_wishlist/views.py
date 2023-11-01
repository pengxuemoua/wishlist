from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating a form from data
        place = form.save() # creating a model object from form
        if form.is_valid(): # validation againsts DB constraints
            place.save() # saves place to db
            return redirect('place_list') # reloads home place

    # if no post is made, display unvisited places according to name
    places = Place.objects.filter(visited=False).order_by('name')
    new_placce = NewPlaceForm()
    #render to wishlist.html and send data for display
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_placce})

def places_visited(request):
    # display places that are visited according to name
    visited = Place.objects.filter(visited=True).order_by('name')
    #render to visited.html and send data for display
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get() will return one object
        
        place = get_object_or_404(Place, pk=place_pk) # attempt to make query to db, if pk not found return 404 error
        place.visited = True # checks that visited is checked
        place.save() # save changes to the database
    
    return redirect('place_list') #redirect to place_list to refresh page


def about(request):
    author = 'Pengxue'
    about = 'A website to create a list of places to visit'
    #render about.html and send data for display
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})



