# Generated by Django 4.0.3 on 2022-06-12 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0014_alter_sds_sds'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chemicaldangersymbols',
            unique_together={('id_sds', 'id_danger')},
        ),
    ]