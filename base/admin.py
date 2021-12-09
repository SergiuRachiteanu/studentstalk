from django.contrib import admin
from .models import Channel, Message, Student, Subchannel

admin.site.register(Student)
admin.site.register(Channel)
admin.site.register(Subchannel)
admin.site.register(Message)
