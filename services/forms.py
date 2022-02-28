from django import forms
import datetime
from .models import Services

#Multiple choice
LANGUAGE_CHOICE = [
    
    ('english', 'English'),
    ('chinese_(Simplified)', 'Chinese (Simplified)'),
    ('czech', 'Czech'),   
    ('french', 'French'),
	('german', 'German'),
    ('japanese', 'Japanese'),
	('portuguese', 'Portuguese'),
    ('slovak', 'Slovak'),
	('spanish', 'Spanish'),
    ]


class URLInput(forms.TextInput):
    input_type = 'url'


#entry for the web link    
class web_page_summary_form(forms.Form): 
    SUMMARIZE = forms.URLField(required = True, label='Enter a Valid Url:',  widget=URLInput(attrs={'placeholder': 'https://www.example.com/????',}))
    LANGUAGE = forms.CharField(required = True, label='choose language', widget=forms.Select(choices=LANGUAGE_CHOICE))
    SENTENCES_COUNT = forms.IntegerField(required = True, initial=1, min_value = 1, help_text = '',  label='sentence count',) 


class text_summary_form(forms.Form): 
    Text_field =  forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":100
    }),
     required = True, help_text = "",
      label='Enter text here')
    Lang = forms.CharField(required = True, label='choose language', widget=forms.Select(choices=LANGUAGE_CHOICE))
    s_counts = forms.IntegerField(required = True, min_value = 1, help_text = '', initial=1,  label='sentence count',)


class contactForm(forms.Form):
    name = forms.CharField(required = False, max_length=20, help_text = '')
    email = forms.EmailField(required = True)
    comment = forms.CharField(required = True, label='Message', widget = forms.Textarea) 


SERVICE_CHOICE = [
    ('Project_writing_(thesis)', 'Research/project work (thesis)'),
    ('Data_Analysis', 'Data Analysis'),    
    ('Content_Management', 'Content Management'),
    ('Web_Development', 'Web Development'),
       ('Others', 'Others'),
    ]




class ServicesForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "email address",
    }), label="")

    service = forms.CharField(required = True,
     label='which of our services do you require?',    
    widget=forms.Select(choices=SERVICE_CHOICE))



    class Meta:
        model = Services
        fields = '__all__'