# Generated by Django 3.0.7 on 2020-08-09 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0007_citizen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
