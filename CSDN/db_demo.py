from django.http import HttpResponse
from DB.models import Account, DownloadTimes, DownloadLog, DbKm
from django.shortcuts import render


def testdb(request):
    print(DbKm.objects.all())
    return HttpResponse('success')


def update(request):
    return render(request, 'update.html')


def solve_update(request):
    Account.objects.filter(id='test').update(free=True)
    return HttpResponse('success')
