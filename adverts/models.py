from django.db import models
from allauth.account.signals import user_signed_up

class Signup(models.Model):
    email = models.EmailField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# def SignupCallback(sender, request, user, **kwargs):
#     userSignup, is_created = Signup.objects.get_or_create(email=email)
#     if is_created:        
#         userSignup.email = user.email         
#         userSignup.save()
# user_signed_up.connect(SignupCallback)