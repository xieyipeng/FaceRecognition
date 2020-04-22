import pandas as pd
import numpy as np
from PIL import Image
import os
import imageio

import matplotlib
import numpy as np


import matplotlib.pyplot as pyplot

emotions = {
    '0': 'anger',
    '1': 'disgust',  # 厌恶
    '2': 'fear',  # 恐惧
    '3': 'happy',
    '4': 'sad',
    '5': 'surprised',
    '6': 'normal'
}


# 创建文件夹
def create_dir(dir):
    if os.path.exists(dir) is False:
        os.makedirs(dir)


# 读取出图片
def save_image_fer2013(fer_2013):
    data = pd.read_csv(fer_2013)
    count = 0
    for index in range(len(data)):
        emotion_data = data.loc[index][0]
        image_data = data.loc[index][1]
        usage_data = data.loc[index][2]

        data_array = list(map(float, image_data.split()))
        data_array = np.asarray(data_array)
        image_reshape = data_array.reshape(48, 48)
        image = Image.fromarray(image_reshape)
        print(image)

        dir_name = usage_data
        emotion_name = emotions[str(emotion_data)]

        image_path = os.path.join(dir_name, emotion_name)

        create_dir(dir_name)
        create_dir(image_path)

        image_name = os.path.join(image_path, str(index) + '.jpg')
        print(image_name)
        # image.convert('RGB').save(image_name, format="RGB")
        matplotlib.image.imsave(image_name, image)

        count = index
    print(count)


if __name__ == '__main__':
    file = '/home/xieyipeng/code/dataset/FER2013/fer2013/fer2013.csv'
    save_image_fer2013(file)
