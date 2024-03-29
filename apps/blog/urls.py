from django.urls import path
from apps.blog import views

urlpatterns = [
    path('', views.blog_category_list, name='blog_category_list'),
    path('<int:category_id>/', views.article_list, name='article_list'),
    path('<int:category_id>/<int:article_id>', views.article_view, name='article_view'),
    path('<int:category_id>/<int:article_id>/<int:tag_id>', views.tag_article_list, name='tag_article_list'),
]
