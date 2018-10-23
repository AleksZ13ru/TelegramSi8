from django.utils import timezone

from django.shortcuts import render
from py_site.svg_create import svg_text_create, svg_pure
from si8_parsing.models import Machine, Value, Date

DATE_FORMAT = 'd E Y'
DB_DATE_FORMAT = '%d/%m/%Y'


def django(request):
    return render(request, 'py_site/django.html')


def notes(request):
    return render(request, 'py_site/notes.html')


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
        d = Date.objects.filter(date=timezone.now())[0]
        try:
            value = Value.objects.filter(register=machine.register, date=d.id)[0].value
            svg = svg_text_create(value)
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
