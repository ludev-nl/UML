# Generated by Django 3.0.7 on 2020-10-21 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0176_citizen_complaint_customer_grade_order_product_teacher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
