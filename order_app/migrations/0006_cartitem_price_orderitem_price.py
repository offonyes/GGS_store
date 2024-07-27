# Generated by Django 5.0.7 on 2024-07-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0005_alter_orderitem_order_alter_orderitem_shoe'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Price'),
            preserve_default=False,
        ),
    ]
