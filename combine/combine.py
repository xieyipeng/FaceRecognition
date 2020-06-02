import cv2
import tensorflow.compat.v1 as tf
from tools.mtcnn.tools import get_model_filenames
import numpy as np
import threading, queue
import tools.mtcnn.tools as tools
from test_vgg_ck import rgb2gray
from skimage.transform import resize
from PIL import Image
import os
from tools.vgg.models import *
from test_vgg_ck import transform_test

cap = cv2.VideoCapture('/home/xieyipeng/视频/demo-2020-05-10_21.33.44.mkv')
# cap = cv2.VideoCapture(0)
cv2.namedWindow('test', 0)

detect_queue = queue.Queue(maxsize=128 * 128 * 36)
detect_result_queue = queue.Queue(maxsize=1000 * 36)

emotion_queue = queue.Queue(maxsize=128 * 128 * 36)
emotion_result_queue = queue.Queue(maxsize=1000 * 36)


def face_detect(factor=0.7, model_dir='model/mtcnn', threshold=None):
    if threshold is None:
        threshold = [0.8, 0.8, 0.8]
    file_paths = get_model_filenames(model_dir)
    with tf.device('/gpu:0'):
        with tf.Graph().as_default():
            config = tf.ConfigProto(allow_soft_placement=True)
            with tf.Session(config=config) as sess:
                saver = tf.train.import_meta_graph(file_paths[0])
                saver.restore(sess, file_paths[1])

                def pnet_fun(img):
                    return sess.run(
                        ('softmax/Reshape_1:0',
                         'pnet/conv4-2/BiasAdd:0'),
                        feed_dict={
                            'Placeholder:0': img})

                def rnet_fun(img):
                    return sess.run(
                        ('softmax_1/softmax:0',
                         'rnet/conv5-2/rnet/conv5-2:0'),
                        feed_dict={
                            'Placeholder_1:0': img})

                def onet_fun(img):
                    return sess.run(
                        ('softmax_2/softmax:0',
                         'onet/conv6-2/onet/conv6-2:0',
                         'onet/conv6-3/onet/conv6-3:0'),
                        feed_dict={
                            'Placeholder_2:0': img})

                while 1:
                    minsize = 20
                    img = detect_queue.get()
                    factor_count = 0
                    total_boxes = np.empty((0, 9))
                    points = []
                    h = img.shape[0]
                    w = img.shape[1]
                    minl = np.amin([h, w])
                    m = 12.0 / minsize
                    minl = minl * m
                    # creat scale pyramid
                    scales = []
                    while minl >= 12:
                        scales += [m * np.power(factor, factor_count)]
                        minl = minl * factor
                        factor_count += 1

                    # first stage
                    for j in range(len(scales)):
                        scale = scales[j]
                        hs = int(np.ceil(h * scale))
                        ws = int(np.ceil(w * scale))
                        im_data = tools.imresample(img, (hs, ws))
                        im_data = (im_data - 127.5) * (1. / 128.0)
                        img_x = np.expand_dims(im_data, 0)
                        out = pnet_fun(img_x)
                        out0 = out[0]
                        out1 = out[1]
                        boxes, _ = tools.generateBoundingBox(out0[0, :, :, 1].copy(),
                                                             out1[0, :, :, :].copy(), scale, threshold[0])

                        # inter-scale nms
                        pick = tools.nms(boxes.copy(), 0.5, 'Union')
                        if boxes.size > 0 and pick.size > 0:
                            boxes = boxes[pick, :]
                            total_boxes = np.append(total_boxes, boxes, axis=0)

                    numbox = total_boxes.shape[0]
                    if numbox > 0:
                        pick = tools.nms(total_boxes.copy(), 0.7, 'Union')
                        total_boxes = total_boxes[pick, :]
                        regw = total_boxes[:, 2] - total_boxes[:, 0]
                        regh = total_boxes[:, 3] - total_boxes[:, 1]
                        qq1 = total_boxes[:, 0] + total_boxes[:, 5] * regw
                        qq2 = total_boxes[:, 1] + total_boxes[:, 6] * regh
                        qq3 = total_boxes[:, 2] + total_boxes[:, 7] * regw
                        qq4 = total_boxes[:, 3] + total_boxes[:, 8] * regh
                        total_boxes = np.transpose(np.vstack([qq1, qq2, qq3, qq4, total_boxes[:, 4]]))
                        total_boxes = tools.rerec(total_boxes.copy())
                        total_boxes[:, 0:4] = np.fix(total_boxes[:, 0:4]).astype(np.int32)
                        dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = tools.pad(total_boxes.copy(), w, h)

                    numbox = total_boxes.shape[0]
                    if numbox > 0:
                        # second stage
                        tempimg = np.zeros((24, 24, 3, numbox))
                        for k in range(0, numbox):
                            tmp = np.zeros((int(tmph[k]), int(tmpw[k]), 3))
                            tmp[dy[k] - 1:edy[k], dx[k] - 1:edx[k],
                            :] = img[y[k] - 1:ey[k], x[k] - 1:ex[k], :]
                            if tmp.shape[0] > 0 and tmp.shape[1] > 0 or tmp.shape[0] == 0 and tmp.shape[1] == 0:
                                tempimg[:, :, :, k] = tools.imresample(tmp, (24, 24))
                            else:
                                return np.empty()
                        tempimg = (tempimg - 127.5) * 0.0078125
                        tempimg1 = np.transpose(tempimg, (3, 0, 1, 2))
                        out = rnet_fun(tempimg1)
                        out0 = np.transpose(out[0])
                        out1 = np.transpose(out[1])
                        score = out0[1, :]
                        ipass = np.where(score > threshold[1])
                        total_boxes = np.hstack(
                            [total_boxes[ipass[0], 0:4].copy(), np.expand_dims(score[ipass].copy(), 1)])
                        mv = out1[:, ipass[0]]
                        if total_boxes.shape[0] > 0:
                            pick = tools.nms(total_boxes, 0.7, 'Union')
                            total_boxes = total_boxes[pick, :]
                            total_boxes = tools.bbreg(total_boxes.copy(), np.transpose(mv[:, pick]))
                            total_boxes = tools.rerec(total_boxes.copy())

                    numbox = total_boxes.shape[0]
                    if numbox > 0:
                        # third stage
                        total_boxes = np.fix(total_boxes).astype(np.int32)
                        dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = tools.pad(total_boxes.copy(), w, h)
                        tempimg = np.zeros((48, 48, 3, numbox))
                        for k in range(0, numbox):
                            tmp = np.zeros((int(tmph[k]), int(tmpw[k]), 3))
                            tmp[dy[k] - 1:edy[k], dx[k] - 1:edx[k], :] = img[y[k] - 1:ey[k], x[k] - 1:ex[k], :]
                            if (tmp.shape[0] > 0 and tmp.shape[1] > 0 or
                                    tmp.shape[0] == 0 and tmp.shape[1] == 0):
                                tempimg[:, :, :, k] = tools.imresample(tmp, (48, 48))
                            else:
                                return np.empty()
                        tempimg = (tempimg - 127.5) * 0.0078125
                        tempimg1 = np.transpose(tempimg, (3, 0, 1, 2))
                        out = onet_fun(tempimg1)
                        out0 = np.transpose(out[0])
                        out1 = np.transpose(out[1])
                        out2 = np.transpose(out[2])
                        score = out0[1, :]
                        points = out2
                        ipass = np.where(score > threshold[2])
                        points = points[:, ipass[0]]
                        total_boxes = np.hstack(
                            [total_boxes[ipass[0], 0:4].copy(), np.expand_dims(score[ipass].copy(), 1)])
                        mv = out1[:, ipass[0]]
                        w = total_boxes[:, 2] - total_boxes[:, 0] + 1
                        h = total_boxes[:, 3] - total_boxes[:, 1] + 1
                        points[0:10:2, :] = np.tile(w, (5, 1)) * (points[0:10:2, :] + 1) / 2 + np.tile(
                            total_boxes[:, 0], (5, 1)) - 1
                        points[1:11:2, :] = np.tile(h, (5, 1)) * (points[1:11:2, :] + 1) / 2 + np.tile(
                            total_boxes[:, 1], (5, 1)) - 1
                        if total_boxes.shape[0] > 0:
                            total_boxes = tools.bbreg(total_boxes.copy(), np.transpose(mv))
                            pick = tools.nms(total_boxes.copy(), 0.7, 'Min')
                            total_boxes = total_boxes[pick, :]
                            points = points[:, pick]

                    detect_result_queue.put((total_boxes, points))


def emotion_rec():
    class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    net = VGG('VGG19')
    checkpoint = torch.load(os.path.join('model/CK+_VGG19/10/Test_model.t7'))
    net.load_state_dict(checkpoint['net'])
    net.cuda()
    net.eval()

    while 1:
        raw_img = emotion_queue.get()
        gray = rgb2gray(raw_img)
        gray = resize(gray, (48, 48), mode='symmetric').astype(np.uint8)
        img = gray[:, :, np.newaxis]
        img = np.concatenate((img, img, img), axis=2)
        img = Image.fromarray(img)
        inputs = transform_test(img)

        n_crops, c, h, w = np.shape(inputs)

        inputs = inputs.view(-1, c, h, w)
        inputs = inputs.cuda()
        inputs = Variable(inputs, volatile=True)
        outputs = net(inputs)

        outputs_avg = outputs.view(n_crops, -1).mean(0)  # avg over crops

        score = F.softmax(outputs_avg)
        _, predicted = torch.max(outputs_avg.data, 0)

        emotion_result_queue.put((class_names[predicted.item()], score[predicted.item()].item()))
        # return class_names[predicted.item()], score


detect_thread = threading.Thread(target=face_detect)
detect_thread.start()

emotion_thread = threading.Thread(target=emotion_rec)
emotion_thread.start()

while True:
    ret, frame = cap.read()
    if ret:
        # TODO: 人脸检测
        detect_queue.put(frame)
        rectangles, points = detect_result_queue.get()
        for rectangle in rectangles:
            x1, y1, width, height, face_score = rectangle
            x1, y1, x2, y2 = x1, y1, x1 + width, y1 + height

            cv2.putText(frame, str(rectangle[4]), (int(rectangle[0]), int(rectangle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0))
            cv2.rectangle(frame, (int(rectangle[0]), int(rectangle[1])), (int(rectangle[2]), int(rectangle[3])),
                          (255, 0, 0), 1)

            # TODO: 表情识别
            emotion_queue.put(frame[int(y1):int(y2), int(x1):int(x2)])
            category, emotion_score = emotion_result_queue.get()
            print(category, emotion_score)
            cv2.putText(frame, category, (int(x1), int(y1) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                        cv2.LINE_AA)

    cv2.resizeWindow("test", 1024, 768)
    cv2.imshow("test", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
