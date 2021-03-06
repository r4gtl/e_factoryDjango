# Generated by Django 4.0.3 on 2022-05-12 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0013_alter_suppliers_vat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliers',
            name='vat_perc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='master_data.vatcodes'),
        ),
        migrations.CreateModel(
            name='CustomersContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master_data.suppliers')),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('vat_number', models.CharField(max_length=11, unique=True)),
                ('cf_number', models.CharField(blank=True, max_length=16)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('cap', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('prov', models.CharField(blank=True, max_length=10)),
                ('country_state', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vat_perc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='master_data.vatcodes')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
    ]
