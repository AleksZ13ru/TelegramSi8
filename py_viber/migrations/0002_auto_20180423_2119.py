# Generated by Django 2.0.3 on 2018-04-23 21:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('py_viber', '0001_squashed_0005_auto_20180422_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='key',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='viber_chart',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]
