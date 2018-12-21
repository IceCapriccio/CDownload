from django.db import models


class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=30, null=True)
    # permission: admin, user, test
    permission = models.CharField(max_length=5, default='user')
    free = models.BooleanField(default=False)
    regTime = models.DateTimeField(auto_now=True)


class DownloadTimes(models.Model):
    id = models.OneToOneField("Account", primary_key=True, unique=True, on_delete=models.CASCADE)
    times = models.IntegerField(null=False)


class DownloadLog(models.Model):
    id = models.OneToOneField("Account", primary_key=True, unique=True, on_delete=models.PROTECT)
    url = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)


class CSDN_VIP_Account(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=30)
    today_use_times = models.IntegerField(null=True)
    today_use_limit = models.IntegerField(null=True)
    left_times = models.IntegerField(null=False, default=600)


class DbKm(models.Model):
    gid = models.IntegerField()
    km = models.CharField(max_length=100, blank=True, null=True)
    bentime = models.DateTimeField(db_column='benTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    out_trade_no = models.CharField(max_length=100, blank=True, null=True)
    trade_no = models.CharField(max_length=100, blank=True, null=True)
    rel = models.CharField(max_length=50, blank=True, null=True)
    stat = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DB_km'

