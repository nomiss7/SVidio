# Generated by Django 4.0.6 on 2022-09-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, default=1, verbose_name='О себе'),
            preserve_default=False,
        ),
    ]
