# Generated by Django 4.0.3 on 2022-06-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0016_chemicalorder_chemicalorderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemicalorder',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
