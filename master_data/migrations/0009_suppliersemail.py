# Generated by Django 4.0.3 on 2022-04-27 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0008_alter_suppliers_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuppliersEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=20)),
                ('notes', models.TextField()),
            ],
        ),
    ]
