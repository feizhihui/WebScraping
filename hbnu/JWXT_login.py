# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 17:07:17 2016

@author: liudiwei
"""
import getpass
import json
import urllib

from JWXTSpider import WSpider
import sys

type = sys.getfilesystemencoding()

print type


def zhiHuLogin():
    spy = WSpider()
    logger = spy.createLogger('mylogger', 'temp/logger.log')
    homepage = r"http://jwgl1.hbnu.edu.cn/"

    username = raw_input("Please input username: ")
    password = getpass.getpass("Please input your password: ")

    reurl = spy.getResponse(homepage).geturl()
    # 保存验证码
    logger.info("save captcha to local machine.")
    captchaURL = r"http://jwgl1.hbnu.edu.cn/(qnmphm45lksemgnjx0jlxk45)/CheckCode.aspx?%22%20onclick=%22reloadcode()"  # 验证码url
    spy.saveCaptcha(captcha_url=captchaURL, outpath="temp/captcha.jpg")  # 生成验证码图片

    # 请求的参数列表
    post_data = {
        'Button1': '',
        'RadioButtonList1': r'%E9%83%A8%E9%97%A8',
        'TextBox2': password,
        '_VIEWSTATE': 'dDwtMTMxNjk0NzYxNTs7PgsXsgF0WZgYxdSKS8zE4dNmne3H',
        'lbLanguage': '',
        'txtSecretCode': raw_input("Please input captcha: "),
        'txtUserName': username
    }

    # 请求的头内容
    header = {
        'Origin': 'http://jwgl1.hbnu.edu.cn/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }

    spy.setRequestData(reurl, post_data, header)
    resText, code, reurl = spy.getHtmlText(is_cookie=True)

    print '3.2', spy.cookiejar
    # resText.decode('GB2312').encode(type)
    resText = unicode(resText, "gb2312").encode("utf-8")
    print resText
    print 'Reuturn Code:', code
    print reurl
    jsonText = json.loads(resText)

    if jsonText["r"] == 0:
        logger.info("Login success!")
    else:
        logger.error("Login Failed!")
        logger.error("Error info ---> " + jsonText["msg"])

    text = spy.opener.open(homepage).read()  # 重新打开主页，查看源码可知此时已经处于登录状态
    spy.output(text, "out/home.html")  # out目录需手动创建


if __name__ == '__main__':
    zhiHuLogin()
