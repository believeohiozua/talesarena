from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import MultipleObjectMixin
from django.template.loader import render_to_string
from django.views import generic
from .forms import (CommentForm, PostForm,ProfileForm,
                             UserUpdateForm, ProfileUpdateForm, CatForm
                            )
 
from .models import PostView, Profile, Post_Comment, Post, Category
from django.contrib.auth import get_user_model
User = get_user_model()
import random
from adverts.forms import EmailSignupForm
from adverts.models import Signup
##############---SUMMARIZER---#####################
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
#############################################
 



def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__category') \
        .annotate(Count('categories__category'))
    return queryset


# def homePage(request):
#     publish = Post.objects.filter(publish=True).order_by('-timestamp')[0:3]    
#     most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
#     category_count = get_category_count()   
#     most_recent = Post.objects.order_by('-timestamp') 
#     counts = []
#     for count in category_count:
#         counts.append(count)
#     category_count = random.choices(category_count, k=20)
 
#     if request.method == "POST":        
#             email = request.POST["email"]
#             new_signup = Signup()
#             new_signup.email = email
#             new_signup.save()

#     context = {
#             'object_list': publish,
#             'most_popular': most_popular,
#             'category_count': category_count,
#             'most_recent': most_recent,
             
#      }
#     template = 'index.html'
#     return render(request, template, context)

class IndexView(View):
    form = EmailSignupForm()    
    def get(self, request, *args, **kwargs):
        publish = Post.objects.filter(publish=True).order_by('-timestamp')[0:3]
        most_popular =  Post.objects.annotate(like_count=Count('likes') + Count('comments')).order_by('-like_count') 
        category_count = get_category_count()   
        most_recent = Post.objects.order_by('-timestamp') 
        counts = []
        for count in category_count:
            counts.append(count)            
        category_count = random.choices(category_count, k=36)

        
            
        context = {
            'object_list': publish,
            'most_popular': most_popular,
            'category_count': category_count,
            'most_recent': most_recent,
            'form': self.form,
            
           
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")

# class CatSearch(generic.ListView):
#     model = Post    
#     paginate_by = 4
#     template_name = 'catsearch.html'
#     def get_context_data(self, **kwargs):
#         publish = Post.objects.filter(publish=True).order_by('-timestamp')[0:3]       
#         most_popularSum = Post.objects.annotate(Post_Comment=Count('comments')).count()
#         most_popularSum1 = Post.objects.annotate(like_count=Count('likes')).count()
#         sum =  most_popularSum1 + most_popularSum1
#         most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-comments') 
#         category_count = get_category_count()   
#         most_recent = Post.objects.order_by('-timestamp') 
#         counts = []
#         for count in category_count:
#             counts.append(count)
#         category_count = random.choices(category_count, k=36)
#         cat_queryset = Post.objects.all()
#         cat_query = self.request.GET.get('cat')
#         if cat_query:
#             cat_queryset = cat_queryset.filter(
#                 Q(categories__category__icontains=cat_query) |
#                 Q(content__icontains=cat_query) 
                    
#             ).distinct()         

#         context = super().get_context_data(**kwargs)
#         context['cat_queryset'] = cat_queryset       
#         context['cat_query'] = cat_query 
#         context['object_list'] = publish 
#         context['most_popular'] = most_popular      
#         context['category_count'] = category_count 
#         context['most_recent'] = most_recent   
        
#         return context

        
class CatSearch(View):
    model = Post
    template_name = 'catsearch.html'
    paginate_by = 4
    def get(self, request, *args, **kwargs):
        publish = Post.objects.filter(publish=True).order_by('-timestamp')[0:3]           
        most_popular =  Post.objects.annotate(like_count=Count('likes') + Count('comments')).order_by('-like_count') 
        # most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        category_count = get_category_count()   
        most_recent = Post.objects.order_by('-timestamp') 
        counts = []
        for count in category_count:
            counts.append(count)
        category_count = random.choices(category_count, k=36)
        cat_queryset = Post.objects.all()
        cat_query = request.GET.get('cat')
        if cat_query:
            cat_queryset = cat_queryset.filter(
                Q(categories__category__icontains=cat_query) |
                Q(content__icontains=cat_query) 
                    
            ).distinct()

        # numbers_list = range(1, 1000)
        page = request.GET.get('page', 1)
        paginator = Paginator(cat_queryset, 4)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)

        context = {
            'cat_queryset': cat_queryset,
            'cat_query': cat_query,
            'object_list': publish,
            'most_popular': most_popular,
            'category_count': category_count,
            'most_recent': most_recent,
            'numbers': numbers,
        }
        return render(request, 'catsearch.html', context)   
    
        
class Search(View):
    paginate_by = 4
    def get(self, request, *args, **kwargs):
        publish = Post.objects.filter(publish=True).order_by('-timestamp')[0:3]       
        most_popularSum = Post.objects.annotate(Post_Comment=Count('comments')).count()
        most_popularSum1 = Post.objects.annotate(like_count=Count('likes')).count()
        sum =  most_popularSum1 + most_popularSum1
        most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-comments') 
        category_count = get_category_count()   
        most_recent = Post.objects.order_by('-timestamp') 
        counts = []
        for count in category_count:
            counts.append(count)
        category_count = random.choices(category_count, k=20)
        cat_queryset = Post.objects.all()
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) 
                    
            ).distinct()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 4)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)

        context = {
            'queryset': queryset,
            'query': query,
            'object_list': publish,
            'most_popular': most_popular,
            'category_count': category_count,
            'most_recent': most_recent,
             'numbers': numbers,
        }
        return render(request, 'search_results.html', context)


class PostListView(generic.ListView):   
    model = Post    
    paginate_by = 4
    template_name = 'post/post_list.html'
    def get_queryset(self):
        return Post.objects.filter(publish=True).order_by('-timestamp')

    def get_context_data(self, **kwargs):         
        most_popular =  Post.objects.annotate(like_count=Count('likes') + Count('comments')).order_by('-like_count')       
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp') 
        counts = []
        for count in category_count:
            counts.append(count)       
        category_count = random.choices(category_count, k=20)                 
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent        
        context['category_count'] = category_count 
        context['most_popular'] = most_popular       
        
        return context



def get_author(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class PostDetailView(generic.DetailView):   
    model = Post
    context_object_name = 'post'
    template_name = 'post/post_detail.html'
    form = CommentForm()        

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj



    def get_context_data(self, **kwargs):         
        mypost = self.get_object()        
        if mypost.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        else:
            is_liked = False
        total_likes = Post.objects.filter(likes=self.request.user.id).count()
        category_count = get_category_count()
        most_recent = Post.objects.all().order_by('-timestamp')#[0:4]  
        most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count') 
        counts = []
        for count in category_count:
            counts.append(count)
        category_count = random.choices(category_count, k=20)   


        try:
            with open('postsum.txt', 'w', encoding="utf-8") as f:
                f.write(mypost.content+mypost.overview)
            text_parser = PlaintextParser.from_file('postsum.txt', Tokenizer('english'))
            text_stemmer = Stemmer('english')
            text_summarizer = Summarizer(text_stemmer)
            text_summarizer.stop_words = get_stop_words('english')           
            post_sum = text_summarizer(text_parser.document, self.request.GET['sentence_count'] )
        except:                
            post_sum = None

        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form        
        context['post_sum'] = post_sum
        context['is_liked'] = is_liked
        context['total_likes'] =total_likes 
        context['most_popular'] = most_popular       
        return context
 

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)        
        if form.is_valid():            
            post = self.get_object()           
            form.instance.user = request.user
            form.instance.post = post
            form.instance.link = 'profile/'+str(request.user.profile.pk)
            try:
                form.instance.image = request.user.profile.profile_photo 
            except:
                form.instance.image = None
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            })) 



         

def like_post(request):    
    post = get_object_or_404(Post, id=request.POST.get('id')) 
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked =False
    else:        
        post.likes.add(request.user)
        is_liked =True   
    context = {
            'post': post,
            'is_liked' : is_liked,
            
            }
    if request.is_ajax():
        html = render_to_string('base/like_section.html', context, request=request)
        return JsonResponse({'form': html})

class PostCreateView(CreateView):
    model = Post    
    form_class = PostForm   
    template_name = 'post/post_form.html'

    def get(self, request, *args, **kwargs):       
        form_class = PostForm(request.POST or None, request.FILES or None)       
        category = Category.objects.all()
        mytitle = 'Create Your Tales'
        subtitle = 'This is Your Window of Expression, The Stage is All Yours!'  
        if request.method == "POST" and form_class.is_valid():
        # if form_class.is_valid():  
            name = form.cleaned_data['author']
            title = form.cleaned_data['title']
            subject = 'New Post'
            message = '%s %s %s' %(title, ', a new post by \n', name)
            emailFrom = 'post@talesarena.com'
            emailTo = ['mytalesrena@gmail.com'] 
            send_mail(subject, message, emailFrom, emailTo,  fail_silently = True),
            mytitle = 'Thanks for Inspiring the World'
            subtitle = 'Your Post will be Reviewed And Published Within the Next 24hrs \n  if found Valid!.'
            form_class.save()
            form_class = None               

                # return redirect(reverse("post-detail", kwargs={
                # 'pk': form.instance.pk
                # }))   
        context = {  
            'profile': Profile.objects.filter(user=self.request.user.pk),   
            'form': form_class,
            'the_author': get_author(self.request.user), 
            'category': category,
            'mytitle': mytitle,
            'subtitle': subtitle,                 
            }    
        return render(request, 'post/post_form.html', context)

class PostUpdateView(UpdateView):
    model = Post    
    form_class = PostForm
    cat_form = CatForm
    template_name = 'post/post_form.html'
    def get(self, request, pk, *args, **kwargs):  
        category = Category.objects.all() 
        post = get_object_or_404(Post, pk=pk)
        form_class = PostForm(request.POST or None, request.FILES or None, instance = post)
        cat_form =  CatForm(request.POST or None) 
        mytitle = 'Post Update'
        subtitle = 'Its Great to Review Your Work for Better Results'
        if request.method == "POST" and form_class.is_valid():
            # if form_class.is_valid():  
            name = form.cleaned_data['author']
            title = form.cleaned_data['title']
            subject = 'updated Post'
            message = '%s %s %s' %(name, ', updated his post titled: \n' ,title )
            emailFrom = 'post@talesarena.com'
            emailTo = ['mytalesrena@gmail.com'] 
            send_mail(subject, message, emailFrom, emailTo,  fail_silently = True),
            mytitle = 'Thanks for Inspiring the World'
            subtitle = 'Your Post will be Reviewed And Published Within the Next 24hrs \n  if found Valid!.'
            form_class.save()
            form_class = None               
         
                # return redirect(reverse("post-detail", kwargs={
                # 'pk': form.instance.pk
                # }))   
        context = {   
                'profile': Profile.objects.filter(user=self.request.user.pk),   
                'form': form_class,
                'the_author': get_author(self.request.user), 
                'category': category,
                'mytitle': mytitle,
                'subtitle': subtitle,          
            }    
        return render(request, 'post/post_form.html', context)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = '/post'




class ProfileCreateView(CreateView):
    pass


    
class ProfileDetailView(generic.DetailView, MultipleObjectMixin):   
    model = Profile
    paginate_by =4
    template_name = 'profile/profile_detail.html'  
    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(author_id=self.get_object(),publish=True).order_by('-timestamp')# Post.objects.filter(author=self.get_object())# Post.objects.all()#self.object.get_purchases().filter()##Lecture.objects.filter(partner=self.get_object())
        context = super(ProfileDetailView,
         self).get_context_data(object_list=object_list,
          **kwargs)
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp') 
        most_popular =  Post.objects.annotate(like_count=Count('likes')).order_by('-like_count') 
        counts = []
        for count in category_count:
            counts.append(count)       
        category_count = random.choices(category_count, k=30)        
        context['most_recent'] = most_recent        
        context['category_count'] = category_count 
        context['most_popular'] = most_popular      

        return context 

class ProfileUpdatelView(UpdateView): 
    model = Profile
    # template_name = 'profile/profile_form.html'
    # form_class = ProfileForm
    # user_form = UserUpdateForm




  
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        this_user = get_object_or_404(User, pk=pk)
        form_class = ProfileForm(request.POST or None, request.FILES or None, instance = profile)
        user_form =  UserUpdateForm(request.POST or None, instance =this_user) 
        if request.method == "POST":
            if form_class.is_valid() and user_form.is_valid():
                form_class.instance.user = self.request.user                                        
                form_class.save()               
                user_form.save()
                this_user.save()                       
                return redirect(reverse("profile-detail", kwargs={
                'pk': form.instance.pk
                })) 
    
        context = {       
            'form': form_class,
            'user_form': user_form,            
            'mytitle': 'Update Your Profile',           
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'Gender': profile.Gender,
            'Birthday':profile.Birthday,
            'profile_photo': profile.profile_photo,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'linkedin': profile.linkedin,
            'facebook': profile.facebook,
            'twitter': profile.twitter,
            'instagram': profile.instagram                   
            }    
        return render(request, 'profile/profile_form.html', context)


def update_profile(request, pk):
    title ='Update Your Profile'
    profile = get_object_or_404(Profile, pk=pk)
    u_form = UserUpdateForm(request.POST or None, instance = request.user)
    p_form = ProfileForm(request.POST or None,request.FILES or None, instance = profile)    
    if request.method == "POST":
         if u_form.is_valid() and p_form.is_valid():
            p_form.instance.user = request.user
            # profile.Birthday = request.POST['Birthday_month']
            profile.save()
            u_form.save()
            p_form.save()            
            return redirect(reverse("profile-detail", kwargs={
                'pk': p_form.instance.pk
            }))     
    context = {       
        'u_form': u_form,
        'p_form': p_form,
        'title': title,
        'obj': profile

    }    
    return render(request, 'profile/create_profile.html', context)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Profile Update'
    #     context['user_form'] = self.user_form
    #     context['form_class'] = self.form_class
    #     return context  

    # def form_valid(self, form):
    #     user_form = UserUpdateForm(request.POST or None, instance = self.request.user)
    #     user_form.instance.username = self.request.user.username
    #     user_form.instance.email = self.request.user.email
    #     form.instance.user = self.request.user 
    #     user_form.save()              
    #     form.save()       
    #     return redirect(reverse("profile-detail", kwargs={
    #         'pk': form.instance.pk
    #     }))

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profile/profile_confirm_delete.html'
    success_url = '/'


  
    

    
    



