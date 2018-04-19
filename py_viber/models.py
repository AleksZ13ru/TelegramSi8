from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# from si8_parsing.models import Machine


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    ROLE_STAT = (
        ('USER', 'User'),
        ('SU_USER', 'Superuser'),
        ('NEW_USER', 'New user'),
        ('VALID', 'Valid user'),        # пользователь ввел адрес почты, ожидает проверки
        ('VALID_GOOD', 'Valid good'),   # проверка пройдена, ожидается отправка сообщения о завершении проверки
        ('SU_VALID', 'Super valid user'),  # администратор, для принятия новых пользователей
        ('ADMIN', 'Admin'),
        ('BLACK', 'Blacklist user')     # черный список пользователей
    )

    first_name = models.CharField(max_length=100)
    viber_id = models.CharField(max_length=100)
    role = models.CharField(max_length=8, choices=ROLE_STAT, default='NEW_USER')
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.first_name


# class Favorite(models.Model):
#     class Meta:
#         verbose_name = "Избронное"
#         verbose_name_plural = "Избранные"
#
#     STATUS_STAT = (
#         ('READY', 'Запись добавлена, но еще не подтверждена'),
#         ('RUN', 'Запись в работе'),
#         ('DELETE', 'Для записи запрошено удаление')
#     )
#     user = models.ForeignKey('User', on_delete=models.PROTECT)
#     machine = models.CharField(max_length=30)
#     status = models.CharField(max_length=4, choices=STATUS_STAT)


# class Loop(models.Model):
#     """
#     Запись с указанием оборудования и сохраненном состоянием на указаннуое время-дату
#     Муки выбора:
#                     1- user = models.ForeignKey - много к одному, приведет к увеличению количества записей для одного
#                     оборудования у разных пользовтелей, то есть возможность настройки разных тригеров
#             OK =    2- user = models.ManyToManyField - много ко многим, при небходимости добавить другое условие
#                     тригера, создать следующую запись
#
#     trigger_datetime = время, последней фиксации изменения состояния работы
#     trigger_value = значение скорссти в момент времени, trigger_datetime
#     trigger_hysteresis = время, по истечению которого можно считать что условие останова/запуска произошло
#     """
#
#     class Meta:
#         verbose_name = "Петля"
#         verbose_name_plural = "Петли"
#
#     STATUS_STAT = (
#         ('READY', 'Запись добавлена, но еще не подтверждена'),
#         ('RUN', 'Запись в работе'),
#         ('DELETE', 'Для записи запрошено удаление')
#     )
#
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
#     status = models.CharField(max_length=6, choices=STATUS_STAT, default='RUN')
#     trigger_datetime = models.DateTimeField(default=timezone.now)
#     trigger_value = models.IntegerField(default=0)
#     trigger_hysteresis = models.IntegerField(default=0)  # считает кол-во минут значения скорости
#
#     def __str__(self):
#         return '%s: %s' % (self.user, self.machine)
#
#
class Message(models.Model):
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    STATUS_STAT = (
        ('READY', 'Ждет отправления'),
        ('POST', 'Отправлено')
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=6, choices=STATUS_STAT, default='READY')
    date_status = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=300)

    def __str__(self):
        return '%s: %s' % (self.user, self.status)
