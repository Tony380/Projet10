from django.shortcuts import render


def index(request):
    """ Main page """
    return render(request, 'index.html')


def legal(request):
    """ Legal mentions page """
    return render(request, 'legal.html')


def my_404_view(request, exception):
    """ Error 404 page """
    return render(request, '404.html')


def my_500_view(request):
    """ Error 500 page """
    return render(request, '500.html')
