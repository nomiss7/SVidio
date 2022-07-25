# Generated by Django 4.0.6 on 2022-07-21 10:44

from django.db import migrations
from apps.blog.models import BlogCategory


def add_blog_categories(apps, schema_editor):
    categories = [
        'Новости',
        'Акции',
        'Партнерам',
        'Обзоры',
        'Специальные предложения',
    ]
    for category in categories:
        BlogCategory.objects.create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_tag_tags_article_tags'),
    ]

    operations = [
        migrations.RunPython(add_blog_categories)
    ]
