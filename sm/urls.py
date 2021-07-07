from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name="home"),
    path('instamate/',views.get_insta,name="get_insta"),
    path('download/<str:url>',views.download,name="download"),
]