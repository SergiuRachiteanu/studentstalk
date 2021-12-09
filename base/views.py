from django.contrib.messages.api import MessageFailure
from django.shortcuts import render,redirect
from django.http import HttpResponse
import mysql.connector
from operator import itemgetter
from django.contrib.auth.models import User
from .models import Channel, Student, Subchannel
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
import time
from hashlib import sha256
from django.contrib.auth.decorators import login_required


#testare afisare dictionar in template.
rooms = [
    {'id' : 1, 'name' : 'FMI'},
    {'id' : 2, 'name' : 'CBG'}
]

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        facultate = request.POST.get('facultate')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('register')


        createNewUser = User.objects.create_user(
            username = username ,
            email = email ,
            password = password ,
            #facultate = facultate ,
        )
        createNewUser.save()

        student = Student()
        student.name = username
        student.email = email
        student.facultate = facultate
        student.save()
        return redirect('login')

    return render(request, 'register.html')
        
def login(request):

    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        authUser = authenticate(
            request,
            username = username,
            password = password
        )
        if authUser is not None:
            auth_login(request, authUser)
            return redirect('main')
        else:
             messages.error(request, 'Invalid Credentials!')
               
    return render(request, 'login.html')

@login_required
def main(request):
    #afisare nume facultate in template
    facultate = request.user.student.facultate
    nume_facultate = Channel.objects.filter(name=facultate).get()
    nume_complet = nume_facultate.completename

    #afisare subcanale in template
    subcanale = Subchannel.objects.filter(scowner=nume_facultate.id)
    dictionar = dict()
    list = []
    for subcanal in subcanale:
        dictionar.update({subcanal.id:subcanal.name})


    context = [{'facultate' : nume_complet, 'subcanale' : dictionar}]
    return render(request, 'main.html', {'context' : context})

def logoutView(request):
    logout(request)
    return redirect('/')

@login_required
def chat(request):
    return render(request, 'chat.html')