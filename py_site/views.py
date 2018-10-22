from django.shortcuts import render
from py_site.svg_create import svg_text_create
from si8_parsing.models import Machine, Value



def django(request):
    return render(request, 'py_site/django.html')


def notes(request):
    return render(request, 'py_site/notes.html')


def notes_b(request):
    machines = Machine.objects.all()
    ms = []
    for machine in machines:
        value = Value.objects.filter(register=machine.register)[0].value
        m = {'title': machine.title, 'value': svg_text_create(value)}
        ms.append(m)
    context = {'machines': ms}
    return render(request, 'py_site/notes_b.html', context)
