#!/usr/bin/env python
#coding=utf_8
import httplib, urllib

httpClient = None
try:
    params = urllib.urlencode({"id": "1","password": "pbkdf2_sha256$12000$XWiaV5T31xji$d/Bk4bCtA1IYLojlaz3If+bVBmIVWtNOUMNB+EdRywE="})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    httpClient = httplib.HTTPConnection("127.0.0.1", 8001)
    httpClient.request("POST", "/api/login/", params,headers)

    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders() #获取头信息
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()