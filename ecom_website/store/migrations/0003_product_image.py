# Generated by Django 4.1.7 on 2023-03-31 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cart_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='none', upload_to='images/'),
            preserve_default=False,
        ),
    ]
