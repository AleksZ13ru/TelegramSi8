# Generated by Django 2.0.3 on 2019-08-02 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('si8_parsing', '0015_machine_normative_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('index', models.IntegerField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
            ],
            options={
                'verbose_name': 'Смена',
                'verbose_name_plural': 'Смены',
            },
        ),
    ]
