# Generated by Django 4.0.3 on 2022-04-27 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0010_suppliersemail_id_supplier'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SuppliersEmail',
            new_name='SuppliersContacts',
        ),
    ]
