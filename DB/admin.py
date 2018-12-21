from django.contrib import admin
from .models import Account, DownloadTimes, DownloadLog

admin.site.register(Account)
admin.site.register(DownloadTimes)
admin.site.register(DownloadLog)

# Register your models here.
