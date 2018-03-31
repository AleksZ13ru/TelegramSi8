import django
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json

DB_DATETIME_FORMAT = '%d/%b/%Y %H:%M:%S'
DB_DATE_FORMAT = '%m/%d/%Y'
DB_DATETIME_Z_FORMAT = '%m/%d/%Y 0:0'
DB_TIME_FORMAT = "%H:%M"


class Folder(models.Model):
    class Meta:
        verbose_name = "Папки"
        verbose_name_plural = "Папки"

    path = models.CharField(max_length=250)
    enable = models.BooleanField()

    def __str__(self):
        return self.path


class File(models.Model):
    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    name = models.CharField(max_length=50)
    path = models.CharField(max_length=250)
    parsing_status = models.IntegerField(default=0)  # 0 - еще не парсин,
    # 1 - парсинг успешен,
    # 2 - парсинг начат но не закончен
    hash = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.path, self.name)


class Date(models.Model):
    class Meta:
        verbose_name = "Дата"
        verbose_name_plural = "Даты"

    date = models.DateField()

    def __str__(self):
        # result = '%s' % (
        #     self.date
        # )
        return self.date.strftime(DB_DATETIME_FORMAT)


# class TimeStamp(models.Model):
#     class Meta:
#         verbose_name = "Штамп времени"
#         verbose_name_plural = "Штампы времени"
#
#     title = models.CharField(max_length=40)
#     x = JSONField()
#
#     def __str__(self):
#         return self.title


class Value(models.Model):
    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"

    FLAG_STAT = (
        ('GOOD', 'Good'),
        ('TOUT', 'Time Out'),
        ('ERR', 'Error')
    )
    register = models.IntegerField()
    date = models.ForeignKey('Date', on_delete=models.PROTECT)
    flag = models.CharField(max_length=4, choices=FLAG_STAT)  # флаг состояния цепочки данных
    value = JSONField()

    def __str__(self):
        result = '%s | %s=%d | %s' % (
            self.date,
            self.register,
            len(self.value),
            self.flag
        )
        return result

    def display_title(self):
        try:
            title = Machine.objects.get(register=self.register)
        except ObjectDoesNotExist:
            title = 'Нет привязки к оборудованию'
        return title

    def display_len(self):
        return len(self.value)

    # meaning=смысл, значение, важность
    @staticmethod
    def add(register=None, date_now=timezone.now(), flag=FLAG_STAT[0][0], time_stamp=None, meaning=None, end_date=None):
        pass
        if register == 128:
            a = 1
            pass
        current_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
        obj_data = Date.objects.get_or_create(date=current_date)[0]
        current_time = date_now.time()
        total_minute = (current_time.hour * 60 + current_time.minute)
        try:
            value = Value.objects.filter(register=register, date_id=obj_data.id).get()
            old_value = value.value
            new_value = meaning
            #  есть строка в базе
            # l_old_value = old_value.value

            for i in range(abs(len(old_value) - len(new_value))):
                if len(old_value) < len(new_value):
                    old_value.append(0)
                else:
                    new_value.append(0)
            for j in range(len(old_value)):
                if j > 450:
                    a = old_value[j]
                    b = new_value[j]
                if old_value[j] != 0 and new_value[j] == 0:
                    new_value[j] = old_value[j]
                    # elif old_value[j]!=0 and new_value[j]!=0:
            # if len(lvalue) < total_minute - 1:
            #     for i in range(total_minute - len(lvalue)):
            #         lvalue.append(0)
            # lvalue.append(meaning)
            value.value = new_value
            value.save()

        except ObjectDoesNotExist:
            # lvalue = []
            # for i in range(total_minute - 1):
            #     lvalue.append(0)
            # lvalue.extend(meaning)
            value = Value.objects.create(register=register, date_id=obj_data.id, flag='GOOD', value=meaning)
            value.save()

        try:
            # machine = Machine.objects.get(register=register)
            value_change = ValueChange.objects.get(machine__register=register)
            # if (value_change.change_value != 0 and value.value[-1] == 0) or \
            #         (value_change.change_value == 0 and value.value[-1] != 0):
            value_change.change_value = value.value[-1]
            hour = (len(value.value) - 1) // 60
            if hour > 23:
                hour = 23
            minute = len(value.value) - hour * 60 - 1
            if minute > 59:
                minute = 59
            value_change.change_datetime = date_now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            # value_change.change_datetime = date_now.replace(minute=len(value.value))
            value_change.save()
            # current_time.replace()
        except ObjectDoesNotExist:
            machine = Machine.objects.get(register=register)
            change_value = value.value[-1]
            hour = (len(value.value) - 1) // 60
            min = len(value.value) - hour * 60 - 1
            change_datetime = date_now.replace(hour=hour, minute=min, second=0, microsecond=0)
            value_change = ValueChange.objects.create(machine=machine, change_value=change_value,
                                                      change_datetime=change_datetime)
            value_change.save()
        if end_date is not None:
            if value_change.change_datetime < end_date:
                value_change.read_datetime = end_date
                value_change.read_value = 0
            elif value_change.change_datetime == end_date:
                value_change.read_datetime = end_date
                value_change.read_value = value_change.change_value
            elif value_change.change_datetime > end_date:
                pass
            value_change.save()
        # Register.last_update(register=register.pk, time=date_now, value=meaning)


class Machine(models.Model):
    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

    title = models.CharField(max_length=50)  # имя объекта(название группы регистров - пример=битумный котел)
    lower = models.CharField(max_length=50, default='')  # имя в нижнем регистре, для поиска телеграмм бота
    register = models.IntegerField()  # адрес устройства

    def __str__(self):
        result = '%s | %d' % (self.title, self.register)
        return self.title


class ValueChange(models.Model):
    class Meta:
        verbose_name = 'Последние опросы'
        verbose_name_plural = 'Последний опрос'

    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    change_datetime = models.DateTimeField(default=django.utils.timezone.now)  # время последней не нулевой скорости
    change_value = models.IntegerField(default=0)  # значение последней не нулевой скорости
    read_datetime = models.DateTimeField(
        default=django.utils.timezone.now)  # время последнего опроса, получается из поледнего времени полученного из файла
    read_value = models.IntegerField(default=0)  # значение последнего опроса

    def __str__(self):
        result = '{0} | {1}={2}'.format(self.machine.title, self.read_datetime, self.read_value)
        return result