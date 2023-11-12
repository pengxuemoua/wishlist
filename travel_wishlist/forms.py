from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

class DateInput(forms.DateInput):
    input_type = 'date'

class TripReviewForm(forms.ModelForm):
    class Meta: # class meta describes information about objecy
        model = Place # model belongs to Place model
        fields = ('notes', 'date_visited', 'photo') # form has three fields
        widgets = { 
            'date_visited': DateInput() # user will get a calendar to select a date
        }