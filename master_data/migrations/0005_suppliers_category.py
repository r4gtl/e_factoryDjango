# Generated by Django 4.0.3 on 2022-04-16 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0004_supplierscategories'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliers',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='master_data.supplierscategories'),
            preserve_default=False,
        ),
    ]
