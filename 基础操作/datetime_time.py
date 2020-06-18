
#在Python中共有三种表达方式：
#1）timestamp 2）tuple或者struct_time 3）格式化字符串。
############strftime 可以理解为 str format time ,意为字符格式的时间
############strptime 可以理解为 str tuple time ,意为元组格式的时间（结构体时间）
############################################一、time模块的使用：####################################
#1、获取当前时间的时间戳，time.time() 
import time
#1、获取时间戳
time.time()   # 1542359416.0360363
#2、将时间戳转为结构体格式，time.localtime()
time.localtime(time.time())#time.struct_time(tm_year=2019, tm_mon=6, tm_mday=25, tm_hour=17, tm_min=38, tm_sec=52, tm_wday=1, tm_yday=176, tm_isdst=0)
#3、time.mktime(t)：将一个struct_time转化为时间戳。
time.mktime(time.localtime(time.time()))#1561455610.0
#4、获取当前时间的另一个格式。
time.ctime()  #一个时间戳转化为time.asctime()的形式:'Fri Nov 16 17:10:21 2018'
#5、将一个代表时间的元组或者struct_time，转化为格式化的时间字符串。time.strftime("%H:%M:%S",t)
time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#'2020-06-17 19:48:33"
#6、格式化的时间字符串转为struct_time，time.strptime(t,"%H:%M:%S")
time.strptime(time.strftime("%H:%M:%S",time.localtime(time.time())),"%H:%M:%S")#time.struct_time(tm_year=1900, tm_mon=1, tm_mday=1, tm_hour=18, tm_min=2, tm_sec=36, tm_wday=0, tm_yday=1, tm_isdst=-1) ==>

############################################二、datetime模块的使用：####################################
#1、将时间戳转为本地时间，datetime.datetime.fromtimestamp(）。
import datetime
time.time()  # 1542415739.4501636
#1、将时间戳转化为datetime对象
datetime.datetime.fromtimestamp(time.time())  # datetime.datetime(2018, 11, 17, 8, 50, 44, 137584)
#2、将datetime对象转为时间戳
datetime.datetime.now().timestamp()
#3、当前本地时间的datetime对象
datetime.datetime.now()  #datetime.datetime(2018, 11, 17, 8, 59, 46, 505069)
#4、strftime('%Y-%m-%d %H:%M:%S')函数，时间转为年月日，时分秒。
datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #'2018-11-17 09:02:05'
#5、strptime方法，将年月日，时分秒转为datetime对象。
datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')


############################################二、dataframe举例：####################################
#一、时间戳转为'%Y-%m-%d %H:%M:%S'。
#1：time.localtime，将时间戳转为结构体。2：time.strftime，将结构体转为日期时间
df['time'].apply(lambda x : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
aaa = 1592397180 #时间戳
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(aaa))  #'2020-06-17 20:33:00'

#二、'%Y-%m-%d %H:%M:%S'(日期时间)转为时间戳。
#1：日期时间格式转为datetime对象。2：datetime对象转时间戳
aaa2=datetime.datetime.strptime(datetime.datetime(2020, 6, 18, 5,0,0).strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')#'2020-06-18 05:00:00'
aaa2.timestamp() #转为时间戳


datetime.datetime.strptime(str(sell_record2.iloc[:,0][0]),'%Y-%m-%d %H:%M:%S')-datetime.timedelta(days=1)




url = 'https://www.aicoin.cn/api/chart/kline/setting/drawing'
hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36','Content-Length':'367','Accept-Encoding':'gzip, deflate, br',
      'Accept-Language':'zh-CN,zh;q=0.9','content-type':'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie':'GA1.2.2020834299.1588823932; __els__=1; _pk_id.2.f745=6fc35da00fe32622.1591754903.3.1591853086.1591853086.; _pk_ref.2.f745=%5B%22%22%2C%22%22%2C1591853086%2C%22https%3A%2F%2Fwww.aicoin.cn%2Fchart%2Fbitfinex_btc%22%5D; XSRF-TOKEN=eyJpdiI6IkhPV0xUSHJNbHhldEVBdm1wbDhKcUE9PSIsInZhbHVlIjoiVzNQbFwvdFlaOFdFWEJ0cWlJV3FcL2VIdHlBRnRyVkdySVd5VDd2WU1xK0FuOVRnN2lMNU93KzBBY1pEZVwvM2tmM0pDTWdEY0xaZEhXZXdxbXB1UjJRVVE9PSIsIm1hYyI6Ijk1MjNiMzZlMWI2MDI2MzhlYmY0NTcyNjQ2NjYxZTFiMmIyYzYxZDNkZjI2Zjk4MTZiZjZjYzcxZDc1MjA0YzgifQ%3D%3D; aicoin_token=VGOOCyuoENDurPlOtaEKoyMcIEXs4zgz%2FssY0KuWRgnoRG7etNISC4gQPM1K5iRp3vpjjV6s%2FuIXFrUwSGwxMp%2FJB1arlbqTl6k1SCFC%2FR7SwslQaIDT2GLX5B4nZ3a%2Bz5MZVwAkmE3muSStzzngbS5G7D7olBJ%2FLgciCk%2FFxguI%2BIKZzu%2BbsLkamA5%2BG5AodISNkKbztOOD6YWnSj3Mx73T8TuxR%2B0dFBFsUoWv628%3D; HWWAFSESID=d46c27ff3f005a1863; HWWAFSESTIME=1592277554099; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1590983460,1591754879,1591843567,1592277560; _pk_testcookie..undefined=1; _gid=GA1.2.302249551.1592277561; _pk_ses.2.57ea=1; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1592383305; aicoin_session=eyJpdiI6IkplN2NzMjhPUFh6RXlKdHVoNkV1RUE9PSIsInZhbHVlIjoiOUJPK1RPcFNvdlo3XC91K09tUUIwTTRkczRab092eDNpN3dhZCtnU2FuTnhDSnJXYktFVlVJSXVRaFVsRjNsMDF5TDl0aTk0R29ET1ZhaXZUSURlMzJRPT0iLCJtYWMiOiJjOWU4ZmQwYTM3MTdiZGJjM2Y1YjlmNWQ1ZmMxYWE0NGI5MmRkNTQwNzY1ZmI2NzEzMTNhZjJkNWMzZDA1NTY4In0%3D; _pk_id.2.57ea=365ae5012419d343.1588823932.19.1592384231.1592383146.',
      'Host':'www.aicoin.cn','Origin':'https://www.aicoin.cn','Referer':'https://www.aicoin.cn/chart/bitfinex_btc','x-requested-with':'XMLHttpRequest','x-xsrf-token':'eyJpdiI6IkhPV0xUSHJNbHhldEVBdm1wbDhKcUE9PSIsInZhbHVlIjoiVzNQbFwvdFlaOFdFWEJ0cWlJV3FcL2VIdHlBRnRyVkdySVd5VDd2WU1xK0FuOVRnN2lMNU93KzBBY1pEZVwvM2tmM0pDTWdEY0xaZEhXZXdxbXB1UjJRVVE9PSIsIm1hYyI6Ijk1MjNiMzZlMWI2MDI2MzhlYmY0NTcyNjQ2NjYxZTFiMmIyYzYxZDNkZjI2Zjk4MTZiZjZjYzcxZDc1MjA0YzgifQ=='}
for i in range(len(sell_record2.index)):
    if sell_record2.iloc[:,0][i].hour>7:
        buy_time_to_draw =str((int(datetime.datetime.strptime(sell_record2.iloc[:,0][i].strftime('%Y-%m-%d'),'%Y-%m-%d').timestamp())+28800)*1000)
    else:
        buy_time_to_draw = str((int((datetime.datetime.strptime(sell_record2.iloc[:,0][i].strftime('%Y-%m-%d'),'%Y-%m-%d')-datetime.timedelta(days=1)).timestamp())+28800)*1000)
    buy_price_to_draw = str(sell_record2.iloc[:,3][i])
    buy_price_to_draw_low = str(int(float(buy_price_to_draw)*0.93))
    data = {'points[0][x]':buy_time_to_draw,'points[0][y]':buy_price_to_draw_low,'points[0][s]':'0',
        'points[1][x]':buy_time_to_draw,'points[1][y]':buy_price_to_draw,'points[1][s]':'0',
        'options[isLocked]':'false','options[lineWidth]':'3','options[lineColor]':'rgba(245,33,45,1)',
        'options[lineDash][]':'0','name':'CArrowLineObject','symbol':'btc:bitfinex'}
    r = requests.post(url,headers=hd,data=data ,timeout=10)

















