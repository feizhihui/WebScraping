# encoding=utf8

import urllib
import collections


def _encode_params(**kw):
    def _encode(L, k, v):
        if isinstance(v, unicode):
            print 'unicode'
            L.append('%s=%s' % (k, urllib.quote(v.encode('utf-8'))))
        elif isinstance(v, str):
            print 'str'
            L.append('%s=%s' % (k, urllib.quote(v)))
        elif isinstance(v, collections.Iterable):
            for x in v:
                _encode(L, k, x)
        else:
            L.append('%s=%s' % (k, urllib.quote(str(v))))

    args = []
    for k, v in kw.iteritems():
        _encode(args, k, v)
    return '&'.join(args)


print _encode_params(button1='', RadioButtonList1='部门')
