# Generated by Django 4.0.6 on 2022-08-18 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='category',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='catalog.productimage', verbose_name='Теги'),
        ),
    ]
