# Generated by Django 4.0.3 on 2022-08-31 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0023_chemicalpurchase_alter_substances_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chemicalpurchase',
            options={'ordering': ['-date_doc'], 'verbose_name': 'Chemicals Purchase', 'verbose_name_plural': 'Chemicals Purchases'},
        ),
    ]
