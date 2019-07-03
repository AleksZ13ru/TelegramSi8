# Generated by Django 2.0.3 on 2019-06-07 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('si8_parsing', '0003_comport_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='comport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='si8_parsing.ComPort'),
        ),
    ]
