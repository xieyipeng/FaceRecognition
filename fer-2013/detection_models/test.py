import cv2

cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象

cap.set(3, 960)
cap.set(4, 960)

flag = 1

while (cap.isOpened()):
    ret, frame = cap.read()

    # TODO: 人脸检测
    # <class 'numpy.ndarray'>
    # print(frame.shape)
    # print(type(frame))

    # TODO: 表情识别

    cv2.imshow("Capture_Test", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
