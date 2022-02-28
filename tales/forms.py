from django import forms
from tinymce import TinyMCE
import datetime
from .models import Post, Post_Comment, Profile, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from allauth.account.forms import SignupForm
from django.forms import CheckboxInput, HiddenInput
from djangoeditorwidgets.widgets import TinymceWidget


def get_author(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None
def author(request): 
    author = get_author(request.user)   
    return author

Gender_CHOICE = [   
        ('Male', 'Male'),
        ('Female', 'Female'),    
        ]


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput({'placeholder':'First Name','class':'form-class'}))    
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput({'placeholder':'Last Name','class':'form-class'}))    
    # Gender = forms.CharField(required = True, label='Gender', widget=forms.Select(choices=Gender_CHOICE))
    # Birthday = forms.DateField(label='Birthday', widget=forms.SelectDateWidget)
    # Phone_number = forms.IntegerField(required = True, help_text = '',  label='Phone') 
    class Meta:
        model = User 
        fields = '__all__'
    def signup(self, request, user): 
        # user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']      
        user.last_name = self.cleaned_data['last_name']
        # user.Gender = self.cleaned_data['Gender']
        # user.Birthday = self.cleaned_data['Birthday']
        # user.Phone_number = self.cleaned_data['Phone_number']       
        user.save()
        return user


class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self,email):
        RestrictedList = [' ']
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.')
        return email

class URLInput(forms.TextInput):
    input_type = 'url'

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=50, widget=forms.TextInput({
                                                                    'placeholder':'your title',
                                                                    'class' : 'form-control',
                                                                    'maxlength':"50",
                                                                    
                                                                                }))
    overview = forms.CharField(required=True, min_length=750, help_text = 'min-Words:750',
                                                         label="Inspire The World!", 
                                                         widget=forms.Textarea(attrs={
                                                            'class': 'form-control',
                                                            # 'placeholder': 'Your Content',
                                                            'id': '',                                                   
                                                            'border': '2px solid #750a20',
                                                            'cols': 50,
                                                            'rows': 10                                                           
                                                        }))
    # content = forms.CharField(required=False, help_text ='Media Content', label="Get Unique Go Dynamic! ",
    #     widget=TinymceWidget(
    #         attrs={'class': 'form-control', 'cols': 50,'rows': 10 }
    #     )
    # )  
    content = forms.CharField(required=False,
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    other_categories =  forms.CharField(max_length=50, required=False,
                                        widget=forms.TextInput({'placeholder':'Add Here, If Your Category is not Listed',
                                                                'class':"form-control",
                                                                 'id':"id_other_categories" 
                                        }))
    # categories = forms.CharField(required = True, label='choose language', widget=forms.Select(choices=Cat_Choice))
    thumbnail = forms.ImageField(required=False, label='Caption Your Content')
    publish =  forms.BooleanField(label='',
                                widget=forms.CheckboxInput(attrs={'class': 'hidden',
                                                                'value': False}), 
                                required=False, 
                                initial=False
                            )

    class Meta:
        model = Post
        fields = ('author','title', 'overview', 'content', 'thumbnail', 
        'categories', 'publish')
        widgets = {
            'content': TinymceWidget()
        }
    

        

        
class CatForm(forms.ModelForm):
    category = forms.CharField(max_length=100, label="Other categories", widget=forms.TextInput({'placeholder':'If Category is not listed'}))
    class Meta:
        model = Category
        fields = ('category',)



class CommentForm(forms.ModelForm):  
    content = forms.CharField( label="Say Something", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
        'border': '2px solid #750a20'

    }))
    class Meta:
        model = Post_Comment
        fields = ('content', )
  

        
        
        
     
 
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label='username', widget=forms.TextInput({'placeholder':'UserName','class': 'form-control'})) 
    email = forms.EmailField( widget=forms.EmailInput({'placeholder':'E-Mail','class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']


Gender_CHOICE = [   
        ('Gender', 'Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),    
        ]
from django.forms import ModelForm, DateInput

class DatePickerForm(DateInput):
    input_type = 'date'

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="first_name", widget=forms.TextInput({'placeholder':'first_name','class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label="last_name", widget=forms.TextInput({'placeholder':'last_name','class': 'form-control'}))
    Gender = forms.CharField(label='Gender', widget=forms.Select(choices=Gender_CHOICE))
    Birthday =  forms.DateField(required = False, label='Birthday',
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'class': 'form-control vDateField', 'type':'Date'}),
        input_formats=['%Y-%m-%d',]
        ) 
   
    bio = forms.CharField(required = False, help_text = 'Tell us SomeThing about YourSelf. (word limit <300', widget=forms.Textarea(attrs={                                                                                          
                                                                                            'class': 'form-control',
                                                                                            'placeholder': 'Your Bio',
                                                                                            'id': 'id_bio',                                                   
                                                                                            'border': '2px solid #750a20',
                                                                                            'cols': 50,
                                                                                            'rows': 10  
                                                                                             }))
    phone_number = forms.IntegerField(required =True,  help_text = "Whatsapp",  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    facebook = forms.URLField(required = False,  help_text = "", widget=URLInput(attrs={'placeholder': 'https://www.facebook.com/your-facebook-id','class': 'form-control'}))
    twitter = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.twitter.com/your-twitter-id','class': 'form-control'}))
    instagram = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.instagram.com/your-instagram-id','class': 'form-control'}))
    linkedin = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.linkedin.com/your-linkedin-id','class': 'form-control'}))
    
 
   

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','Gender', 'Birthday', 
                  'bio', 'profile_photo',  'phone_number',
                  'linkedin','facebook','twitter','instagram']
        
class ProfileUpdateForm(forms.ModelForm):
    pass
    # first_name = forms.CharField(max_length=100, label="Full Names", widget=forms.TextInput({'placeholder':'Full Names'}))
    # last_name = forms.CharField(max_length=100, label="Full Names", widget=forms.TextInput({'placeholder':'Full Names'}))    
    # bio = forms.CharField(help_text = 'Tell us Some about You.', max_length=300, widget=forms.Textarea)
    # facebook = forms.URLField(required = False,  help_text = "", widget=URLInput(attrs={'placeholder': 'https://www.facebook.com/your-facebook-id',}))
    # twitter = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.twitter.com/your-twitter-id',}))
    # instagram = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.instagram.com/your-instagram-id',}))
    # linkedin = forms.URLField(required = False,  help_text = "",  widget=URLInput(attrs={'placeholder': 'https://www.linkedin.com/your-linkedin-id',}))
    
    # class Meta:
    #     model = Profile
    #     fields = ['first_name', 
    #               'bio', 'profile_photo',  'phone_number',
    #               'linkedin','facebook','twitter','instagram']
        






 


