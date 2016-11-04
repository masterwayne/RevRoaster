from django.conf.urls import url
from . import views

urlpatterns= [
	url(r'^$',views.home,name='rev'),
	url(r'^searchurl/$', views.home, name='url'),

]
