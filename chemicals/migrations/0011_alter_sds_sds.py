# Generated by Django 4.0.3 on 2022-06-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0010_alter_chemicals_cov'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sds',
            name='sds',
            field=models.FileField(upload_to=''),
        ),
    ]
