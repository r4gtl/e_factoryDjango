# Generated by Django 4.0.3 on 2022-04-27 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0009_suppliersemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliersemail',
            name='id_supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_data.suppliers'),
        ),
    ]