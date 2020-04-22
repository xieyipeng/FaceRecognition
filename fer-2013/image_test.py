import cv2
import tensorflow.compat.v1 as tf
from keras.models import load_model
import numpy as np
from utils import preprocess_input, load_image, get_coordinates, detect_faces, draw_bounding_box, draw_text

# init = tf.global_variables_initializer()
#
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config)
#
# session.run(init)

# parameters for loading data and images
image_path = 'images/1.jpg'
detection_model_path = 'detection_models/haarcascade_frontalface_default.xml'
# emotion_model_path = 'trained_models/emotion_models/simple_CNN.985-0.66.hdf5'
emotion_model_path = 'trained_models/simpler_CNN.100-0.64.hdf5'
# gender_model_path = 'trained_models/gender_models/simple_CNN.81-0.96.hdf5'

emotion_labels = {0: 'angry', 1: 'disgust', 2: 'sad', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

# 加载人脸识别模型
face_detection = cv2.CascadeClassifier(detection_model_path)
# 加载表情识别模型
emotion_classifier = load_model(emotion_model_path, compile=False)

# 获得模型输入图形宽高尺寸大小
emotion_target_size = emotion_classifier.input_shape[1:3]

# 加载原始图像
rgb_image = load_image(image_path, grayscale=False)
# 加载灰度图像
gray_image = load_image(image_path, grayscale=True)

# 去掉维度为1的维度（只留下宽高，去掉灰度维度）
gray_image = np.squeeze(gray_image)
gray_image = gray_image.astype('uint8')

# 检测出图像中的全部人脸
faces = detect_faces(face_detection, gray_image)

# 对于图像中的每一个人脸
for face_coordinates in faces:
    # 获取人脸在图像中的矩形区域坐标
    x1, x2, y1, y2 = get_coordinates(face_coordinates)
    # 截取人脸图像像素数组
    gray_face = gray_image[y1:y2, x1:x2]

    try:
        # 将人脸reshape成模型需要的尺寸
        gray_face = cv2.resize(gray_face, (emotion_target_size))
    except:
        continue

    # 将人脸数据归一化（像素值归一化到0-1之间）
    gray_face = preprocess_input(gray_face)
    # 扩充第一个维度
    gray_face = np.expand_dims(gray_face, 0)
    # 扩充最后一个维度
    # shape(1,48,48,1)---shape(图片数量，高，宽，通道数），输入1张1通道48 * 48的图像数据
    gray_face = np.expand_dims(gray_face, -1)

    # 通过我们训练的模型预测表情
    emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
    emotion_text = emotion_labels[emotion_label_arg]
    print(emotion_text)

    color = (255, 0, 0)
    # 画边框
    draw_bounding_box(face_coordinates, rgb_image, color)
    # 画表情说明
    draw_text(face_coordinates, rgb_image, emotion_text, color, 0, face_coordinates[3] + 30, 1, 2)

# 将图像转换为BGR模式显示
bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
cv2.imwrite('images/predicted_image.png', bgr_image)

# cv2.imshow("img_covert", bgr_image)
# cv2.waitKey()
