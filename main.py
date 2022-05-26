import json
import sys
import requests
import time
from hashlib import md5
import random
import captcha
import image

__value__ = {
    "vaccineCode": "0208",  # 0208
    "vaccineIndex": "1",  # 接种第几针
    "linkmanId": "26605318",  # 26605318
    "subscribeDate": "2022-05-27",
    "subscirbeTime": "2004  ",  # GET 选择时间段时 响应body的Data ID
    "departmentVaccineId": "9904",  # 9904 10339
    "depaCode": "4201050012",  # 4202040003_b3f3799d4320171be60039325023fa67
    # 时间+subscirbeTime+abcd md5 2022030500482004fuckhacker10000
    "serviceFee": "0",
    "ticket": "28331688:26605318:4202040003:9904___1646412476944",
    "channelCode": "yyymsg",
    "idCardNo": "4211234612321313", # 身份证号码
    "captchaVerification": "mLgqQeaWJEvA87kUTlgzQorjvrDQk4Q3XijOheMQmNpRe5ud/8W3PqiLXv2AN++cstPaDeR+5EFh4sx5vdhHmZhMmA+bHE32LXbYxv1Cra4=",
    # 待加密文本：token+验证码坐标   9beeae52e806454c8afcc44d93abd762---{"x":164.96428571428572,"y":5}   密钥：5GDh59HsZQ8CaJtD
    "token": "9beeae52e806454c8afcc44d93abd762",
}


def getConfig():
    head = {
        "Host": "wx.scmttec.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 ("
                      "KHTML, like Gecko) Version/4.0 Chrome/87.0.4240.99 XWEB/3225 MMWEBSDK/20220402 Mobile "
                      "Safari/537.36 MMWEBID/9813 MicroMessenger/8.1.22.2140(0x280016E6) WeChat/arm64 Weixin "
                      "NetType/4G Language/zh_CN ABI/arm64",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,"
                  "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 ",
        "x-requested-with": "com.tencent.mm",
        "referer": "https://wx.scmttec.com/index.html",
        "tk": "wxtoken:3117786a5086286af91ee9fe547793c8_e072d4f9ae73476bc59a8b86c8600d6d",
        "st": md5(time.strftime("%Y-%m-%d %H:%M:%S").encode("utf8")).hexdigest(),
        "cookie": "_xzkj_=wxtoken:3117786a5086286af91ee9fe547793c8_a8d19eae5badf2e1d8af10bda970967e",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    return head


def getIndex():
    url = "https://wx.scmttec.com/index.html"
    head = getConfig()
    r = requests.get(url, headers=head)
    r.encoding = "utf8"
    print(r.text)
    with open('./test.html', "w+", encoding="utf8") as f:
        f.write(r.text)


# 疫苗医院列表页面 经纬度：附近的医院，name：根据名称搜索
def getDepartments():
    url = "https://wx.scmttec.com/department/department/getDepartments.do"
    url2 = "http://httpbin.org/post"
    head = getConfig()
    data = {
        "offset": "0",
        "limit": "10",
        "name": "",
        "regionCode": "4202",
        "isOpen": "1",
        "longitude": "115.01461",
        "latitude": "30.210896",
        "sortType": "1",
        "vaccineCode": "",
        "customId": "30",
    }
    r = requests.post(url=url, headers=head, data=data)
    r.encoding = "utf8"
    print(r.text)
    a = json.loads(r.text)
    for i in a.get("data").get("rows"):
        name = i.get("name")
        vaccineName = i.get("vaccineName")
        code = i.get("code")
        address = i.get("address")
        depaVaccId = i.get("depaVaccId")
        print(address)


# 疫苗医院详情页面
def getBaseInfo():
    url = "https://wx.scmttec.com/base/departmentVaccine/item.do"
    data = {
        "id": __value__.get("departmentVaccineId"),
        "isShowDescribtion": "true",
        "showOthers": "true"
    }
    head = getConfig()
    r = requests.get(url, headers=head, params=data)
    r.encoding = "utf8"
    print(r.text)
    print(r.url)
    res = json.loads(r.text)
    __value__["vaccineCode"] = res["data"]["vaccineCode"]
    __value__["depaCode"] = res["data"]["departmentCode"]  # 待补充，提交订单需加时间戳md5
    print("当前选中：", res["data"]["departmentName"], res["data"]["name"])


# 账号下添加的用户身份信息
def findByUserId():
    url = "https://wx.scmttec.com/order/linkman/findByUserId.do"  # ?userId=28331687
    head = getConfig()
    r = requests.get(url, headers=head)
    a = json.loads(r.text)
    for i in a.get("data"):
        id = i.get("id")
        username = i.get("name")
        print(id, username)


# 能否订阅
def isCanSubscribe():
    url = "https://wx.scmttec.com/subscribe/subscribe/isCanSubscribe.do"
    head = getConfig()
    data = {  # 医院详情页面
        "id": __value__["departmentVaccineId"],  # 医院ID
        "depaCode": __value__["depaCode"],  # 行政区划代码
        "vaccineCode": __value__["vaccineCode"],  # 疫苗ID
        "linkmanId": __value__["linkmanId"],  # 用户身份ID

    }
    r = requests.get(url, headers=head, params=data)
    a = json.loads(r.text)
    i = a.get("data")
    canSubscribe = i.get("canSubscribe")
    ticket = i.get("ticket")
    __value__["ticket"] = ticket
    print("能否订阅:", canSubscribe, ticket)


# 订单页面 可选日期
def getWorkDay():
    url = "https://wx.scmttec.com/order/subscribe/workDaysByMonth.do"
    head = getConfig()
    data = {
        "depaCode": __value__["depaCode"],
        "linkmanId": __value__["linkmanId"],
        "vaccCode": __value__["vaccineCode"],
        "vaccIndex": __value__["vaccineIndex"],
        "departmentVaccineId": __value__["departmentVaccineId"],
        "month": "2022-05-1",

    }
    r = requests.get(url, headers=head, params=data)
    print("订单页面 可选日期", r.text)
    a = json.loads(r.text)
    i = a.get("data").get("dateList")
    __value__["subscribeDate"] = i[1]


# 订单页面 可选日期的具体时间
def getWorkTime():
    url = "https://wx.scmttec.com/subscribe/subscribe/departmentWorkTimes2.do"
    head = getConfig()
    data = {
        "depaCode": __value__["depaCode"],
        "vaccCode": __value__["vaccineCode"],
        "vaccIndex": __value__["vaccineIndex"],
        "subsribeDate": __value__["subscribeDate"],
        "departmentVaccineId": __value__["departmentVaccineId"],
        "linkmanId": __value__["linkmanId"],
        "idCardNo": __value__["idCardNo"],

    }
    r = requests.get(url, headers=head, params=data)
    print("具体日期：", r.text)
    a = json.loads(r.text)
    if a["ok"] == False:
        print(a["msg"])
    else:
        i = a.get("data").get("times").get("data")
        __value__["subscirbeTime"] = i[0]["id"]


# 随机生成UUID
def createUUID():
    uuid = []
    for i in range(36):
        j = random.randint(0, 15)
        uuid += "0123456789abcdef"[j]
    uuid[14] = "4"
    try:
        uuid[19] = int(uuid[19])
        # print("尝试",uuid[19])
    except:
        uuid[19] = random.randint(0, 9)
        # print("修改",uuid[19])
    uuid[19] = "0123456789abcdef"[3 & uuid[19] | 8]
    uuid[8] = uuid[13] = uuid[18] = uuid[23] = "-"
    return ("slider-" + "".join(uuid))


# 获取验证码
def getCaptcha():
    url = "https://wx.scmttec.com/captcha/captcha/v2/get.do"
    url2 = "http://httpbin.org/post"
    head = getConfig()
    timestamp = time.time()
    timestamp = int(timestamp * 1000)
    data = {
        "captchaType": "blockPuzzle",
        "clientUid": "slider-f893f399-33d9-485f-8b27-7327e8cb82c0",  # "slider-f893f399-33d9-485f-8b27-7327e8cb82c0"，此处可替换为createUUID()，随机一个UUID()
        "ts": int(timestamp)
    }
    r = requests.post(url, headers=head, json=data)
    a = json.loads(r.text)
    # print(r.text)
    i = a.get("data").get("repData")
    print("获取验证码：", i)
    __value__["token"] = i.get("token")
    return i


# 发送验证码
def checkCaptcha(token=None, point_text=None):
    url = "https://wx.scmttec.com/captcha/captcha/v2/check.do"
    head = getConfig()
    data = {
        "captchaType": "blockPuzzle",
        "pointJson": point_text,
        "token": token
    }
    r = requests.post(url, headers=head, json=data)
    a = json.loads(r.text)
    print("验证码结果：", r.text)
    i = a.get("data").get("repData")
    return i


# 验证码检验
def orderCheck():
    i = getCaptcha()
    captcha.b64ToImage(i)
    token = i.get("token")
    key = i.get("secretKey")
    # print("key ", key, "token ", token)
    x = image.readImage()
    num = random.uniform(0.5111111111111, 0.9115111111111)
    point_x = ("%.13f") % (float(x) + num)
    point_dict = {"x": float(point_x), "y": 5}
    raw_text = json.dumps(point_dict, separators=(',', ':'))  # python会加入空格，影响结果
    en_point_text = captcha.enPoint(raw_text, key)
    res = checkCaptcha(point_text= en_point_text,token=token)
    # en_point_text = captcha.enPoint(x, key)
    # checkCaptcha(token, en_point_text)

    captchaVerification = captcha.enPoint(token + "---" + raw_text, key)
    __value__["captchaVerification"] = captchaVerification


def nowTime():
    url = "https://wx.scmttec.com/base//time/now.do"
    head = getConfig()
    r = requests.get(url, headers=head)
    time = json.loads(r.text).get("data")
    return time


"""----------------提交购买参数----------------"""


def subscribeAdd():
    url = "https://wx.scmttec.com/subscribe/subscribe/add.do"
    end = 'fuckhacker10000'
    head = getConfig()
    data = __value__
    # times = nowTime()
    # times = times.replace('-', '').replace(' ', '').replace(':', '')[0:12]
    times = time.strftime("%Y%m%d%H%M")
    times = times + str(__value__["subscirbeTime"]) + end
    times = md5(times.encode("utf8")).hexdigest()
    data["depaCode"] = data["depaCode"] + "_" + times
    while True:
        if int(time.strftime("%H%M%S")) > int("163000") or 1:
            r = requests.get(url, headers=head, params=data)
            break
        else:
            print("等待提交订单")
    print("购买结果", r.text)
    return r.text


def startSubscribe():
    getBaseInfo()
    isCanSubscribe()
    if int(time.strftime("%H%M%S")) > int("163000") or 1: #简单的时间控制，16点30分00秒之后开始运行，or 1 则忽略时间直接运行
        getWorkDay()
        getWorkTime()
        # orderCheck()
        res = subscribeAdd()
        return res


if __name__ == '__main__':

    orderCheck()
    i = 0
    while True:
        i = i + 1
        if int(time.strftime("%H%M%S")) >= int("162958") or 1:#简单的时间控制，16点29分58秒之后开始运行，or 1 则忽略时间直接运行
            try:
                time.sleep(0.2)
                print("[Info]:尝试运行")
                res = startSubscribe()
                res = json.loads(res)
            except BaseException as e:
                with open("out.log", "a+", encoding="utf8") as f:
                    print("[Error]：跳过循环", sys.exc_info())
                    print("[Error]：跳过循环", sys.exc_info(), file=f)
                    time.sleep(5)
                continue
            if res["code"] == "0000" or res["code"] == "9999":
                print("[Success]：退出循环")
                break
            else:
                print(res["msg"])
        else:
            print("<", i)
    print(__value__)
