# Generated by Django 2.0.3 on 2019-07-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('si8_parsing', '0007_value_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='lower',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]