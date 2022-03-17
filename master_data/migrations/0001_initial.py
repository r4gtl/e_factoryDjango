# Generated by Django 4.0.3 on 2022-03-17 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VatCodes',
            fields=[
                ('vat_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=10)),
                ('tax_perc', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Vat Code',
                'verbose_name_plural': 'Vat Codes',
            },
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_supplier', models.IntegerField()),
                ('company_name', models.CharField(max_length=100)),
                ('vat_number', models.CharField(max_length=11)),
                ('cf_number', models.CharField(max_length=16)),
                ('address', models.CharField(max_length=100)),
                ('cap', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(max_length=100)),
                ('prov', models.CharField(max_length=10)),
                ('country_state', models.CharField(blank=True, max_length=10, null=True)),
                ('gg_valuta', models.IntegerField(blank=True, null=True)),
                ('sds_path', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vat_perc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master_data.vatcodes')),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
            },
        ),
    ]
