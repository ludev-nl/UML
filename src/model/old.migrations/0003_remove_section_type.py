# Generated by Django 3.0.7 on 2021-07-12 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_auto_20210706_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='type',
        ),
    ]
