from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import city, movie, theater_movies_rel, theater, theater_seats, user_seats, users, user_bookings
from django.contrib.auth.models import User
from .forms import SearchForm, BookingForm, SeatsForm2, SeatsForm, CreateUserForm
import datetime
from django.views.generic import FormView
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', {'movies': movie.objects.all()})


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # print(form)
            user = form.cleaned_data.get('username')
            messages.success(
                request, 'Account was created successfully for ' + user)
            return redirect('login')
        else:
            print(form)

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):

    username = ""
    password = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = User.objects.get(username=username).email
        user_id = User.objects.get(username=username).id
        request.session['name'] = username
        request.session['email'] = email
        request.session['id'] = user_id
        print(request.session.get('name'))
        print(request.session.get('email'))
        print(request.session.get('id'))
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    # return HttpResponse('Please Login!!')
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(user)  # first we logout the user then redirect it to the homepage
    return redirect('login')


@login_required(login_url='login')
def searchpage(request):
    cityid = " "
    movieid = " "
    datestring = " "
    shows = []
    url = ""
    check = False
    form2 = BookingForm(initial={'theater_relid': 2})
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cityid = form.cleaned_data['city']
            movieid = form.cleaned_data['movie']
            datestring = form.cleaned_data['date']
            theaters = theater.objects.filter(city_id=cityid).order_by(
                'theater_id').values('theater_id')
            theaternames = theater.objects.filter(city_id=cityid).order_by(
                'theater_id').values('theater_name')
            # print(theaternames) //<QuerySet [{'theater_name': 'Inox Swabhumi'}, {'theater_name': 'City Center Inox'}]>
            shows = theater_movies_rel.objects.filter(
                movie_id=movieid, theater_id__in=theaters).order_by('theater_id')

            # image url of the movie
            url = movie.objects.get(movie_id=movieid).url
            showlist = {}
            for ctheat in theaternames:
                # print(ctheat['theater_name'])  //Inox Swabhumi;City Center Inox
                showlist[str(ctheat['theater_name'])] = []
            for show in shows:  # shows has all movie shows in all theaters at that city for all timings
                li = []
                # print(show.theater_id)  # theater object (1)
                li.append(str(show.show_start)[10:16])
                # print(str(show.show_start)[10:16])  # 12:00
                # print(str(show.show_start))  # 2021-04-17 12:00:00+00:00
                form2 = BookingForm(
                    initial={'theater_relid': show.theater_movies_id})
                # print(str(show.theater_movies_id))
                li.append(form2)
                # [' 12:00', <BookingForm bound=False, valid=Unknown, fields=(theater_relid)>]
                # print(li)
                showlist[show.theater_id.theater_name].append(li)
                # print(str(show.theater_id.theater_name)) #Shailesh Talkies
            shows = showlist
            for show in shows:
                for val in shows[show]:
                    # [' 12:00', <BookingForm bound=False, valid=Unknown, fields=(theater_relid)>]
                    print(val)
            check = True
    else:
        form = SearchForm()
    return render(request, 'searchpage.html', {'location': cityid, 'form': form, 'movie': movieid, 'datestring': datestring,
                                               'shows': shows, 'url': url, 'check': check, 'form2': form2})


@login_required(login_url='login')
def BookingPage(request):
    theaterrelid = " "
    rows = ['A', 'B', 'C', 'D', 'E']
    seats = ['1', '2', '3', '4', '5', '6', '', '7', '8', '9', '10', '11', '12']
    colspan = 15
    bookedseats = []
    form2 = SeatsForm2(initial={'theater_relid': theaterrelid})
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            theaterrelid = form.cleaned_data['theater_relid']
            form2 = SeatsForm2(initial={'theater_relid': theaterrelid})
            confirm = "confirmed"
            bookedseats = user_seats.objects.select_related('theater_seats_id').filter(
                theater_seats_id__theater_movies_id=theaterrelid, status=confirm).values_list('theater_seats_id__seat_no', flat=True)
    return render(request, 'bookingsuccess.html', {'theaterrelid': theaterrelid, 'rows': rows, 'seats': seats,
                                                   'colspan': colspan, 'form': form2, 'bookedseats': bookedseats})


@login_required(login_url='login')
def BookingSuccess(request):
    selected_seats = ""
    if request.method == 'POST':
        form = SeatsForm2(request.POST)
        print(form)
        if form.is_valid():
            selected_seats = form.cleaned_data['selected_seats']
            theater_relid = form.cleaned_data['theater_relid']
            tmp = selected_seats
            seats = tmp.split(',')[1:]
            umail = request.session.get('email')
            print(umail)
            print(seats)
            print(theater_relid)
            print("coming here")

            print(request.session)
            # get user object
            uid = request.session.get('id').first()
            # print("uid" + str(id))
            userob = User.objects.filter(id=uid)
            print(request.session.get('name'))

            # get thearter rel
            theater_rel = theater_movies_rel.objects.get(
                theater_movies_id=theater_relid)

            # populate seats
            seatobjects = []
            for seat in seats:
                try:
                    obj = theater_seats.objects.get(
                        theater_movies_id=theater_rel, seat_no=seat)
                    seatobjects.append(obj)
                except theater_seats.DoesNotExist:
                    obj = theater_seats(
                        theater_movies_id=theater_rel, seat_no=seat)
                    obj.save()
                    seatobjects.append(obj)

            # create user bookings object
            trn = user_bookings.objects.all().aggregate(Max('transaction_number'))
            trn = trn['transaction_number__max']
            if trn is None:
                trn = 0
            trn = trn + 1
            print(trn)
            trn_mode = "Online"
            price = len(seats) * theater_rel.price
            # userbookingob = user_bookings(
            #   userid=userob, transaction_number=trn, amount_paid=price, transaction_mode=trn_mode)
            # userbookingob.save()
            user_bookings.objects.create(
                userid_id=userob.id, transaction_mode=trn_mode, transaction_number=trn, amount_paid=price)
            userbookingob = user_bookings.objects.get(transaction_number=trn)

            # create the relation
            for obj in seatobjects:
                relob = user_seats(user_bookings_id=userbookingob,
                                   theater_seats_id=obj, status="confirmed")
                relob.save()

            # redirect user to my bookings page
            return HttpResponseRedirect('/mybookings/')
        else:
            print("form not valid")
    return render(request, 'bookingpage.html', {'seats': selected_seats})


@login_required(login_url='login')
def myBookings(request):
    # get user object
    id = request.session.get('id')
    userob = User.objects.get(id=id)
    print(userob)
    bookinglist = user_bookings.objects.filter(userid=userob)
    #  bookedseats = user_seats.objects.select_related('theater_seats_id').filter(
    #             theater_seats_id__theater_movies_id=theaterrelid, status=confirm).values_list('theater_seats_id__seat_no', flat=True)
    userseats = user_seats.objects.select_related('user_bookings_id')
    print(userseats.query)
    context = {'msg': "Thanks for booking with us!!",
               'name': userob.username, 'bookinglist': bookinglist}
    return render(request, 'mybookings.html', context=context)
