from test_mtcnn_wider import face_detect
from keras.models import load_model
import cv2
from statistics import mode
import numpy as np
from tools.fer2013.utils import preprocess_input

emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}
emotion_model_path = '../model/fer2013/fer2013_mini_XCEPTION.33-0.65.hdf5'

cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]
emotion_window = []
frame_window = 10

cv2.namedWindow('test',0)


def rescale_frame(frame, percent=75):
    scale_percent = percent
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


while True:
    frame = cap.read()[1]
    frame = rescale_frame(frame)

    # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # TODO: 人脸检测
    rectangles, points = face_detect(frame=frame)
    # print(rectangles)
    for rectangle in rectangles:
        cv2.putText(frame, str(rectangle[4]),
                    (int(rectangle[0]), int(rectangle[1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0))
        cv2.rectangle(frame, (int(rectangle[0]), int(rectangle[1])),
                      (int(rectangle[2]), int(rectangle[3])),
                      (255, 0, 0), 1)
        # TODO: 表情识别
        face = frame[int(rectangle[0]):int(rectangle[2]), int(rectangle[1]):int(rectangle[3])]
        try:
            face = cv2.resize(face, (emotion_target_size))
            # print(face.shape)
        except:
            continue

        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # 再将后者由三通道转换为单通道

        # gray_face = preprocess_input(face, True)
        # gray_face = np.expand_dims(gray_face, 0)
        # gray_face = np.expand_dims(gray_face, -1)
        # emotion_prediction = emotion_classifier.predict(gray_face)
        # emotion_label_arg = np.argmax(emotion_prediction)
        # emotion_text = emotion_labels[emotion_label_arg]
        # emotion_window.append(emotion_text)
        # if len(emotion_window) > frame_window:
        #     emotion_window.pop(0)
        # try:
        #     emotion_text = mode(emotion_window)
        # except:
        #     continue
        # color = (0, 0, 255)
        #
        #
        # cv2.putText(frame, emotion_text, (int(rectangle[0]), int(rectangle[1]) - 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        # frame = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        # cv2.resizeWindow("test", 1024, 768)
        # cv2.imshow('test', rgb_image)
        # print('==============')
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break



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
        cv2.putText(frame, emotion_mode,  (int(rectangle[0]), int(rectangle[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    (255, 0, 0), 1, cv2.LINE_AA)

    # cv2.namedWindow("test", 0)
    cv2.resizeWindow("test", 1024, 768)
    cv2.imshow("test", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()
