from tinymce import HTMLField
from django.db import models
from allauth.account.signals import user_signed_up
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
from django_resized import ResizedImageField
from djangoeditorwidgets.fields import XMLField

class PostView(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Post', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

Gender_CHOICE = [   
        ('Male', 'Male'),
        ('Female', 'Female'),    
        ]
 
class Profile(models.Model):   
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)   
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    Gender = models.CharField(max_length=10, choices=Gender_CHOICE, help_text='Gender', blank=True, null=True)
    Birthday = models.DateField(blank=True, null=True)
    profile_photo = ResizedImageField(size=[215, 215], upload_to='profile', blank=True, null=True)   
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(help_text = 'phone number',max_length=20, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter= models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)     

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={
            'pk': self.pk
        })

    def __str__(self): 
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category

def ProfileCallback(sender, request, user, **kwargs):
    userProfile, is_created = Profile.objects.get_or_create(user=user)
    if is_created:
        # userProfile.user = user.username
        userProfile.first_name = user.first_name
        userProfile.last_name = user.last_name        
        
        # userProfile.Birthday = user.Birthday
        # userProfile.phone_number = user.phone_number 
        userProfile.save()
user_signed_up.connect(ProfileCallback)



class Post_Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)
    # image = models.CharField(max_length=100000000)
    image = models.ImageField(default='')
    link = models.CharField(max_length=100, default="'profile/'+request.user", blank=True, null=True)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)    

    def __str__(self):
        return self.user.username

class Postsum(models.Model):
    pass 
  
    

class Post(models.Model): 
    title = models.CharField(max_length=100)   
    timestamp = models.DateTimeField(auto_now_add=True)
    overview = models.TextField()
    content = HTMLField(blank=True, null=True)   #or XMLField()    
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    thumbnail = ResizedImageField(size=[820, 420], upload_to='post', blank=True, null=True, force_format='PNG')
    categories = models.ManyToManyField(Category, blank=True)
    other_categories = models.CharField(max_length=50, blank=True, null=True)
    publish = models.BooleanField( default = False)
    likes = models.ManyToManyField(User, related_name='likes', blank= True)  
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        app_label = 'tales'
    def get_cropping_as_list(self):
        if self.cropping:
            return list(map(int, self.cropping.split(',')))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })
   
    def __str__(self):
        return self.title

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Post_Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def total_likes(self):
        return self.likes.count()

   



    



   
