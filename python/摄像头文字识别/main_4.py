import fastdeploy as fd
import cv2

def main(det_model_path, rec_model_path, rec_label_file, image_path):
    # 加载检测模型
    det_model = fd.vision.ocr.DBDetector(model_file=det_model_path)
    
    # 加载识别模型
    rec_model = fd.vision.ocr.Recognizer(model_file=rec_model_path, label_file=rec_label_file)

    # 读取图像
    image = cv2.imread(image_path)

    # 进行文字检测
    det_result = det_model.predict(image)

    # 进行文字识别
    rec_result = rec_model.predict(image, det_result)

    # 打印识别结果
    print("Recognition Results:")
    for text in rec_result:
        print(text)

    # 可视化结果
    vis_image = fd.vision.vis_ppocr(image, rec_result)
    cv2.imwrite("visualized_result.jpg", vis_image)
    print("Visualized result saved as 'visualized_result.jpg'.")

if __name__ == "__main__":
    # 替换为你的模型路径和图像路径
    det_model_path = 'ppocrv4_det_rk3568.rknn'
    rec_model_path = 'ppocrv4_rec_rk3568.rknn'
    rec_label_file = 'ppocr_keys_v1.txt'
    image_path = '12.jpg'
    
    main(det_model_path, rec_model_path, rec_label_file, image_path)
