from django.utils import timezone

from django.shortcuts import render
from py_site.svg_create import svg_text_create, svg_pure
from si8_parsing.models import Machine, Value, Date

DATE_FORMAT = 'd E Y'
DB_DATE_FORMAT = '%d/%m/%Y'


def django(request):
    return render(request, 'py_site/django.html')


# передаваемые данные:
# 1 - current_date - текущая дата
# 2 - machine - единица оборудования
# 2.1 - title - название оборудования
# 2.2 - value - массив скорости

def notes_b(request):
    current_date = timezone.now().strftime(DB_DATE_FORMAT)
    machines = Machine.objects.all()
    ms = []
    for machine in machines:
        # value = Value.objects.filter(register=machine.register)[0].value
        try:
            d = Date.objects.get(date=timezone.now())
        except Date.DoesNotExist:
            d = Date(date=timezone.now())
            d.save()
        try:
            value = Value.objects.get(register=machine.register, date=d.id)
            svg = svg_text_create(value.value)
            m = {'title': machine.title, 'value': svg, 'kmt': value.create_kmt()}
            ms.append(m)
        except IndexError:
            svg = svg_pure()
    context = {'current_date': current_date, 'machines': ms}
    return render(request, 'py_site/notes_b.html', context)


def report(request):
    current_date = timezone.now().strftime(DB_DATE_FORMAT)
    machines = Machine.objects.all()
    ms = []
    for machine in machines:
        try:
            d = Date.objects.get(date=timezone.now())
        except Date.DoesNotExist:
            d = Date(date=timezone.now())
            d.save()
        try:
            value = Value.objects.get(register=machine.register, date=d.id)
            # svg = svg_text_create(value)
            m = {'title': machine.title,
                 'normative_time': '{0:0>2}:{1:0>2}'.format(machine.normative_time.hour, machine.normative_time.minute),
                 'normative_speed': machine.normative_speed,
                 'normative_product': machine.normative_product,
                 'present_time': value.create_work_time_hm(),
                 'present_speed': value.create_speed(),
                 'present_product': value.create_length_km(),
                 'kmt': value.create_kmt()}
            ms.append(m)
        except IndexError:
            pass
    context = {'current_date': current_date, 'machines': ms}
    return render(request, 'py_site/report.html', context)


def report_history(request, filter, party, year, month, day):
    current_date = timezone.now().replace(year=year, month=month, day=day).strftime(DB_DATE_FORMAT)
    if filter is 0:
        machines = Machine.objects.all()
    else:
        machines = Machine.objects.filter(pk=filter)
    ms = []
    for machine in machines:
        # d = Date.objects.filter(date=timezone.now().replace(year=year, month=month, day=day))[0]
        try:
            d = Date.objects.get(date=timezone.datetime(year=year, month=month, day=day))
        except Date.DoesNotExist:
            d = Date(date=timezone.datetime(year=year, month=month, day=day))
            d.save()
        kmt = 0
        length = 0
        length_km = 0
        work_time = 0
        work_time_hm = '00:00'
        speed = 0
        # TODO:  переправить filter на get запрос
        # TODO:  kmt и подобные запросы перенести в модель
        if party is 2:
            next_d = Date.objects.get(date=timezone.datetime(year=year, month=month, day=day+1))
        try:
            value = Value.objects.filter(register=machine.register, date=d.id)[0].value
            v = value
            next_value = Value.objects.filter(register=machine.register, date=next_d.id)[0].value
            v.extend(next_value)
            kmt = round((len(v) - v.count(0)) / len(v), 2)
            for s in v:
                if s > 0:
                    work_time = work_time + 1
                    length = length + s
            if work_time is not 0:
                speed = round(length / work_time, 2)
            length_km = round(length / 1000, 2)
            work_time_hm = '{0:0>2}:{1:0>2}'.format(work_time // 60, work_time % 60)
        except IndexError:
            pass

        m = {'title': machine.title,
             'normative_time': machine.normative_time,
             'normative_speed': machine.normative_speed,
             'normative_product': machine.normative_product,
             'present_time': work_time_hm,
             'present_speed': speed,
             'present_product': length_km,
             'kmt': kmt}
        ms.append(m)
    context = {'current_date': current_date, 'machines': ms}
    return render(request, 'py_site/report.html', context)


def machine_filter(request, filter, party, year, month, day):
    current_date = timezone.now().replace(year=year, month=month, day=day).strftime(DB_DATE_FORMAT)
    if filter is 0:
        machines = Machine.objects.all()
    else:
        machines = Machine.objects.filter(pk=filter)
    ms = []
    for machine in machines:
        d = Date.objects.filter(date=timezone.now().replace(year=year, month=month, day=day))[0]
        if party is 2:
            next_d = Date.objects.filter(date=timezone.now().replace(year=year, month=month, day=day + 1))[0]
        try:
            value = Value.objects.filter(register=machine.register, date=d.id)[0].value
            if party is 2:
                next_value = Value.objects.filter(register=machine.register, date=next_d.id)[0].value
                svg = svg_text_create(values=value, next_values=next_value, party=party)
            else:
                svg = svg_text_create(values=value, party=party)
        except IndexError:
            svg = svg_pure()

        m = {'title': machine.title, 'value': svg}
        ms.append(m)
    context = {'current_date': current_date, 'machines': ms}
    return render(request, 'py_site/notes_b.html', context)


def notes_b_history(request, year, month, day):
    current_date = timezone.now().replace(year=year, month=month, day=day).strftime(DB_DATE_FORMAT)
    machines = Machine.objects.all()
    ms = []
    for machine in machines:
        # value = Value.objects.filter(register=machine.register)[0].value
        d = Date.objects.filter(date=timezone.now().replace(year=year, month=month, day=day))[0]
        try:
            value = Value.objects.filter(register=machine.register, date=d.id)[0].value
            svg = svg_text_create(value)
        except IndexError:
            svg = svg_pure()
        m = {'title': machine.title, 'value': svg}
        ms.append(m)
    context = {'current_date': current_date, 'machines': ms}
    return render(request, 'py_site/notes_b.html', context)


def notes_detail(request, pk):
    current_date = timezone.now().strftime(DB_DATE_FORMAT)
    machine = Machine.objects.filter(register=pk)[0]
    ms = []
    d = Date.objects.filter(date=timezone.now())[0]
    try:
        value = Value.objects.filter(register=machine.register, date=d.id)[0].value
        svg = svg_text_create(value)
    except IndexError:
        svg = svg_pure()
    m = {'title': machine.title, 'value': svg}
    ms.append(m)
    context = {'current_date': current_date, 'machine': m}
    return render(request, 'py_site/notes_b_single.html', context)
