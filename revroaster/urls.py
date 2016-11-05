from django.conf.urls import url
from . import views
from .views import BotView

urlpatterns= [
	url(r'^$',views.home,name='rev'),
	url(r'^searchurl/$', views.home, name='url'),
    url(r'^ca1b63d49f4e2f1547d15af7c3d8294b6d3d1ae4006916c62c/$',BotView.as_view())
]
