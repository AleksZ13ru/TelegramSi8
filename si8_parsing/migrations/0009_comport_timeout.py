# Generated by Django 2.0.3 on 2019-07-05 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('si8_parsing', '0008_auto_20190701_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='comport',
            name='timeout',
            field=models.FloatField(default=0.5),
        ),
    ]