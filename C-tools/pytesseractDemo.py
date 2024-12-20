import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# 设置 Tesseract 的安装路径（根据实际路径进行修改）
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


# 读取图像并进行预处理
def preprocess_image(image_path, crop_box=None):
    # 绿字黑底图片处理为黑白
    try:
        # 使用 OpenCV 读取图像
        image = cv2.imread(image_path)

        # 如果传入了裁剪框，就进行裁剪
        if crop_box:
            image = image[crop_box[1]:crop_box[3], crop_box[0]:crop_box[2]]

        # 将图像从 BGR 转为 HSV 色彩空间
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 定义绿色的 HSV 范围（这些值可以根据实际情况调整）
        lower_green = np.array([35, 40, 40])  # 绿色的最低阈值
        upper_green = np.array([85, 255, 255])  # 绿色的最高阈值

        # 根据绿色范围创建掩码
        mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # 创建一个黑色图像
        result = np.zeros_like(image)

        # 将绿色部分复制到黑色图像上
        result[mask > 0] = image[mask > 0]

        # 将绿色部分变为白色（或灰色）
        image[mask > 0] = [255, 255, 255]  # 将绿色部分设置为白色

        # 转换回 PIL 图像
        processed_image = Image.fromarray(image)

        # 可选：图像增强
        enhancer = ImageEnhance.Contrast(processed_image)
        processed_image = enhancer.enhance(2)  # 增强对比度

        # 可选：应用模糊滤镜（有时能去除噪点）
        processed_image = processed_image.filter(ImageFilter.MedianFilter(3))

        return processed_image
    except Exception as e:
        print(f"处理图像时出错: {e}")
        return None


# 提取图像中的文本
def extract_text_from_image(image):
    try:
        # 使用 pytesseract 提取文本
        text = pytesseract.image_to_string(image)
        text.replace(".","")
        text.replace("\n","")
        return text.replace(" ", "")  # 去掉多余的空格
    except Exception as e:
        print(f"提取文本时出错: {e}")
        return ""


def getGrade(image_path):
    crop_box = (830, 45, 890, 110)  # 如果需要裁剪，提供裁剪框（x1, y1, x2, y2）

    # 图像预处理
    processed_image = preprocess_image(image_path, crop_box)

    if processed_image:
        # 显示预处理后的图像
        # processed_image.show()

        # 提取文本
        text = extract_text_from_image(processed_image)

        # 输出提取的文本
        print("提取的文本：")
        print(text)
        return text
    else:
        print("图像处理失败，无法提取文本。")

def getName(image_path):
    crop_box = (255, 122, 700, 180)  # 如果需要裁剪，提供裁剪框（x1, y1, x2, y2）
    processed_image = Image.open(image_path)
    processed_image = processed_image.crop(crop_box)
    if processed_image:
        # 显示预处理后的图像
        # processed_image.show()

        # 提取文本
        text = extract_text_from_image(processed_image)

        # 输出提取的文本
        print("提取的文本：")
        print(text)
        return text
    else:
        print("图像处理失败，无法提取文本。")


