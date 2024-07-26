# Generated by Django 5.0.7 on 2024-07-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoe_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Discount Price'),
        ),
    ]