from django.conf.urls import url
from . import views

urlpatterns = [
               #url(r'^$', views.index, name='index')
               url(r'^$', views.IndexView.as_view(), name='index'),
                url(r'^about/$', views.AboutView.as_view(), name='about'),
                url(r'^generate/$', views.generate_story, name='generate'),
               ]
