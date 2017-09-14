# encoding=utf-8

import urllib2
import urllib
import cookielib
import logging
import lxml.html
import os


class WSpider(object):
    def __init__(self):
        # init cookie
        self.cookiejar = cookielib.LWPCookieJar()
        # self.cookiejar = cookielib.MozillaCookieJar(filename)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        # set global open
        urllib2.install_opener(self.opener)

    def getHtmlText(self, url, postdata=None, referer=''):

        header = {
            'Referer': referer,
        }
        if postdata == None:
            request = urllib2.Request(url, headers=header)
        else:
            request = urllib2.Request(url, urllib.urlencode(postdata), headers=header)
        response = self.opener.open(request)

        return response.read(), response.code, response.geturl()

    # save captcha or student picture in places
    def savePicture(self, picture_url, outpath, save_mode='wb'):
        try:
            picture = self.opener.open(picture_url).read()
        except Exception as e:
            print '============================='
            print 'Error Ouccurred:', picture_url
            print e
            print '============================='
            return

        local = open(outpath, save_mode)
        local.write(picture)
        local.close()

    def parse_form(self, html):
        tree = lxml.html.fromstring(html)
        data = {}
        for e in tree.cssselect('form input'):
            if e.get('name'):
                data[e.get('name')] = e.get('value')
        return data

    """#EXAMPLE
    logger = createLogger('mylogger', 'temp/logger.log')
    logger.debug('logger debug message')
    logger.info('logger info message')
    logger.warning('logger warning message')
    logger.error('logger error message')
    logger.critical('logger critical message')
    """

    def createLogger(self, logger_name, log_file):
        # 创建一个logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 定义handler的输出格式formatter
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
