import cv2


def CatchCamera(window_name, camera_idx):
    cv2.namedWindow(window_name)  # 该方法是写入打开时视频框的名称
    # 捕捉摄像头
    # VideoCapture()中参数是0，表示打开笔记本的内置摄像头。
    cap = cv2.VideoCapture(camera_idx)
    while cap.isOpened():  # 判断摄像头是否打开，打开的话就是返回的是True
        ok, frame = cap.read()  # 读取一帧数据，该方法返回两个参数，第一个参数是布尔值，frame就是每一帧的图像，是个三维矩阵，当输入的是一个是视频文件，读完ok==flase
        if not ok:  # 如果读取帧数不是正确的则ok就是Flase则该语句就会执行
            break
        # 图片输出
        cv2.imwrite("out.jpg", frame)
        # 显示图像
        cv2.imshow(window_name, frame)  # 该方法就是现实该图像
        # 参数是1，表示延时1ms切换到下一帧图像，参数过大如cv2.waitKey(1000)，会因为延时过久而卡顿感觉到卡顿。
        # 参数为0，如cv2.waitKey(0)只显示当前帧图像，相当于视频暂停。
        c = cv2.waitKey(1)
        if c == 27:  # esc退出视频
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchCamera("FaceRect", 0)
