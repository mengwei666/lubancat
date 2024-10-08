import fastdeploy as fd
import cv2


def default_recipe():
    # 模型路径
    det_model_path = './ppocrv4_det_rk3568.rknn'
    rec_model_path = './ppocrv4_rec_rk3568.rknn'
    rec_label_file = './ppocr_keys_v1.txt'
    image_path = './12.jpg'  # 替换为你的图像路径

    # 加载模型
    print("Loading detection model...")
    det_model = fd.vision.ocr.DBDetector(model_file=det_model_path)

    print("Loading recognition model...")
    rec_model = fd.vision.ocr.Recognizer(model_file=rec_model_path, label_file=rec_label_file)

    # 读取图像
    image = cv2.imread(image_path)

    # 进行文字检测
    print("Running detection...")
    det_result = det_model.predict(image)

    # 进行文字识别
    print("Running recognition...")
    rec_result = rec_model.predict(image, det_result)

    # 打印识别结果
    print("Recognition Results:")
    for text in rec_result:
        print(text)

    # 可视化结果
    vis_image = fd.vision.vis_ppocr(image, rec_result)
    cv2.imwrite("visualized_result.jpg", vis_image)
    print("可视化结果已保存为 visualized_result.jpg")


if __name__ == "__main__":
    default_recipe()
