# Generated by Django 3.0.7 on 2020-11-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0296_course_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
