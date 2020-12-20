from django.contrib import admin
from django.urls import path
from Dress_Recomm_Sys import views

urlpatterns = [
path('',views.home_func,name='home_func'),
path('result',views.res,name='res')
]