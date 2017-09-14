# encoding=utf-8

import lxml.html
import urllib2
import urllib

import cookielib
import pprint

HOMEPAGE = 'http://jwgl1.hbnu.edu.cn'


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
response = opener.open(HOMEPAGE)
html = response.read()
LOGIN_URL = response.geturl()
print 'LOGIN_URL', LOGIN_URL
print '==========================='

data = parse_form(html)
pprint.pprint(data)
data['txtUserName'] = raw_input("Please input account name:")
data['TextBox2'] = raw_input("Please input password:")
# data['txtUserName'] = 'lwh'
data['TextBox2'] = '********'
data['RadioButtonList1'] = unicode('部门', 'utf8').encode('gbk')

data['txtSecretCode'] = raw_input('请输入验证码：')
data['lbLanguage'] = ''

encoded_data = urllib.urlencode(data)

print encoded_data

request = urllib2.Request(LOGIN_URL, encoded_data)
response = opener.open(request)
finalurl = response.geturl()
print 'FINAL_URL', finalurl

resText = unicode(response.read(), 'gb2312').encode("utf-8")

print resText
print response.code
print '=========================================================================='
# ============================
print '打开学生第二个页面'

header = {
    'Referer': finalurl,
}

secret = finalurl[finalurl.index('('):finalurl.index(')') + 1]
# 学生信息查询
template_url = 'http://jwgl1.hbnu.edu.cn/' + secret + '/xsxx.aspx?xh=lwh&xm=&gnmkdm=N120306'

# template_url = finalurl + '&xm=&gnmkdm=N120306'
template_url = finalurl[:finalurl.index(')') + 1] + '/xsxx.aspx?xh=lwh&xm=&gnmkdm=N120306'

print template_url

request = urllib2.Request(template_url, headers=header)
response = opener.open(request)

resText = unicode(response.read(), 'gb2312').encode("utf-8")

print resText
print response.code

# 查询某一学生信息

data = parse_form(resText)
data['TextBox1'] = '2011115010130'
data['Button3'] = unicode('查询', 'utf8').encode('gbk')
encoded_data = urllib.urlencode(data)
print encoded_data
request = urllib2.Request(template_url, encoded_data, header)
response = opener.open(request)
finalurl = response.geturl()

resText = unicode(response.read(), 'gb2312').encode("utf-8")
print 'finalfinalUrl: ' + finalurl
print resText


def savePicture(url, outpath, save_mode='wb'):
    picture = opener.open(url).read()  # 用openr访问验证码地址,获取cookie
    local = open(outpath, save_mode)
    local.write(picture)
    local.close()
    # resText = unicode(picture, 'gbk').encode("utf-8")
    print picture


imageUrl = 'http://jwgl1.hbnu.edu.cn/' + secret + '/readimagexs.aspx?xh=2011115010130'

savePicture(imageUrl, outpath="temp/student.jpg")
