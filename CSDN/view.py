from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from DB.models import Account, DownloadLog, DownloadTimes, CSDN_VIP_Account, DbKm
from django.db.models import F
from .downloader import CsdnDownloader
import base64 as b
from random import randint
import DB.models


def register(request):
    return render(request, 'register.html')


def solve_register(request):
    id = request.POST['id']
    password = request.POST['password']
    email = request.POST['email']
    query = Account.objects.filter(id=id)
    if len(query) == 0:
        # 账号之前未被注册，Account 表中插入数据
        Account(id=id, password=b64encode(id), free=True, email=email).save()
        # 注册成功直接跳转登录界面，并发送 cookie
        response = render(request, 'download.html')
        response.set_cookie('id', id, max_age=600)  # cookie 存在 10 分钟
        return response
    else:
        response = HttpResponseRedirect('/register')
        response.set_cookie('msg', 'account already exist!')
        return response


def login(request):
    if request.COOKIES.get('id', None) is not None:
        id = request.COOKIES['id']
        times = DownloadTimes.objects.get(id=Account.objects.get(id=id)).times
        context = {'id': id, 'download_times': times}
        response = render(request, 'download.html', context=context)
        return response
    return render(request, 'login.html')


def b64encode(plain):
    """
    :return 将明文经过 Base64 加密后，头部加上 'A'，作为加密后的密文
    """
    return (b'A' + b.b64encode(plain.encode())).decode()


def b64decode(cipher):
    """
    :return: 将密文去掉第一个字符后经过 Base64 解密，即为明文
    """
    cipher = cipher[1:].encode()
    return b.b64decode(cipher).decode()


def solve_login(request):
    # print('solve login cookies:', request.COOKIES)
    id = request.POST['id']
    password = request.POST['password']
    query = Account.objects.filter(id=id)

    if len(query) == 0:
        response = HttpResponseRedirect('/login')
        response.set_cookie('msg', 'account not exist!')
        return response
    if query[0].password != b64encode(password):
        response = HttpResponseRedirect('/login')
        response.set_cookie('msg', 'password wrong!')
        return response
    # 登录成功则跳转到下载页面
    response = HttpResponseRedirect('/download')
    response.set_cookie('id', id, max_age=600)  # cookie 存在 10 分钟
    response.set_cookie('msg', 'login success', expires=10)
    return response


def download(request):
    # 如果 cookie 过期，则跳转到登录界面
    if request.COOKIES.get('id') is None:
        return render(request, 'login.html')
    id = request.COOKIES['id']
    download_times = DownloadTimes.objects.get(id=id).times
    return render(request, 'download.html', locals())


def solve_download(request):
    # print('solve download cookies:', request.COOKIES).
    # 下载到本地的路径
    local_path = '/var/www/html/down/files'

    # 如果 cookie 过期，则跳转到登录界面
    if request.COOKIES.get('id') is None:
        return render(request, 'login.html')

    # cookie 判断下载次数是否足够
    id = request.COOKIES['id']
    times = DownloadTimes.objects.get(id=id).times
    act_obj = Account.objects.get(id=id)
    isfree = act_obj.free
    if times <= 0 and not isfree:
        return HttpResponse('次数不足')

    # 从 CSDN 账号池中选择一个账号
    accounts = CSDN_VIP_Account.objects.filter(today_use_times__lt=F("today_use_limit"))
    if len(accounts) == 0:
        # 没有可用账号
        return HttpResponse("出现了一点问题呢，请联系管理员~")
    number = len(accounts)
    choice = randint(0, number - 1)  # 随机选择一个账号
    account = accounts[choice]
    while account.today_use_times >= account.today_use_limit:
        choice = randint(0, number - 1)
        account = accounts[choice]
    username = account.username
    password = b64decode(account.password)

    # 下载文件
    url = request.POST['url']
    # TODO url 不合法
    # https://download.csdn.net/download/weixin_44174032/10861867
    if not url.startswith('https://download.csdn.net/download/'):
        response = HttpResponseRedirect('/download')
        response.set_cookie('msg', 'url format error!')
        return response
    downloader = CsdnDownloader(username, password)
    path = downloader.download(url, local_path)
    if path:
        # 如果下载成功，返回文件
        file = open(path, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % path.split('/')[-1]

        # 如果第一次先免费下载
        if isfree:
            Account.objects.filter(id=id).update(free=False)
        else:
            # 下载次数 - 1
            obj = DownloadTimes.objects.get(id=id)
            obj.times = times - 1
            obj.save()

            # 增加下载记录
            DownloadLog(id=act_obj, url=url).save()
        return response
    response = HttpResponseRedirect('/download')
    response.set_cookie('msg', 'download failed, please contact with administrator!')
    return response


def solve_logout(request):
    response = HttpResponseRedirect("/login")
    response.delete_cookie('id')
    return response


def recharge(request):
    # 如果 cookie 过期，则跳转到登录界面
    if request.COOKIES.get('id') is None:
        return render(request, 'login.html')
    id = request.COOKIES['id']
    download_times = DownloadTimes.objects.get(id=id).times
    print(locals())
    return render(request, 'recharge.html', locals())


def solve_recharge(request):
    # TODO 卡密充值过了还能继续使用

    # 如果 cookie 过期，则跳转到登录界面
    if request.COOKIES.get('id') is None:
        return render(request, 'login.html')
    id = request.COOKIES['id']
    key = request.POST['key']

    # 先根据 key 找到商品的 gid
    flt_lst = DbKm.objects.filter(km=key)
    if len(flt_lst) == 0:
        # 卡密无效
        response = HttpResponseRedirect('/download')
        response.set_cookie('msg', 'invalid key!')
        return response
    gid = flt_lst[0].gid

    # 再根据 gid 确定充次
    dic = {3: 1, 15: 2, 16: 5, 19: 10, 14: 50, 8: 100, 9: 200}
    add_times = dic[gid]

    # 增加表中的账户的下载次数
    times = DownloadTimes.objects.get(id=id).times
    DownloadTimes.objects.filter(id=id).update(times=times+add_times)
    # 用完的卡密改为 null 的 base64 加密结果
    DbKm.objects.filter(km=key).update(km='bnVsbA==')
    response = render(request, 'download.html', {'id': id, 'download_times': times + add_times})
    response.set_cookie('msg', 'recharge success', expires=2)
    return response

