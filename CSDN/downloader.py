from bs4 import BeautifulSoup
import re
import os
import requests
import json


class CsdnDownloader:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    driver = None
    action = None

    # 会话
    __session = requests.session()
    # 下载次数
    download_count = 0
    # 是否登录
    __is_logined = False
    __login_url = "https://passport.csdn.net/account/login"

    def download(self, remote_url, local_dir):

        # 1.是否登录
        if not self.__is_logined:
            self.__login()

        # 下载次数+1
        self.download_count += 1

        count = 0
        while count < 3:
            count += 1

            # 2.解析真实下载URL
            html_text = self.__session.get(remote_url).text
            html = BeautifulSoup(html_text, "html5lib")
            real_url = html.find("a", id="vip_btn").attrs["href"]

            # 3.下载
            source = self.__session.get(real_url)

            # 3.1获取下载名
            filename = re.findall(r".*\"(.*)\"$", source.headers.get("Content-Disposition", "\"None\""))[0]
            if filename == "None":
                continue
            filename = re.sub("\s", "_", filename)

            # 3.2创建本地文件
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            _local_path = local_dir + filename

            # 3.3分段下载
            local_file = open(_local_path.encode("utf-8"), "wb")
            for file_buffer in source.iter_content(chunk_size=512):
                if file_buffer:
                    local_file.write(file_buffer)
            return _local_path

        return None

    def __login(self):
            data = {"loginType": "1", "pwdOrVerifyCode": self.__password, "userIdentification": self.__username}

            jsontext=json.dumps(data)
            print(jsontext)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            }
            url='https://passport.csdn.net/v1/register/pc/login/doLogin'
            session=requests.session()
            response = session.post(url, data=jsontext, headers=headers, verify=False)

            # 3.保存cookies
            self.__session.cookies = response.cookies
            self.__is_logined = True
