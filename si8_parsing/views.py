from django.http import HttpResponse
from django.shortcuts import render
from .code2 import find_file, open_files
from .models import File, Value, Machine
from .code.pack import repack


def parsing(request):
    listsfile = File.objects.all().order_by('name')
    listcount = {'ready': len(listsfile.filter(parsing_status=0)),
                 'ok': len(listsfile.filter(parsing_status=1)),
                 'error': len(listsfile.filter(parsing_status=2))
                 }
    return render(request, 'si8parsing/parsing.html', {'listsfile': listsfile, 'listcount': listcount})


def si8_find_file(request):
    find_file()
    # task.find.delay()
    # TemplateView.as_view(template_name='si8_parsing/parsing.html')
    html = "<html><body> This is %s view</body></html>" % "hello!"
    return HttpResponse(html)


def si8_pars_file(request, pk):
    open_files(pk)
    # task.parsing.delay(pk)
    html = "<html><body> This is %s parsing</body></html>" % pk
    return HttpResponse(html)


def details(request, pk):
    html = "<html><body> This details is %s view</body></html>" % str(pk)

    val = Value.objects.get(register=pk)
    name = Machine.objects.get(register=pk).title
    stringvalue = repack(name, val.date, val.value)
    return HttpResponse(stringvalue)


"""
def parsing(request):
    findfile()
    # parsing_si8()
    # {'value': 51.8, 'now_date': datetime.datetime(2016, 12, 26, 7, 30), 'id_si8': 1}

    html = "<html><body> This is %s view</body></html>" % "hello!"
    return HttpResponse(html)
"""
