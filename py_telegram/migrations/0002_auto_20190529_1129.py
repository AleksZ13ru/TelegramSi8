# Generated by Django 2.0.3 on 2019-05-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('py_telegram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'User'), ('SU_USER', 'Superuser'), ('NEW_USER', 'New user'), ('ADMIN', 'Admin'), ('BLACK', 'Blacklist user')], default='BLACK', max_length=8),
        ),
    ]
