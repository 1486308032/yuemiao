"""提交订单参数GET
https://wx.scmttec.com/subscribe/subscribe/add.do?
vaccineCode=0208
vaccineIndex=1
linkmanId=26605318
subscribeDate=2022-03-08
subscirbeTime=2004  # GET 选择时间段时 响应body的Data ID https://wx.scmttec.com/subscribe/subscribe/departmentWorkTimes2.do?depaCode=4202040003&vaccCode=0208&vaccIndex=1&subsribeDate=2022-03-10&departmentVaccineId=9904&linkmanId=26605318&idCardNo=421003200012253211
departmentVaccineId=9904
depaCode=4202040003_b3f3799d4320171be60039325023fa67   # 时间+subscirbeTime+abcd md5 2022030500482004fuckhacker10000
serviceFee=0
ticket=28331688:26605318:4202040003:9904___1646412476944
channelCode=yyymsg
idCardNo=421003200012253211
captchaVerification=captchaVerification=mLgqQeaWJEvA87kUTlgzQorjvrDQk4Q3XijOheMQmNpRe5ud/8W3PqiLXv2AN++cstPaDeR+5EFh4sx5vdhHmZhMmA+bHE32LXbYxv1Cra4=
    待加密文本：token+验证码坐标   9beeae52e806454c8afcc44d93abd762---{"x":164.96428571428572,"y":5}   密钥：5GDh59HsZQ8CaJtD
token=9beeae52e806454c8afcc44d93abd762
    # 响应body
{"code":"0000","msg":null,"data":{"subscribeId":null,"subNo":420019811712673280,"subNoStr":"420019811712673280","wxPrePayResponse":null},"ok":true,"notOk":false}

https://wx.scmttec.com/subscribe/subscribe/submitDetail.do?
subNo=420019811712673280

UUID随机生成的js代码 https://wx.scmttec.com/static/js/0.34dffafa46f5354e96b3.js
for (var t = [], e = 0; e < 36; e++)
    t[e] = "0123456789abcdef".substr(Math.floor(16 * Math.random()), 1);
t[14] = "4",
t[19] = "0123456789abcdef".substr(3 & t[19] | 8, 1),
t[8] = t[13] = t[18] = t[23] = "-";
var i = "slider-" + t.join("")
  , n = "point-" + t.join("");

"""





# def construct_departmentCode_32encode(subscirbeTime, now=None):
#     """
#     在立即预约的时候，传入的社区编号参数中不仅要传入社区编号，还有一个32位的编码字符需要构造。
#     这个32位的字符我猜测认为主要是防止用户点进去提交的界面后，两分钟之内如果没有提交则会过时，需要用户重新再次进去提交界面
#     depaCode=4101840004_4a4eccf02eda431817ae943d22d8bbc0
#     后面的4a4eccf02eda431817ae943d22d8bbc0这个数据没找到怎么生成的，估计是md5加密了，
#     看了js有这一段代码：
#         depaCode: this.submitInfo.department.code + "_" +
#                 f()(moment(new Date(this.submitInfo.nowTime)).format("YYYYMMDDHHmm") + this.submitInfo.subscirbeTime.value + this.abcde)
#     :param subscirbeTime: 选择的时间段，是编码过的时间段，具体可以参考 departmentWorkTimes2 返回的每一个时间段的 id 字段的值
#     :return: 返回构造的32位编码字符
#     """
#     end = 'fuckhacker10000'  # 在js文件中 https://cdn.scmttec.com/static/js/app.431ab7ea97d2f2ef6381.js
#     # 中间一步，构造编码的时间 depaCode=4101840004_4a4eccf02eda431817ae943d22d8bbc0
#     cur_time = get_server_time()  # 2021-01-14 16:37:10
#     cur_time = get_server_time_miaomiao()
#     # self._header['st'] = hashlib.md5(str(cur_time).encode('utf-8')).hexdigest()
#     # print("cur_time: ", cur_time)
#     # print("subscirbeTime id: ", subscirbeTime)
#     decodetime = cur_time.replace('-', '').replace(' ', '').replace(':', '')[0:12] + str(subscirbeTime) + end
#     # decodetime = cur_time + str(subscirbeTime) + end
#     # decodetime = str(now) + str(subscirbeTime) + end
#     depaCode_md5 = hashlib.md5(str(decodetime).encode('utf-8')).hexdigest()
#     # depaCode_md5 = hashlib.md5((depaCode_md5+'ux$ad70*b').encode('utf-8')).hexdigest()
#     print("decodetime_ori: ", decodetime)
#     print("depaCode_md5: ", depaCode_md5)
#     return depaCode_md5
if __name__ == '__main__':
    createUUID()
