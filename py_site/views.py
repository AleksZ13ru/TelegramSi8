from django.shortcuts import render


def django(request):
    return render(request, 'py_site/django.html')
