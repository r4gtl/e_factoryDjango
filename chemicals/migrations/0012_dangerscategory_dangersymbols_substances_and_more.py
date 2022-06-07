# Generated by Django 4.0.3 on 2022-06-07 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0011_alter_sds_sds'),
    ]

    operations = [
        migrations.CreateModel(
            name='DangersCategory',
            fields=[
                ('id_category', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DangerSymbols',
            fields=[
                ('id_danger', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('acronym', models.CharField(max_length=50)),
                ('symbol', models.ImageField(upload_to='danger_symbols')),
            ],
        ),
        migrations.CreateModel(
            name='Substances',
            fields=[
                ('id_substance', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('ec_number', models.CharField(max_length=50)),
                ('cas_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalsSubstances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentration', models.CharField(max_length=50)),
                ('id_chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.chemicals')),
                ('id_sds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.sds')),
                ('id_substance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.substances')),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalsPrecautionaryStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.chemicals')),
                ('id_ps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.precautionarystatements')),
                ('id_sds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.sds')),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalDangerSymbols',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.chemicals')),
                ('id_danger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.dangersymbols')),
                ('id_sds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.sds')),
            ],
        ),
    ]
