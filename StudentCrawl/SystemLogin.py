# encoding=utf-8
from Spider import WSpider
import lxml
from Bean import Person
import os


class DataSearch(object):
    def __init__(self, loginURL):
        self.HOMEPAGE = loginURL
        self.currentURL = loginURL
        self.spider = WSpider()
        self.sid = {}
        self.info_table = {}  # stuid:Person represent the record existence
        # self.img_table = {}  # stuid:name represent the record existence

    def showHtml(self, htmlPage):
        return unicode(htmlPage, 'gb2312', errors='ignore').encode('utf-8')

    def login_system(self):
        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(self.currentURL)
        print nextUrl
        data = self.spider.parse_form(htmlPage)
        data['txtUserName'] = 'lwh'
        data['TextBox2'] = 'poiu1234'
        data['RadioButtonList1'] = unicode('部门', 'utf8').encode('gbk')
        data['txtSecretCode'] = raw_input('请输入验证码：')
        data['lbLanguage'] = ''

        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(nextUrl, postdata=data)

        # if login success
        self.secretKey = nextUrl[nextUrl.index('('):nextUrl.index(')') + 1]
        self.currentURL = nextUrl

        print '===========LOGIN INFORMAION============='
        print stateCode
        print self.showHtml(htmlPage)

    def download_studentinfo(self, stuid):
        # step in lookup page
        url = self.HOMEPAGE + ds.secretKey + '/xsxx.aspx?xh=lwh&xm=&gnmkdm=N120306'
        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(url, referer=self.currentURL)

        # look up all students' information by college
        data = self.spider.parse_form(htmlPage)
        data['TextBox1'] = stuid
        data['DropDownList1'] = 'a.xh'
        data['Button3'] = unicode('查询', 'utf8').encode('gbk')

        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(url, postdata=data, referer=self.currentURL)

        tree = lxml.html.fromstring(self.showHtml(htmlPage))
        xh = tree.cssselect('td > span#xh')[0].text
        xm = tree.cssselect('td > span#xm')[0].text
        xb = tree.cssselect('td > span#xb')[0].text
        csrq = tree.cssselect('td > span#csrq')[0].text
        mz = tree.cssselect('td > span#mz')[0].text
        xy = tree.cssselect('td > span#xy')[0].text
        zymc = tree.cssselect('td > span#zymc')[0].text
        xzb = tree.cssselect('td > span#xzb')[0].text
        sfzh = tree.cssselect('td > span#sfzh')[0].text
        p = Person(stuid=xh, name=xm, gender=xb, birth=csrq, nation=mz, college=xy, major=zymc, aclass=xzb, idcard=sfzh)
        print xh, stuid
        try:
            assert xh == stuid
        except AssertionError as e:
            print e
        self.info_table[xh] = p

    def download_studentimg(self, root_dir):
        # http://jwgl1.hbnu.edu.cn/(dmrmuuy421uhfi55au0ot245)/readimagexs.aspx?xh=2007215210424
        for college, rows in self.sid.items():

            pic_dir = root_dir + college + '/'
            if not os.path.isdir(pic_dir):
                os.mkdir(pic_dir)

            for row in rows:
                # only save these unsaved before
                stuid = row[0]
                pictureUrl = self.HOMEPAGE + self.secretKey + '/readimagexs.aspx?xh=' + stuid
                outpath = pic_dir + row[0] + '.jpg'
                self.spider.savePicture(pictureUrl, outpath)
                print 'save:', row[0], row[1]

    def download_studentid(self, college):

        # step in lookup page
        url = self.HOMEPAGE + ds.secretKey + '/xsxx.aspx?xh=lwh&xm=&gnmkdm=N120306'
        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(url, referer=self.currentURL)

        # look up all students' information by college
        data = self.spider.parse_form(htmlPage)
        data['TextBox1'] = unicode(college, 'utf8').encode('gb2312')
        data['DropDownList1'] = 'a.xy'
        data['Button3'] = unicode('查询', 'utf8').encode('gbk')

        htmlPage, stateCode, nextUrl = self.spider.getHtmlText(url, postdata=data, referer=self.currentURL)

        print '==============信息页面====================='
        tree = lxml.html.fromstring(self.showHtml(htmlPage))
        data = {}
        k = 0
        for e in tree.cssselect('select option'):
            if e.getparent().get('name') == 'DropDownList2':
                content = e.text.encode('utf8')
                data[k] = content.split('||')
                k += 1
        self.sid[college] = data.values()


if __name__ == '__main__':
    loginURL = 'http://jwgl1.hbnu.edu.cn/'
    ds = DataSearch(loginURL)

    ds.login_system()

    collegeList = ['音乐学院']
    # set sid
    for college in collegeList:
        ds.download_studentid(college)

    # download all picture by sid
    ds.download_studentimg(r'/home/feizhihui/MyData/')
    # download each student information by student id
    for college, rows in ds.sid.items():
        for stuid in rows:
            print 'download information page：', stuid[0]
            ds.download_studentinfo(stuid[0])
