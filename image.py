import cv2


def tran_canny(image):
    """消除噪声"""
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def showImage(image):
    return 0
    cv2.imshow("pic", image)
    cv2.waitKey(0)
    cv2.destroyWindow("pic")


def readImage(background_path="./1.png", slider_path="./2.png"):
    background = cv2.imread(background_path, 0)
    # cv2.resize(background,)
    slider = cv2.imread(slider_path, 0)
    # showImage(background)
    # showImage(slider)
    res = cv2.matchTemplate(tran_canny(slider), tran_canny(background), cv2.TM_CCOEFF_NORMED)  # 匹配验证
    res2 = cv2.minMaxLoc(res, mask=None)  # 取匹配值
    max_loc = res2[3]  # 最佳值
    # print(res2)
    x, y = max_loc  # 获取x,y位置坐标
    w, h = slider.shape[::-1]  # 宽高
    cv2.rectangle(background, (x, y), (x + w, y + h), (7, 249, 151), 2)
    showImage(background)
    print("image：验证码坐标", x * 0.5)
    # return x * 0.49 - 3
    return x * 0.5


if __name__ == '__main__':
    readImage()
