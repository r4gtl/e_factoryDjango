# Generated by Django 4.0.3 on 2022-10-21 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('idreparto', models.AutoField(db_column='idreparto', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='descrizionereparto', help_text='Nome reparto', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'wards',
                'db_table': 'reparti',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('idmansione', models.AutoField(db_column='idmansione', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='descrizionemansione', help_text='Nome mansione', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idreparto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.ward')),
            ],
            options={
                'verbose_name_plural': 'roles',
                'db_table': 'mansioni',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='HumanResource',
            fields=[
                ('idpersona', models.AutoField(db_column='idpersona', primary_key=True, serialize=False)),
                ('cognomedipendente', models.CharField(max_length=50)),
                ('nomedipendente', models.CharField(max_length=50)),
                ('dataassunzione', models.DateField()),
                ('datadimissioni', models.DateField(blank=True, null=True)),
                ('qualifica', models.CharField(blank=True, max_length=50, null=True)),
                ('commenti', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idmansione', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.role')),
                ('idreparto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.ward')),
            ],
            options={
                'verbose_name_plural': 'dipendenti',
                'db_table': 'dipendenti',
                'ordering': ['-dataassunzione'],
            },
        ),
    ]
