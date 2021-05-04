from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import article_list

urlpatterns = [
    path('article', article_list),
]