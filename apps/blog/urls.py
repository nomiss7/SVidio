from django.urls import path
from apps.blog import views


urlpatterns =[
    path('', views.blog_category_list,name='views.blog_category_list')
]