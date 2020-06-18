# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:13:38 2020

@author: Administrator
"""
import requests
import json
#########################get基础操作#####################################
#地址
#url = 'https://www.aicoin.cn/api/chart/kline/setting/drawing'
url = 'https://www.aicoin.cn/chart/bitfinex_btc'
#获取网页信息
r= requests.get(url)
#编码方式
r.encoding= r.apparent_encoding    #r.encoding = r.apparent_encoding
#解析备选编码方式
r.apparent_encoding
#链接状态
r.status_code   #418反爬
#查看请求头
r.request.headers
#更改User-Agent防止网站反爬
kv = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
r= requests.get(url,headers=kv )
r.status_code
r.request.headers
#查看网页文本信息
r.text  
#########################post基础操作#####################################
#地址
url = 'https://www.aicoin.cn/api/chart/kline/setting/drawing'
#更改User-Agent防止网站反爬
hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36','Content-Length':'367','Accept-Encoding':'gzip, deflate, br',
      'Accept-Language':'zh-CN,zh;q=0.9','content-type':'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie':'GA1.2.2020834299.1588823932; __els__=1; _pk_id.2.f745=6fc35da00fe32622.1591754903.3.1591853086.1591853086.; _pk_ref.2.f745=%5B%22%22%2C%22%22%2C1591853086%2C%22https%3A%2F%2Fwww.aicoin.cn%2Fchart%2Fbitfinex_btc%22%5D; XSRF-TOKEN=eyJpdiI6IkhPV0xUSHJNbHhldEVBdm1wbDhKcUE9PSIsInZhbHVlIjoiVzNQbFwvdFlaOFdFWEJ0cWlJV3FcL2VIdHlBRnRyVkdySVd5VDd2WU1xK0FuOVRnN2lMNU93KzBBY1pEZVwvM2tmM0pDTWdEY0xaZEhXZXdxbXB1UjJRVVE9PSIsIm1hYyI6Ijk1MjNiMzZlMWI2MDI2MzhlYmY0NTcyNjQ2NjYxZTFiMmIyYzYxZDNkZjI2Zjk4MTZiZjZjYzcxZDc1MjA0YzgifQ%3D%3D; aicoin_token=VGOOCyuoENDurPlOtaEKoyMcIEXs4zgz%2FssY0KuWRgnoRG7etNISC4gQPM1K5iRp3vpjjV6s%2FuIXFrUwSGwxMp%2FJB1arlbqTl6k1SCFC%2FR7SwslQaIDT2GLX5B4nZ3a%2Bz5MZVwAkmE3muSStzzngbS5G7D7olBJ%2FLgciCk%2FFxguI%2BIKZzu%2BbsLkamA5%2BG5AodISNkKbztOOD6YWnSj3Mx73T8TuxR%2B0dFBFsUoWv628%3D; HWWAFSESID=d46c27ff3f005a1863; HWWAFSESTIME=1592277554099; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1590983460,1591754879,1591843567,1592277560; _pk_testcookie..undefined=1; _gid=GA1.2.302249551.1592277561; _pk_ses.2.57ea=1; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1592383305; aicoin_session=eyJpdiI6IkplN2NzMjhPUFh6RXlKdHVoNkV1RUE9PSIsInZhbHVlIjoiOUJPK1RPcFNvdlo3XC91K09tUUIwTTRkczRab092eDNpN3dhZCtnU2FuTnhDSnJXYktFVlVJSXVRaFVsRjNsMDF5TDl0aTk0R29ET1ZhaXZUSURlMzJRPT0iLCJtYWMiOiJjOWU4ZmQwYTM3MTdiZGJjM2Y1YjlmNWQ1ZmMxYWE0NGI5MmRkNTQwNzY1ZmI2NzEzMTNhZjJkNWMzZDA1NTY4In0%3D; _pk_id.2.57ea=365ae5012419d343.1588823932.19.1592384231.1592383146.',
      'Host':'www.aicoin.cn','Origin':'https://www.aicoin.cn','Referer':'https://www.aicoin.cn/chart/bitfinex_btc','x-requested-with':'XMLHttpRequest','x-xsrf-token':'eyJpdiI6IkhPV0xUSHJNbHhldEVBdm1wbDhKcUE9PSIsInZhbHVlIjoiVzNQbFwvdFlaOFdFWEJ0cWlJV3FcL2VIdHlBRnRyVkdySVd5VDd2WU1xK0FuOVRnN2lMNU93KzBBY1pEZVwvM2tmM0pDTWdEY0xaZEhXZXdxbXB1UjJRVVE9PSIsIm1hYyI6Ijk1MjNiMzZlMWI2MDI2MzhlYmY0NTcyNjQ2NjYxZTFiMmIyYzYxZDNkZjI2Zjk4MTZiZjZjYzcxZDc1MjA0YzgifQ=='}

#需要添加的主题内容
#hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36','Content-Length':'367','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh;q=0.9','content-type':'application/x-www-form-urlencoded;charset=UTF-8'}
data = {'points[0][x]':'1591315200000','points[0][y]':'8950.13911268169','points[0][s]':'0',
        'points[1][x]':'1591315200000','points[1][y]':'9147.12698850731','points[1][s]':'0',
        'options[isLocked]':'false','options[lineWidth]':'4','options[lineColor]':'rgba(245,33,45,1)',
        'options[lineDash][]':'0','name':'CArrowLineObject','symbol':'btc:bitfinex'}
#向网页添加信息
r = requests.post(url,headers=hd,data=data ,timeout=10)

r.status_code
print(r.text)




















