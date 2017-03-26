#!/usr/bin/env python
#coding=utf_8

import httplib

url = '/api/login/?id=1&password=pbkdf2_sha256$12000$XWiaV5T31xji$d/Bk4bCtA1IYLojlaz3If+bVBmIVWtNOUMNB+EdRywE='
url1 = '/api/login/?id=1&password=123'

httpClient = None

try:
    httpClient = httplib.HTTPConnection('127.0.0.1', 8001)
    httpClient.request('GET', url1)

    #response是HTTPResponse对象
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()

except Exception,e:
    print e
finally:
    if httpClient:
        httpClient.close()