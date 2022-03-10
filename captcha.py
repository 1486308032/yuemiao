import base64
from Cryptodome.Cipher import AES


# import json
# import random
# from binascii import b2a_hex, a2b_hex

def b64ToImage(data=None):
    image = {
        "secretKey": "EC0bNq7knDiSjPRt",
        "originalImageBase64": "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\u003d",
        "jigsawImageBase64": "iVBORw0KGgoAAAANSUhEUgAAAF4AAAE2CAYAAADoAiXtAAADOElEQVR4Xu3Sba6bOhiF0c5/Vp1GJ9PKiqy4LyQH/BGws5a0f1ydAPZz++sXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKzn7xvxt3SQ4/7+s79SfJZK74LHid/Jmejid1ITvYwf38cBLdFzePErtIYXv0KP6Hmt4Z//+9rfdXvpgjFg7WpilaHju7L4zBLihVt2NNTzl9t3xJXie6Z25PJn9ipQGTA+c2RZfO+0akO8Whno+V/b39Usi3eYUs8weSPemZfEO0xrVKQRy+IdpjRT+LSlws8Uf5nwyWzhl4k/U/g04S/a9OEfV3iIl7vzsnifW3see3uhmTZF+FVil7tt+BVjl8vivS+zcuy424T/luB5twj/bdHTLg//TdFLscNHfUv0W8QurR7+dsGTb4ge73wLK4e/bfRk1fC3jp6sGP720RPhL7Ja+CmiJ4+jbi8w66YJnwh/EeEv8jju9hIzbqrwifAXEf4ijyNvLzLbsni/W1shfNp08VcJnzZd+FXiZ/GOt7VK+LTW+K3Pn7JS+LRSvOue8vf5+fibruIHV9ueeO9k77nYqtm7D66+o/fOYrsqRz9qj3UJL/j5NYcXvW5Z7HmI6G2rCi96+4S/aFls+5bwfXYqvOj9JvxFE/7ixca7Vgv/SvzdyMXGu644WO+V4v2S8u/x2RGL33/pUwcasVex93wqfvzuS584zIidiZ7l+CPufPo8ow4ycqcvGYy4b9WZZopfdcFgxH2rz1V7mFL824gl8ew1ep65+Uz5MFn8QPmhrHw2/q73yu/10OPMsUOz5yu34m+T/Ld4sJ579e1areftfZ5qrRf5ab0v+njj9js/LYvvu0zNJY5u1EWPnrkU33G5fLB46B4bdel35y3F527n3UVaNyJADlt+I4u/vbXyEr03Ksa0sUv5AjFaj00d5hOEv8iof/VZ/B6FEeHThP+B8Bd5JNqGa10Wv0dhRPg04X+Q/3XGcDUrxe+wI8eKIY+sFN/LAWXAGDeuFN9Dpf+z7ovPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATOwfzYslC2OZzFkAAAAASUVORK5CYII\u003d",
        "token": "8eb3f0d66ef24012a97006ad44e044545",
        "result": False
    }
    if data is not None:
        image = data
    origina = image["originalImageBase64"]
    jigsaw = image["jigsawImageBase64"]
    image_data = base64.b64decode(origina)
    image_data2 = base64.b64decode(jigsaw)
    with open('1.png', 'wb') as f:
        f.write(image_data)
    with open('2.png', 'wb') as f:
        f.write(image_data2)


def dePoint(point_str=None, key=None):
    point_str = point_str.encode("utf8")
    point_str = base64.b64decode(point_str)
    # if key is None:
    #     key = "EC0bNq7knDiSjPRt"
    aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    point_str = aes.decrypt(point_str)  # 解密
    print("解码坐标ALL：", point_str, "密钥：", key)
    try:
        point_str[int(point_str[-1])]
        point_str = point_str[:-int(point_str[-1])]
    except:
        pass
    finally:
        point_str = point_str.decode("utf8")
        # print("解码坐标：", point_str, "密钥：", key)
    return point_str


def enPoint(point_str=None, key=None, block_size=16):
    # if key == None:
    #     key = "EC0bNq7knDiSjPRt"
    # if point_str == None:
    #     point_str = 265.7142857142857
    aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    """
    with open("./1.txt", "w") as f:
        # raw_text = f.read().encode("utf8")
        num = random.uniform(0.1111111111111, 0.1115111111111)
        point_str = ("%.13f") % (float(point_str) + num)
        # print("验证码X坐标", point_str)
        raw_text = {"x": float(point_str) , "y": 5}
        raw_text = json.dumps(raw_text, separators=(',', ':'))  # python会加入空格，影响结果
        f.write(raw_text)
        raw_text = raw_text.encode("utf8")
        print("Raw编码后：", raw_text)
        # print(len(raw_text))
    """
    raw_text = point_str.encode("utf8")
    if (len(raw_text) % block_size != 0):
        print("开始填充Padding")
        pl = block_size - (len(raw_text) % block_size)
        padding = bytearray([pl for i in range(pl)])  # 填充字符
        raw_text += padding
    en_text = aes.encrypt(raw_text)  # AES加密文本
    en_text = base64.b64encode(en_text).decode("utf8")  # Base64加密
    print("加密文本：", en_text, "密钥：", key)
    dePoint(en_text, key)
    return en_text


if __name__ == '__main__':
    print("验证码")
    b64ToImage()