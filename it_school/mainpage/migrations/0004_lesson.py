# Generated by Django 4.2.2 on 2023-06-13 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_remove_customuser_available_courses_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='mainpage.course')),
            ],
        ),
    ]