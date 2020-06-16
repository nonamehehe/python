# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:13:38 2020

@author: Administrator
"""
import requests
import json
url = 'https://www.aicoin.cn/api/chart/kline/setting/drawing'
#文件头
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
payload = {'POST': 'https://www.aicoin.cn/api/chart/kline/setting/drawing HTTP/1.1', 'Host': 'www.aicoin.cn','Connection': 'keep-alive','Content-Length': '371','Origin': 'https://www.aicoin.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           }#'key2': 'value2','key2': 'value2'}

r = requests.post(url,data=payload)
r = requests.post(url,data=json.dumps(payload))

print(r.text)
r
