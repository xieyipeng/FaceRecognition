import time

import tensorflow.compat.v1 as tf
import cv2
import numpy as np

from tools.mtcnn.mtcnn import PNet, RNet, ONet
from tools.mtcnn.tools import detect_face, get_model_filenames


def face_detect(factor=0.7, frame=None, image_path='images/test1.jpg', save_image=False, save_name='images/result.jpg',
                model_dir='/home/xieyipeng/code/Graduation-Design/combine/model/mtcnn', threshold=None):
    if threshold is None:
        threshold = [0.8, 0.8, 0.8]
    if frame is None:
        img = cv2.imread(image_path)
    else:
        img = frame
    file_paths = get_model_filenames(model_dir)
    with tf.device('/gpu:0'):
        with tf.Graph().as_default():
            config = tf.ConfigProto(allow_soft_placement=True)
            with tf.Session(config=config) as sess:
                if len(file_paths) == 3:

                    print("1")
                    image_pnet = tf.placeholder(
                        tf.float32, [None, None, None, 3])
                    pnet = PNet({'data': image_pnet}, mode='test')
                    out_tensor_pnet = pnet.get_all_output()

                    image_rnet = tf.placeholder(tf.float32, [None, 24, 24, 3])
                    rnet = RNet({'data': image_rnet}, mode='test')
                    out_tensor_rnet = rnet.get_all_output()

                    image_onet = tf.placeholder(tf.float32, [None, 48, 48, 3])
                    onet = ONet({'data': image_onet}, mode='test')
                    out_tensor_onet = onet.get_all_output()

                    saver_pnet = tf.train.Saver(
                        [v for v in tf.global_variables()
                         if v.name[0:5] == "pnet/"])
                    saver_rnet = tf.train.Saver(
                        [v for v in tf.global_variables()
                         if v.name[0:5] == "rnet/"])
                    saver_onet = tf.train.Saver(
                        [v for v in tf.global_variables()
                         if v.name[0:5] == "onet/"])

                    saver_pnet.restore(sess, file_paths[0])

                    def pnet_fun(img):
                        return sess.run(out_tensor_pnet, feed_dict={image_pnet: img})

                    saver_rnet.restore(sess, file_paths[1])

                    def rnet_fun(img):
                        return sess.run(out_tensor_rnet, feed_dict={image_rnet: img})

                    saver_onet.restore(sess, file_paths[2])

                    def onet_fun(img):
                        return sess.run(out_tensor_onet, feed_dict={image_onet: img})

                else:
                    print("2")
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

                start_time = time.time()

                # point .
                # rectangles 矩形
                return detect_face(img, 20, pnet_fun, rnet_fun, onet_fun, threshold, factor)

                # duration = time.time() - start_time
                # time
                # print(duration)
                # print(type(rectangles))
                # points = np.transpose(points)

                # TODO: 画矩形
                # for rectangle in rectangles:
                #     cv2.putText(img, str(rectangle[4]),
                #                 (int(rectangle[0]), int(rectangle[1])),
                #                 cv2.FONT_HERSHEY_SIMPLEX,
                #                 0.5, (0, 255, 0))
                #     cv2.rectangle(img, (int(rectangle[0]), int(rectangle[1])),
                #                   (int(rectangle[2]), int(rectangle[3])),
                #                   (255, 0, 0), 1)

                # TODO: 5个特征点
                # for point in points:
                #     for i in range(0, 10, 2):
                #         cv2.circle(img, (int(point[i]), int(point[i + 1])), 2, (0, 255, 0))

                # cv2.imshow("test", img)
                # if save_image:
                #     cv2.imwrite(save_name, img)
                # if cv2.waitKey(0) & 0xFF == ord('q'):
                #     cv2.destroyAllWindows()


if __name__ == '__main__':
    face_detect()
