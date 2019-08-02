from django.db import models


class Machine(models.Model):
    LOCATION = (
        ('1', 'ПКС'),
        ('7', 'ПСК')
    )
    location = models.CharField(choices=LOCATION, max_length=2)
    title = models.CharField(max_length=20)


class User(models.Model):
    fio = models.CharField(max_length=40)


class Note(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_stop = models.DateField()
    time_start = models.TimeField()
    time_stop = models.TimeField()
    stop_equipment = models.BooleanField()
    user_start = models.ForeignKey(User, on_delete=models.PROTECT)
    user_stop = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', default=None)
    text = models.TextField(max_length=200)
