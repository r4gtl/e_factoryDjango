# Generated by Django 4.0.3 on 2022-07-07 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0020_alter_prices_price_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='price_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]