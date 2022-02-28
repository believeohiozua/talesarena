from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from services.views import Contact, Summary, Services, About
from adverts.views import email_list_signup
from tales.views import (PostListView, PostDetailView, PostCreateView,PostUpdateView, ProfileCreateView, 
                     IndexView, ProfileDetailView,ProfileUpdatelView, ProfileDeleteView, Search, PostDeleteView, 
							like_post, CatSearch, update_profile
							# homePage,
                            )





urlpatterns = [
    url(r'^', include('favicon.urls')),
	path('', IndexView.as_view(), name='home'),
    #path('', homePage, name='home'),
    path('createpost/', PostCreateView.as_view(), name='post-create'),     
    path('post/', PostListView.as_view(), name='post-list'),     
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('victory101/', admin.site.urls),
   
        
]

urlpatterns += [   
    path('profile/<pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<pk>/delete/', ProfileDeleteView.as_view(), name = 'delete-profile'),   
    # path('profile/<pk>/update/',ProfileUpdatelView.as_view(), name = 'update-profile'),   
    path('profile/<pk>/update/', update_profile, name = 'update-profile'),   
]

urlpatterns += [
    url(r'^like/$', like_post, name ="like_post"),
   

]

urlpatterns += [
    path('search/', Search.as_view(), name = 'search'),
    path('catsearch/', CatSearch.as_view(), name = 'catsearch'),
]


urlpatterns += [    
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('summarizer/', Summary, name='summarizer'),
    path('services/',Services, name='services'),
   
]



urlpatterns += [
	path('email-signup/',email_list_signup, name='email-list-signup'),
]


urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
    # url(r'^admin/filebrowser/', include(site.urls)),
]


urlpatterns += [
    path('accounts/', include('allauth.urls')),
    path('account/', include('allauth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace="social")),
]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

from django.views.static import serve
urlpatterns += [
url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]