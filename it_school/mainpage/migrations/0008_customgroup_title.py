# Generated by Django 4.2.2 on 2023-06-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0007_alter_lesson_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroup',
            name='title',
            field=models.CharField(default='Группа 1', max_length=255),
        ),
    ]