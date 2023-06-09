# Generated by Django 4.1.7 on 2023-04-02 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='strip_account_id',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart_item',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='store.order')),
            ],
        ),
    ]
