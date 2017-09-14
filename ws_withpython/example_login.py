# encoding=utf-8

# encoding=utf-8

import lxml.html
import urllib2
import urllib

import cookielib
import pprint

HOMEPAGE = 'http://example.webscraping.com/user/login'


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

data = parse_form(html)
pprint.pprint(data)
data['email'] = '22123@outlook.com'
data['password'] = 'poiu1234'

encoded_data = urllib.urlencode(data)

print cj

request = urllib2.Request(HOMEPAGE, encoded_data)
response = opener.open(request)
print 'FINAL_URL', response.geturl()

resText = unicode(response.read(), 'gb2312').encode("utf-8")

print resText
print response.code
print cj

fw = open('out/login.html', 'w')
fw.write(resText)
fw.close()

# ============================

import json
import string

template_url = 'http://example.webscraping.com/ajax/search.json?page={}&page_size=10&search_term={}'
countries = set()

for letter in string.lowercase:
    page = 0
    while True:
        response = opener.open(template_url.format(page, letter))
        try:
            ajax = json.loads(response.read())
        except ValueError as e:
            print e
            ajax = None
        else:
            for record in ajax['records']:
                countries.add(record['country'])
        page += 1
        if ajax is None or page >= ajax['num_pages']:
            break

        print ajax
        print letter, page, ajax['num_pages']

open('countries.txt', 'w').write('\n'.join(sorted(countries)))
