from django.shortcuts import render
from django.urls import reverse

from apps.blog.forms import CommentForm
from apps.blog.models import BlogCategory, Article, Tag, Comment
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
    comments = Comment.objects.filter(comment_article=article.id, is_checked=True)
    breadcrumbs = {reverse('blog_category_list'): PAGE_NAMES['blog']}
    breadcrumbs.update({reverse('article_list', args=[category.id]): category.name})
    breadcrumbs.update({'current': article.name})
    error = None
    user = request.user
    if request.method == 'POST':
        data = request.POST.copy()
        if user.is_authenticated:
            data.update(name=user.username, email=user.email)
        request.POST = data
        form = CommentForm(request.POST)
        error = form.errors
        if form.is_valid():
            comment = form.save(commit=False)
            csrf = request.session.get('comm_token')
            if not csrf or csrf != data.get('csrfmiddlewaretoken'):
                if user.is_authenticated:
                    comment.is_checked = True
                else:
                    comment.is_checked = False
                comment.comment_article = article
                comment.save()
                breadcrumbs = {reverse('blog_category_list'): PAGE_NAMES['blog']}
                breadcrumbs.update({reverse('article_list', args=[category.id]): category.name})
                breadcrumbs.update({reverse('article_view', args=[category.id, article.id]): article.name})
                breadcrumbs.update({'current': 'Комментарий опубликован'})
                request.session['comm_token'] = data.get('csrfmiddlewaretoken')
            return render(request, 'blog/comment/created_comment.html', {'breadcrumbs': breadcrumbs,
                                                                         'category_id': category_id,
                                                                         'article_id': article_id, })
    else:
        form = CommentForm()
    return render(request, 'blog/article/view.html', {'article': article, 'category': category, 'comments': comments,
                                                      'breadcrumbs': breadcrumbs, 'form': form, 'error': error,
                                                      'user': user})


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
