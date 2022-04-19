# Generated by Django 4.0.3 on 2022-04-16 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0003_alter_suppliers_id_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuppliersCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('note', models.TextField()),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]