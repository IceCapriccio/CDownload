from django.db import models


class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=32)
    free = models.IntegerField()
    permission = models.CharField(max_length=5)
    regtime = models.DateTimeField(db_column='regTime', auto_now=True)  # Field name made lowercase.
    email = models.CharField(max_length=30, blank=True, null=True)


class CSDN_Vip_Account(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=30)
    left_times = models.IntegerField()
    today_use_limit = models.IntegerField(blank=True, null=True)
    today_use_times = models.IntegerField(blank=True, null=True)


class DownloadLog(models.Model):
    username = models.ForeignKey('CSDN_Vip_Account', unique=False)
    url = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)


class DownloadTimes(models.Model):
    id = models.OneToOneField('Account', models.DO_NOTHING, primary_key=True)
    times = models.IntegerField()


class Km(models.Model):
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
