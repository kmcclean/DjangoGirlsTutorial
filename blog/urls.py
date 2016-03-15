from django.conf.urls import url
from . import views

# This holds the URL patterns that are needed for each
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
]
