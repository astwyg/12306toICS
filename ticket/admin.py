from django.contrib import admin

# Register your models here.
from .models import Ticket

admin.site.register(Ticket)