from django.http import HttpResponse
from DATA.models import Account, DownloadTimes, DownloadLog, Km
from django.shortcuts import render


def testdb(request):
    print(Km.objects.all())
    return HttpResponse('success')


def update(request):
    return render(request, 'update.html')


def solve_update(request):
    Account.objects.filter(id='test').update(free=True)
    return HttpResponse('success')
