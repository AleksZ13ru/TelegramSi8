# Generated by Django 2.0.3 on 2019-08-01 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('si8_parsing', '0013_auto_20190731_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='normative_time',
        ),
    ]
