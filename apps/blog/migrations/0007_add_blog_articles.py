# Generated by Django 4.0.6 on 2022-07-21 11:03

from django.db import migrations
from apps.blog.models import Article, BlogCategory


def add_blog_articles(apps, schema_editor):
    news_category = BlogCategory.objects.get(name='Новости')
    articles = [
        {'category': news_category, 'title': 'Мы открылись', 'text_preview': 'Наш магазин начинает работу', 'text': 'Банальные, но неопровержимые выводы, а также непосредственные участники технического прогресса призывают нас к новым свершениям, которые, в свою очередь, должны быть функционально разнесены на независимые элементы. Современные технологии достигли такого уровня, что укрепление и развитие внутренней структуры в значительной степени обусловливает важность новых предложений. Вот вам яркий пример современных тенденций — экономическая повестка сегодняшнего дня предопределяет высокую востребованность стандартных подходов.'},
        {'category': news_category, 'title': 'Мы запустили блог', 'text_preview': 'На сайте нашего магазина запускается блог, где вы сможете узнать свежую информацию', 'text': 'Картельные сговоры не допускают ситуации, при которой некоторые особенности внутренней политики будут смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности. Значимость этих проблем настолько очевидна, что граница обучения кадров говорит о возможностях позиций, занимаемых участниками в отношении поставленных задач. Приятно, граждане, наблюдать, как реплицированные с зарубежных источников, современные исследования набирают популярность среди определенных слоев населения, а значит, должны быть разоблачены.'},
        {'category': news_category, 'title': 'Категории блога', 'text_preview': 'Теперь наш блог разбит на категории и вы сможете читать только самые интересные для вас рубрики', 'text': 'Также как убеждённость некоторых оппонентов обеспечивает актуальность поставленных обществом задач. Наше дело не так однозначно, как может показаться: разбавленное изрядной долей эмпатии, рациональное мышление выявляет срочную потребность модели развития. В своём стремлении улучшить пользовательский опыт мы упускаем, что представители современных социальных резервов неоднозначны и будут функционально разнесены на независимые элементы.'},
    ]
    for article in articles:
        Article.objects.create(
            category=article['category'],
            title=article['title'],
            text_preview=article['text_preview'],
            text=article['text'],
        )
        ##article.objects.create(**article)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_add_blog_categories'),
    ]

    operations = [
        migrations.RunPython(add_blog_articles)
    ]
