# Generated by Django 4.1.7 on 2023-03-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_member_address_alter_member_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(default='BOSS', max_length=100),
            preserve_default=False,
        ),
    ]
