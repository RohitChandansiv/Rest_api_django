from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [

    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_details, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/edit/<int:pk>', views.post_edit, name='post_edit'),
    # api views
    path('api/', views.api_post_list, name='api_post_list'),
    path('api/post/<int:pk>/', views.api_post_detail, name='api_post_detail'),
]
