import django
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json

DB_DATETIME_FORMAT = '%d/%b/%Y %H:%M:%S'
DB_DATE_FORMAT = '%d/%b/%Y'
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
        return self.date.strftime(DB_DATE_FORMAT)


class Party(models.Model):
    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    title = models.CharField(max_length=50)
    index = models.IntegerField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return '{0}: {1} - {2}'.format(self.title, self.time_start, self.time_end)

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
    value = JSONField(default=[])  # TODO: добавил default=[], нужно проверить , написать Тесты!!!!
    status = JSONField(default=[])

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
        return '%d: %d' % (len(self.value), len(self.status))

    def create_kmt(self):
        return round((len(self.value) - self.value.count(0)) / len(self.value), 2)

    @staticmethod  # -> get_in_party
    def create_kmt_in_party(register=None, date_now=timezone.now(), party=None):
        value = Value.get_in_party(register=register, date_now=date_now, party=party)
        if len(value) is 0:
            return round(0.00, 2)
        return round((len(value) - value.count(0)) / len(value), 2)

    def create_length_km(self):
        length = 0
        for s in self.value:
            if s > 0:
                length = length + s
        return round(length / 1000, 2)

    @staticmethod  # -> get_in_party
    def create_length_km_in_party(register=None, date_now=timezone.now(), party=None):
        value = Value.get_in_party(register=register, date_now=date_now, party=party)
        length = 0
        for s in value:
            if s > 0:
                length = length + s
        return round(length / 1000, 2)

    def create_speed(self):
        length = 0
        work_time = 0
        speed = 0
        for s in self.value:
            if s > 0:
                work_time = work_time + 1
                length = length + s
        if work_time is not 0:
            speed = round(length / work_time, 2)
        return speed

    @staticmethod  # -> get_in_party
    def create_speed_in_party(register=None, date_now=timezone.now(), party=None):
        value = Value.get_in_party(register=register, date_now=date_now, party=party)
        length = 0
        work_time = 0
        speed = 0
        for s in value:
            if s > 0:
                work_time = work_time + 1
                length = length + s
        if work_time is not 0:
            speed = round(length / work_time, 2)
        return speed

    def create_work_time_hm(self):
        work_time = 0
        for s in self.value:
            if s > 0:
                work_time = work_time + 1
        work_time_hm = '{0:0>2}:{1:0>2}'.format(work_time // 60, work_time % 60)
        return work_time_hm

    @staticmethod  # -> get_in_party
    def create_work_time_hm_in_party(register=None, date_now=timezone.now(), party=None):
        value = Value.get_in_party(register=register, date_now=date_now, party=party)
        work_time = 0
        for s in value:
            if s > 0:
                work_time = work_time + 1
        work_time_hm = '{0:0>2}:{1:0>2}'.format(work_time // 60, work_time % 60)
        return work_time_hm

    # meaning=смысл, значение, важность
    @staticmethod
    def add(register=None, date_now=timezone.now(), flag=FLAG_STAT[0][0], time_stamp=None, meaning=None, end_date=None):
        # pass
        # if register == 198:
        #     a = 1
        #     pass
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

    @staticmethod  # TODO: определится с поведением на неправильный регистр
    # TODO: обработать случай смена№2, в первый день массив заканчивается раньше 00:00 (1440 элементов)
    def get_in_time(register=None, date_now=timezone.now(), time_start=None, time_end=None):
        try:
            value = Value.objects.get(register=register, date__date=date_now)
            if time_start is not None and time_end is not None:
                minute_start = time_start.hour * 60 + time_start.minute
                minute_end = time_end.hour * 60 + time_end.minute+1
                if minute_end-1 <= minute_start:
                    v = value.value[minute_start:]
                    try:
                        value_next_day = Value.objects.get(register=register, date__date=date_now.replace(day=date_now.day+1))
                        v.extend(value_next_day.value[0:minute_end])
                    except ObjectDoesNotExist:
                        pass
                    return v
                else:
                    return value.value[minute_start:minute_end]
            else:
                return value.value
        except ObjectDoesNotExist:
            return []

    @staticmethod  # -> get_in_time
    def get_in_party(register=None, date_now=timezone.now(), party=None):
        try:
            p = Party.objects.get(index=party)
            return Value.get_in_time(register=register, date_now=date_now, time_start=p.time_start, time_end=p.time_end)
        except ObjectDoesNotExist:
            return Value.get_in_time(register=register, date_now=date_now)


    @staticmethod
    def add_in_com_port(register, date_now=None, meaning=0):
        date_now = timezone.now()
        current_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
        obj_data = Date.objects.get_or_create(date=current_date)[0]
        current_time = date_now.time()
        total_minute = (current_time.hour * 60 + current_time.minute)
        try:
            value = Value.objects.filter(register=register, date_id=obj_data.id).get()
            old_value = value.value
            while len(old_value) < total_minute:
                old_value.append(0)
            old_value.append(meaning)
            value.value = old_value
            value.save()

        except ObjectDoesNotExist:
            value = Value.objects.create(register=register, date_id=obj_data.id, flag='GOOD', value=[])
            old_value = value.value
            while len(old_value) < total_minute:
                old_value.append(0)
            old_value.append(meaning)
            value.value = old_value
            value.save()

    @staticmethod
    def create_list(old_list, ful_lenght, value):
        my_list = old_list[:ful_lenght]
        a = len(old_list)
        b = len(my_list)
        while len(my_list) < ful_lenght:
            my_list.append(0)
        my_list.append(value)
        c = len(my_list)
        return my_list

    # принимает значение скорости и статус опроса
    @staticmethod
    def add_in_com_port1(register, meaning=0, status=0):
        # date_now = timezone.now()
        # current_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
        obj_data = Date.objects.get_or_create(date=timezone.now().date())[0]
        current_time = timezone.now().time()
        total_minute = (current_time.hour * 60 + current_time.minute)
        try:
            # value = Value.objects.filter(register=register, date_id=obj_data.id).get()
            value = Value.objects.filter(register=register, date_id=obj_data.id).get()
            old_value = value.value
            old_status = value.status
            value.value = Value.create_list(old_value, total_minute, round(meaning, 2))
            value.status = Value.create_list(old_status, total_minute, status)
            # while len(old_value) < total_minute:
            #     old_value.append(0)
            # old_value.append(meaning)
            # value.value = old_value
            #
            # while len(old_status) < total_minute:
            #     old_status.append(0)
            # old_status.append(status)
            # value.status = old_status

            value.save()

        except ObjectDoesNotExist:
            # value = Value.objects.create(register=register, date_id=obj_data.id, flag='GOOD', value=[])
            value = Value.objects.create(register=register, date_id=obj_data.id, flag='GOOD', value=[])
            old_value = value.value
            old_status = value.status
            value.value = Value.create_list(old_value, total_minute, meaning)
            value.status = Value.create_list(old_status, total_minute, status)

            # while len(old_value) < total_minute:
            #     old_value.append(0)
            # old_value.append(meaning)
            # value.value = old_value
            #
            # while len(old_status) < total_minute:
            #     old_status.append(0)
            # old_status.append(status)
            # value.status = old_status

            value.save()


class ComPort(models.Model):
    class Meta:
        verbose_name = "Сом порт"

    name = models.CharField(max_length=20, null=True, blank=True)
    enable = models.BooleanField(default=False)
    port_name = models.CharField(default='/dev/ttyUSB0', max_length=20, null=True, blank=True)
    baud_rate = models.IntegerField(default=4800)
    timeout = models.FloatField(default=0.5)

    def __str__(self):
        result = '%s = %d: %s | %d' % (self.name, self.enable, self.port_name, self.baud_rate)
        return result


class Machine(models.Model):
    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

    enable = models.BooleanField(default=False)
    title = models.CharField(max_length=50)  # имя объекта(название группы регистров - пример=битумный котел)
    lower = models.CharField(max_length=50, default='', blank=True, null=True)  # имя в нижнем регистре, для телег.бота
    register = models.IntegerField()  # адрес устройства
    com_port = models.ForeignKey(ComPort, on_delete=models.PROTECT, blank=True, null=True)
    normative_time = models.TimeField()  # норматив машинного времени
    normative_speed = models.FloatField(default=0)  # норматив скорости
    normative_product = models.FloatField(default=0)  # норматив выработки

    # time_disconect  время отсутствия ответа

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

