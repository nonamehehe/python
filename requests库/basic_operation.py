# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:13:38 2020

@author: Administrator
"""
import requests
import json
url = 'https://www.aicoin.cn/api/chart/kline/setting/drawing'

response = requests.head(url)
r= requests.post(url, data=payload)
#文件头
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
payload = {'Host': 'www.aicoin.cn','Connection': 'keep-alive','Content-Length': '371','Origin': 'https://www.aicoin.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           }#'key2': 'value2','key2': 'value2'}

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh,zh-CN;q=0.9','Connection':'keep-alive','Cookie':'_ga=GA1.2.2020834299.1588823932; __els__=1; _pk_id.2.f745=6fc35da00fe32622.1591754903.3.1591853086.1591853086.; _pk_ref.2.f745=%5B%22%22%2C%22%22%2C1591853086%2C%22https%3A%2F%2Fwww.aicoin.cn%2Fchart%2Fbitfinex_btc%22%5D; XSRF-TOKEN=eyJpdiI6IkhPV0xUSHJNbHhldEVBdm1wbDhKcUE9PSIsInZhbHVlIjoiVzNQbFwvdFlaOFdFWEJ0cWlJV3FcL2VIdHlBRnRyVkdySVd5VDd2WU1xK0FuOVRnN2lMNU93KzBBY1pEZVwvM2tmM0pDTWdEY0xaZEhXZXdxbXB1UjJRVVE9PSIsIm1hYyI6Ijk1MjNiMzZlMWI2MDI2MzhlYmY0NTcyNjQ2NjYxZTFiMmIyYzYxZDNkZjI2Zjk4MTZiZjZjYzcxZDc1MjA0YzgifQ%3D%3D; aicoin_token=VGOOCyuoENDurPlOtaEKoyMcIEXs4zgz%2FssY0KuWRgnoRG7etNISC4gQPM1K5iRp3vpjjV6s%2FuIXFrUwSGwxMp%2FJB1arlbqTl6k1SCFC%2FR7SwslQaIDT2GLX5B4nZ3a%2Bz5MZVwAkmE3muSStzzngbS5G7D7olBJ%2FLgciCk%2FFxguI%2BIKZzu%2BbsLkamA5%2BG5AodISNkKbztOOD6YWnSj3Mx73T8TuxR%2B0dFBFsUoWv628%3D; HWWAFSESID=d46c27ff3f005a1863; HWWAFSESTIME=1592277554099; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1590983460,1591754879,1591843567,1592277560; _pk_testcookie..undefined=1; _pk_ses.2.57ea=1; _gid=GA1.2.302249551.1592277561; _gat_gtag_UA_108140256_2=1; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1592277568; aicoin_session=eyJpdiI6ImM2cWpIVHVyTkNKTEVIMldwdERObXc9PSIsInZhbHVlIjoicjR2MjV6NEhTc3JcL2tZa1A5XC83VlwvSnQ3NzFLbXE4UzU2SnpaSXF5M2l4anpXNHJqZjJsZ1o4YnhjUW9QS0RhS2NmZUJhUGtNNlVueGs5N3hRa3JWZlE9PSIsIm1hYyI6IjE5NGRlZjMxYmE3ODFmN2I1N2Q2NjMyN2YxYjBkYmM3OTE1YjFhOTE2MmNlZDAyNGExMzVjMDQwMGQyNWI3YTAifQ%3D%3D; _pk_id.2.57ea=365ae5012419d343.1588823932.14.1592277580.1592277560.','Host':'www.aicoin.cn'
          ,'If-None-Match':'W/"5e2-vo9g5b8dO6TKFJQqiDt+CtB+CUs"','Referer':'https://www.aicoin.cn/chart/bitfinex_btc','Sec-Fetch-Dest':'iframe'
          ,'Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

r = requests.post(url,headers=headers)
r = requests.post(url,data=payload)
r = requests.post(url,data=json.dumps(payload))

print(r.text)
r
data=json.dumps(payload)
r.status_code
