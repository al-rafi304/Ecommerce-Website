# Generated by Django 4.1.7 on 2023-04-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_product_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PD', 'Pending'), ('DL', 'Delivered'), ('CL', 'Cancelled')], default='PD', max_length=2),
        ),
    ]
