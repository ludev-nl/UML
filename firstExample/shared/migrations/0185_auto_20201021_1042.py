# Generated by Django 3.0.7 on 2020-10-21 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0184_delete_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
