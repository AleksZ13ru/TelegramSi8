# Generated by Django 2.0.3 on 2018-03-25 21:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Даты',
                'verbose_name': 'Дата',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=250)),
                ('parsing_status', models.IntegerField(default=0)),
                ('hash', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': 'Файлы',
                'verbose_name': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=250)),
                ('enable', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Папки',
                'verbose_name': 'Папки',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('lower', models.CharField(default='', max_length=50)),
                ('register', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Оборудование',
                'verbose_name': 'Оборудование',
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register', models.IntegerField()),
                ('flag', models.CharField(choices=[('GOOD', 'Good'), ('TOUT', 'Time Out'), ('ERR', 'Error')], max_length=4)),
                ('value', django.contrib.postgres.fields.jsonb.JSONField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='si8_parsing.Date')),
            ],
            options={
                'verbose_name_plural': 'Значения',
                'verbose_name': 'Значение',
            },
        ),
        migrations.CreateModel(
            name='ValueChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('change_value', models.IntegerField(default=0)),
                ('read_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('read_value', models.IntegerField(default=0)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='si8_parsing.Machine')),
            ],
            options={
                'verbose_name_plural': 'Последний опрос',
                'verbose_name': 'Последние опросы',
            },
        ),
    ]
