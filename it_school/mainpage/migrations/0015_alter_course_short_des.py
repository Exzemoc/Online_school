# Generated by Django 4.2.2 on 2023-06-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0014_merge_20230622_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='short_des',
            field=models.TextField(default='', verbose_name='Краткое описание'),
        ),
    ]