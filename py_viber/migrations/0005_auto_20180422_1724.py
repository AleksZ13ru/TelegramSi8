# Generated by Django 2.0.3 on 2018-04-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('py_viber', '0004_auto_20180422_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'User'), ('SU_USER', 'Superuser'), ('NEW_USER', 'New user'), ('VALID', 'Valid user'), ('VALID_VERIF', 'Valid user verif'), ('VALID_GOOD', 'Valid good'), ('SU_VALID', 'Super valid user'), ('ADMIN', 'Admin'), ('BLACK', 'Blacklist user')], default='NEW_USER', max_length=16),
        ),
    ]
