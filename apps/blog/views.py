from django.shortcuts import render
from django.urls import reverse

from apps.blog.models import BlogCategory, Article, Tag
from config.settings import PAGE_NAMES


def blog_category_list(request):
    blog_categories = BlogCategory.objects.all()
    breadcrumbs = {'current': PAGE_NAMES['blog']}
    return render(request, 'blog/category/list.html', {'categories': blog_categories, 'breadcrumbs': breadcrumbs})


def article_list(request, category_id):
    articles = Article.objects.filter(category=category_id)
    category = BlogCategory.objects.get(id=category_id)
    breadcrumbs = {reverse('blog_category_list'): PAGE_NAMES['blog']}
    breadcrumbs.update({'current': category.name})
    return render(request, 'blog/article/list.html', {'articles': articles, 'category': category,
                                                      'breadcrumbs': breadcrumbs})


def article_view(request, category_id, article_id):
    article = Article.objects.get(id=article_id)
    category = BlogCategory.objects.get(id=category_id)
    breadcrumbs = {reverse('blog_category_list'): PAGE_NAMES['blog']}
    breadcrumbs.update({reverse('article_list', args=[category.id]): category.name})
    breadcrumbs.update({'current': article.name})
    return render(request, 'blog/article/view.html', {'article': article, 'category': category,
                                                      'breadcrumbs': breadcrumbs})


def tag_article_list(request, category_id, article_id, tag_id):
    category = BlogCategory.objects.get(id=category_id)
    article = Article.objects.get(id=article_id)
    articles = Article.objects.filter(tags=tag_id)
    tag = Tag.objects.get(id=tag_id)
    breadcrumbs = {reverse('blog_category_list'): PAGE_NAMES['blog']}
    breadcrumbs.update({reverse('article_list', args=[category.id]): category.name})
    breadcrumbs.update({'current': tag.name})
    return render(request, 'blog/article/tag_article_list.html', {'articles': articles, 'tag': tag,
                                                                  'breadcrumbs': breadcrumbs})

# Create your views here.
