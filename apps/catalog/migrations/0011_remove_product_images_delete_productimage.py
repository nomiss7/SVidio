# Generated by Django 4.0.6 on 2022-08-18 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_remove_productimage_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
