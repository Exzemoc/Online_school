# Generated by Django 4.2.2 on 2023-06-20 12:35

import django.core.validators
from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0009_remove_customgroup_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='technologies',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Python', 'Python'), ('C++', 'C++'), ('Java', 'Java'), ('C#', 'C#'), ('Pascal', 'Pascal'), ('Другое', 'Другое')], default='Python', max_length=32, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Применяемы языки'),
        ),
    ]