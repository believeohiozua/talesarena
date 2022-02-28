from django.contrib import admin

from .models import Services

@admin.register(Services)
class Profile(admin.ModelAdmin):
    list_display = ('name','phone_number','email','service')
