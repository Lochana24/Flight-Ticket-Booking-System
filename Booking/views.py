from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from Booking.forms import FlightForm, TicketForm
from Booking.models import Flight, Ticket
from django.db.models import F


# Create your views here.

def home(request):
    return render(request, 'home.html', )

def signupuser(request):
    if request.method=="GET":
        return render(request, 'signupuser.html', {"form":UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                #Log in 
                login(request, user)
                return redirect('currentflights')

            except IntegrityError:
                #Username exists
                return render(request, 'signupuser.html', {"form":UserCreationForm(),"error":" That username alreasy exists. Please choose another username."})

        else:
            #Passwords did not match 
            return render(request, 'signupuser.html', {"form":UserCreationForm(),"error":"Passwords did not match."})

def loginuser(request):
    if request.method=="GET":
        return render(request, 'loginuser.html', {"form":AuthenticationForm()})
    else:
        user= authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {"form":AuthenticationForm(), "error":"Username and password did not match."})
        else:
            login(request, user)
            return redirect('currentflights')

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')


@staff_member_required
def createflight(request):
    if request.method=="GET":
        return render(request, 'admin/addflight.html', {"form":FlightForm()})
    else:
        try:
            form=FlightForm(request.POST)
            flight=form.save(commit=False)
            flight.exists=1
            flight.save()
            return redirect('currentflights')
        except ValueError:
            return render(request, 'admin/addflight.html', {"form":FlightForm(), 'error':'Bad data passed in. Try again.'})

@staff_member_required
def deleteflight(request, pk):
    flight=get_object_or_404(Flight, pk=pk,)
    if request.method=="POST":
        flight.delete()
        return redirect('currentflights')

@login_required
def currentflights(request):
    flights=Flight.objects.filter(deleted=0).order_by('date')
    if request.user.is_superuser:
       return render(request, 'admin/currentflights.html', {"flights":flights} )
    return render(request, 'currentflights.html', {"flights":flights, "searchdate":0, "searchtime":0} )

@login_required
def searchflights(request,flag):
    flights=Flight.objects.filter(date=F('searchdate'),deleted=0).order_by('date')
    if request.user.is_superuser:
       return render(request, 'admin/currentflights.html', {"flights":flights} )
    return render(request, 'currentflights.html', {"flights":flights} )

@staff_member_required
def deleteflight(request, pk):
    flight=get_object_or_404(Flight, pk=pk)
    tickets=Ticket.objects.filter(deleted=0, flight=flight)
    for ticket in tickets:
        ticket.deleted=1
        ticket.delete()
    flight.deleted=1
    if request.method=="POST":
        flight.delete()
        return redirect('currentflights')

@login_required
def viewflight(request, pk):
    flight=get_object_or_404(Flight, pk=pk)
    if request.method=="GET":
        form=FlightForm(instance=flight)
        if request.user.is_superuser:
            return render(request, 'admin/viewflight.html', {"flight":flight,"form":form} )
        return render(request, 'viewflight.html', {"flight":flight,"form":form} )
    else:
        try:
            form=FlightForm(request.POST, instance=flight)
            form.save()
            return redirect('currentflights')
        except ValueError:
            if request.user.is_superuser:
                return render(request, 'admin/viewflight.html', {"flight":flight,"form":form,"error":"Bad information. Try again."} )
            return render(request, 'viewflight.html', {"flight":flight,"form":form,"error":"Bad information. Try again."} )

@login_required
def bookticket(request, pk):
    flight=get_object_or_404(Flight, pk=pk)     
    if request.method=="GET":
        return render(request, 'bookticket.html', {"flight":flight,"form":TicketForm()})
    else:
        try:
            form=TicketForm(request.POST)
            ticket=form.save(commit=False)
            ticket.user=request.user
            flight.available-=1
            flight.booked+=1
            ticket.flight=flight
            ticket.save()
            flight.save()
            return redirect('mytickets')
        except ValueError:
            return render(request, 'bookticket.html', {"flight":flight,"form":TicketForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def cancelticket(request, pk):
    ticket=get_object_or_404(Ticket, pk=pk)
    ticket.deleted=1
    if request.method=="POST":
        flight=ticket.flight
        flight.available+=1
        flight.booked-=1
        flight.save()
        ticket.delete()
        return redirect('mytickets')

@login_required
def mytickets(request):
    tickets=Ticket.objects.filter(user=request.user, deleted=0).order_by('date')
    return render(request, 'mytickets.html', {"tickets":tickets} )

@staff_member_required
def alltickets(request):
    tickets=Ticket.objects.filter(deleted=0).order_by('date')
    return render(request, 'admin/alltickets.html', {"tickets":tickets} )

@login_required
def viewticket(request, pk):
    ticket=get_object_or_404(Ticket, pk=pk)
    if request.method=="GET":
        form=TicketForm(instance=ticket)
        if request.user.is_superuser:
            return render(request, 'admin/viewticket.html', {"ticket":ticket,"form":form} )
        return render(request, 'viewticket.html', {"ticket":ticket,"form":form} )
    else:
        try:
            form=TicketForm(request.POST, instance=ticket)
            form.save()
            if request.user.is_superuser:
                return redirect('alltickets')
            return redirect('mytickets')
        except ValueError:
            if request.user.is_superuser:
                return render(request, 'admin/viewticket.html', {"ticket":ticket,"form":form,"error":"Bad information. Try again."} )
            return render(request, 'viewticket.html', {"ticket":ticket,"form":form,"error":"Bad information. Try again."} )
