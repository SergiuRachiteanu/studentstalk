from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    facultate = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Channel(models.Model):
    name = models.CharField(max_length=10)
    completename = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subchannel(models.Model):
    scowner = models.ForeignKey(Channel, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Message(models.Model):
    msguser = models.ForeignKey(Student, on_delete=models.CASCADE)
    msgowner = models.ForeignKey(Subchannel, on_delete=models.CASCADE)
    msg = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.msguser)
