# 约苗微信公众号抢疫苗
关键参数已在代码中实现，需要改改才能用

image.py文件处理验证码base64

captcha.py处理滑块验证码
### main.py参数介绍
__value__ 中vaccineCode、linkmanId、departmentVaccineId必填

- subscribeDate会被getWorkDay()中__value__["subscribeDate"] = i[0]直接覆盖，填写无效。i[0]默认是最近的可选日期，如果可选日期中已过接种时间，会导致程序运行错误，改为i[1]即可设置为下一天。（例如1月1日 下午2点 有疫苗可选择，但程序运行时已经是下午4点，此时会选择1月1日，但没有时间可选。）

- linkmanId为账号中保存接种人信息的ID编号
