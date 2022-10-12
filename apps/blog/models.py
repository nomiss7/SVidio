from django.db import models
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill

from apps.main.mixins import MetaTagMixin
from apps.user.models import User
from config.settings import MEDIA_ROOT
from tinymce.models import HTMLField


class Tag(MetaTagMixin):
    name = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class BlogCategory(MetaTagMixin):
    name = models.CharField(verbose_name='Название', max_length=255)
    # image = models.ImageField(verbose_name='Изображение', upload_to='blog/category', null=True)
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='blog/category',
        processors=[ResizeToFill(600, 400)],
        format='JPEG',
        options={'quality': 100},
        null=True
    )

    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}' width='100'>")

    image_tag_thumbnail.short_description = 'Текущее изображение'
    image_tag_thumbnail.allow_tags = True

    def image_tag(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}'>")

    image_tag.short_description = 'Текущее изображение'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'


class Article(MetaTagMixin):
    category = models.ForeignKey(
        to=BlogCategory,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )

    tags = models.ForeignKey(
        to=Tag,
        verbose_name='Тег',
        on_delete=models.SET_NULL,
        null=True
    )

    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)

    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='blog/article/',
        processors=[],
        format='JPEG',
        options={'quality': 100},
        null=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)],
        format='JPEG',
        options={'quality': 100},
    )
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    text_preview = models.TextField(verbose_name='Текст-превью')
    text = HTMLField(verbose_name='Текст')
    user = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def image_tag_thumbnail(self):
        if self.image:
            if not self.image_thumbnail:
                Article.objects.get(id=self.id)
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image_thumbnail}' width='100'>")

    image_tag_thumbnail.short_description = 'Текущее изображение'
    image_tag_thumbnail.allow_tags = True

    def image_tag(self):
        if self.image:
            if not self.image_thumbnail:
                Article.objects.get(id=self.id)
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}'>")

    image_tag.short_description = 'Текущее изображение'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    comment_article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя', max_length=255, default='name')
    email = models.EmailField(verbose_name='E-mail')
    text = models.TextField(verbose_name='Комментарий', null=True, blank=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_checked = models.BooleanField(verbose_name='Проверено', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
