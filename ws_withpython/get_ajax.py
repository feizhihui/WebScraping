# encoding=utf-8

import json
import string

template_url = 'http://example.webscraping.com/ajax/search.json?page{}&page_size=10&search_term={}'
countries = set()

for letter in string.lowercase:
    page = 0
    while 1:
        html = 'pass'
        try:
            ajax = json.loads(html)
        except ValueError as e:
            print e
            ajax = None
        else:
            for record in ajax['records']:
                countries.add(record['country'])
        page += 1
        if ajax is None or page >= ajax['num_pages']:
            break

open('countries.txt', 'w').write('\n'.join(sorted(countries)))
