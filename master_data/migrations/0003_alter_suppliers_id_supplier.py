# Generated by Django 4.0.3 on 2022-04-13 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0002_remove_suppliers_id_alter_suppliers_id_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliers',
            name='id_supplier',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]