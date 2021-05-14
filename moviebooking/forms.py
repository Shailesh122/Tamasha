from django import forms
from .models import city, movie, User
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SearchForm(forms.Form):
    city = forms.IntegerField(
        widget=forms.Select(
            choices=city.objects.all().values_list('city_id', 'city_name')
        )
    )
    movie = forms.IntegerField(
        widget=forms.Select(
            choices=movie.objects.all().values_list('movie_id', 'movie_name')
        )
    )
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', }), initial=datetime.date.today)


class BookingForm(forms.Form):
    theater_relid = forms.IntegerField(widget=forms.HiddenInput())


class SeatsForm(forms.Form):
    rows = ['A', 'B', 'C', 'D', 'E']
    choicelist = [['A1', ''], ['A2', ''], ]

    choices = forms.MultipleChoiceField(
        choices=choicelist,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'rectanglebar'}),
        label=False,
    )


class SeatsForm2(forms.Form):
    selected_seats = forms.CharField(
        label='', widget=forms.HiddenInput(), required=False)
    theater_relid = forms.CharField(label='', widget=forms.HiddenInput())
