from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Category, Post, Post_Comment, PostView






admin.site.register(Category)
admin.site.register(Post_Comment)
admin.site.register(PostView)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django.conf import settings
# we are going send a message to the author when ever the post is publshed 
@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title', 'author','publish',  'previous_post', 'next_post', 'timestamp', 'other_categories')
    list_filter = ('categories', 'likes')


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user','first_name','phone_number')







