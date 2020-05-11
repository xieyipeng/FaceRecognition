from statistics import mode
import cv2
from keras.models import load_model
import numpy as np
# from utils import preprocess_input
from test_mtcnn_wider import face_detect
from tools.fer2013.utils import preprocess_input

# parameters for loading data and images
detection_model_path = '/home/xieyipeng/下载/emotionrecognition-master/trained_models/facemodel/haarcascade_frontalface_default.xml'
emotion_model_path = '../model/fer2013/fer2013_mini_XCEPTION.33-0.65.hdf5'
emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                  4: 'sad', 5: 'surprise', 6: 'neutral'}

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]
emotion_window = []
frame_window = 10

# starting video streaming
cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(0)
while True:
    bgr_image = video_capture.read()[1]
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    # faces = face_detection.detectMultiScale(gray_image, 1.3, 5)

    rectangles, points = face_detect(frame=bgr_image)

    # print(len(rectangles))

    for face_coordinates in rectangles:
        # print(face_coordinates)
        cv2.putText(bgr_image, str(face_coordinates[4]),
                    (int(face_coordinates[0]), int(face_coordinates[1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), thickness=1)
        cv2.rectangle(bgr_image, (int(face_coordinates[0]), int(face_coordinates[1])),
                      (int(face_coordinates[2]), int(face_coordinates[3])),
                      (0, 0, 255), 2)

        x1, y1, width, height, flag = face_coordinates
        x1, y1, x2, y2 = x1, y1, x1 + width, y1 + height
        # x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[int(y1):int(y2), int(x1):int(x2)]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue
        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        # emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)
        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_text = mode(emotion_window)
        except:
            continue
        # color = (0, 0, 255)
        cv2.putText(bgr_image, emotion_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2,
                    cv2.LINE_AA)
        # cv2.putText(frame, emotion_mode,  (int(rectangle[0]), int(rectangle[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 2,
        #             (255, 0, 0), 1, cv2.LINE_AA)
    # bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.resizeWindow("window_frame", 1024, 768)
    cv2.imshow('window_frame', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
