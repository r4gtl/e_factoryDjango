# Generated by Django 4.0.3 on 2022-06-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0012_dangerscategory_dangersymbols_substances_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sds',
            name='rev_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]