# Generated by Django 4.0.3 on 2022-04-16 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0006_remove_suppliers_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliers',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='master_data.supplierscategories'),
            preserve_default=False,
        ),
    ]