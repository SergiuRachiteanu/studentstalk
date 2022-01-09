from django.contrib import admin
from .models import Channel, Editinfo, Message, Student, Subchannel

admin.site.register(Student)
admin.site.register(Channel)
admin.site.register(Subchannel)
admin.site.register(Message)
admin.site.register(Editinfo)
