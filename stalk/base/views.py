from django.contrib.messages.api import MessageFailure
from django.shortcuts import render,redirect
from django.http import HttpResponse
import mysql.connector
from operator import itemgetter
from django.contrib.auth.models import User
from .models import Channel, Editinfo, Message, Student, Subchannel
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
import time
from hashlib import sha256
from django.contrib.auth.decorators import login_required


#testare afisare dictionar in template.

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
    for subcanal in subcanale:
        dictionar.update({subcanal.id:subcanal.name})

    #generare subcanale
    rooms = [
        {'id' : 1, 'facultate' : nume_facultate, 'name' : 'Socializare'},
        {'id' : 2, 'facultate' : nume_facultate, 'name' : 'Nelamuriri'},
        {'id' : 3, 'facultate' : nume_facultate, 'name' : 'Teme/Proiecte'},
        {'id' : 4, 'facultate' : nume_facultate, 'name' : 'Examene'}
    ]

    return render(request, 'main.html', {'facultate' : nume_complet,
                                         'rooms' : rooms})

def logoutView(request):
    logout(request)
    return redirect('/')

@login_required
def edit(request):
    if request.method == "POST":
        nume = request.user.username
        changereason = request.POST.get('reason')
        facultate = request.POST.get('facultyselected')

        newrequest = Editinfo()
        newrequest.username = nume
        newrequest.reason = changereason
        newrequest.newfaculty = facultate

        newrequest.save()
        time.sleep(2)
        return redirect('main')

    return render(request, 'edit.html')

@login_required
def chat(request, pk):
    facultate = request.user.student.facultate
    nume_facultate = Channel.objects.filter(name=facultate).get()
    nume_complet = nume_facultate.completename
    rooms = [
        {'id' : 1, 'facultate' : nume_complet, 'name' : 'Socializare'},
        {'id' : 2, 'facultate' : nume_complet, 'name' : 'Nelamuriri'},
        {'id' : 3, 'facultate' : nume_complet, 'name' : 'Teme/Proiecte'},
        {'id' : 4, 'facultate' : nume_complet, 'name' : 'Examene'}
    ]
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i

    subcanal = Subchannel.objects.filter(scowner_id=nume_facultate.id).filter(name=rooms[int(pk) - 1]['name']).get()
    #studentid = Student.objects.filter(name=request.user.username).get()

    mess = Message.objects.filter(msgowner_id=subcanal.id)
    mesaje = []
    for el in mess:
        dic = dict()
        user = Student.objects.get(id=el.msguser_id)
        dic['name'] = user.name
        dic['message'] = el.msg
        dic['date'] = el.created
        mesaje.append(dic) 

    context = {'room' : room, 
               'subcanal' : subcanal,
               'mesaje' : mesaje
               }

    if request.method == "POST":
        message = request.POST.get('sendtext')
        new_message = Message()
        new_message.msguser = Student.objects.filter(name=request.user.username).get()
        new_message.msgowner = Subchannel.objects.filter(scowner_id=nume_facultate.id).filter(name=rooms[int(pk) - 1]['name']).get()
        new_message.msg = message
        new_message.save()

        return redirect('chat', pk)
    
    #print(rooms[int(pk) - 1]['name'])
    return render(request, 'chat.html', context)
