# Generated by Django 3.0.7 on 2020-10-07 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0112_delete_teacher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
