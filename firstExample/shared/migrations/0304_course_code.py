# Generated by Django 3.0.7 on 2020-11-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0303_course_course_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
