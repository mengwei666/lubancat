import cv2

# 使用设备文件路径打开摄像头
cap = cv2.VideoCapture('/dev/video-camera0')  # 使用设备文件的路径

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 捕捉一帧视频
    ret, frame = cap.read()

    # 检查是否成功捕捉到帧
    if not ret:
        print("无法读取摄像头的帧")
        break

    # 显示当前帧
    cv2.imshow('Camera Feed', frame)

    # 如果按下 'q' 键则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有OpenCV窗口
cap.release()
cv2.destroyAllWindows()
