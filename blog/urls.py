from django.conf.urls import url
from . import views

# This holds the URL patterns that are needed for each 
urlpatterns = [
    url(r'^$', views.post_list, name='post_list')
]
