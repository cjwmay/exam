from django.conf.urls import url
from . import views           # So we can call functions from our routes!
urlpatterns = [
	url(r'^main$', views.index),
    url(r'^checkregister$', views.checkregister),
    url(r'^checklogin$', views.checklogin),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.success),
    url(r'^add$', views.add),
    url(r'^addcheck$', views.addcheck),
    url(r'^travels/destination/(?P<id>\d+)$', views.tripbyid, name = "tripbyid"),
    url(r'^join$', views.join),
]
