# Generated by Django 4.0.3 on 2022-05-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0012_alter_suppliers_address_alter_suppliers_cf_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliers',
            name='vat_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]