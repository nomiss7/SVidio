# Generated by Django 4.0.6 on 2022-09-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='О себе'),
        ),
    ]
