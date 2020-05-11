import cv2
from keras.models import load_model
import numpy as np
from statistics import mode
from utils import preprocess_input

detection_model_path = 'detection_models/haarcascade_frontalface_default.xml'
classification_model_path = 'trained_models/simpler_CNN.100-0.64.hdf5'

frame_window = 10

emotion_labels = {0: 'angry', 1: 'disgust', 2: 'sad', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

# 加载人脸检测模型
face_detection = cv2.CascadeClassifier(detection_model_path)

# 加载表情识别
emotion_classifier = load_model(classification_model_path)

emotion_window = []
# 调起摄像头
video_capture = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.startWindowThread()
cv2.namedWindow('window_frame')

while True:
    # 读取一帧
    _, frame = video_capture.read()
    # 获得灰度图，并且在内存中创建一个图像对象
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 获取当前帧中的全部人脸
    faces = face_detection.detectMultiScale(gray, 1.3, 5)
    # 对于所有发现的人脸
    for (x, y, w, h) in faces:
        # 在脸周围画一个矩形框，(255,0,0)是颜色，2是线宽
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 获取人脸图像
        face = gray[y:y + h, x:x + w]

        try:
            # shape变为(48,48)
            face = cv2.resize(face, (48, 48))
            print(face.shape)
        except:
            continue

        # 扩充维度，shape变为(1,48,48,1)
        face = np.expand_dims(face, 0)
        face = np.expand_dims(face, -1)
        # 人脸数据归一化，将像素值从0-255映射到0-1之间
        face = preprocess_input(face)

        # 调用我们训练好的表情识别模型，预测分类
        emotion_arg = np.argmax(emotion_classifier.predict(face))
        emotion = emotion_labels[emotion_arg]

        emotion_window.append(emotion)

        if len(emotion_window) >= frame_window:
            emotion_window.pop(0)

        try:
            # 获得出现次数最多的分类
            emotion_mode = mode(emotion_window)
        except:
            continue

        # 在矩形框上部，输出分类文字
        cv2.putText(gray, emotion_mode, (x, y - 30), font, .7, (255, 0, 0), 1, cv2.LINE_AA)

    try:
        # 将图片从内存中显示到屏幕上
        cv2.imshow('window_frame', gray)
    except:
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
