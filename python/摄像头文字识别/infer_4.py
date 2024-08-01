import fastdeploy as fd
import cv2
import os

# 硬编码模型文件路径和设备类型
det_model_file = "./ch_PP-OCRv3_det_infer.onnx"
cls_model_file = "./ch_ppocr_mobile_v2.0_cls_infer.onnx"
rec_model_file = "./ch_PP-OCRv3_rec_infer.onnx"
rec_label_file = "./ppocr_keys_v1.txt"
device_type = "cpu"
cpu_thread_num = 9

# 构建选项
det_option = fd.RuntimeOption()
cls_option = fd.RuntimeOption()
rec_option = fd.RuntimeOption()

# 设置CPU推理选项
det_option.use_cpu()
cls_option.use_cpu()
rec_option.use_cpu()
det_option.set_cpu_thread_num(cpu_thread_num)
cls_option.set_cpu_thread_num(cpu_thread_num)
rec_option.set_cpu_thread_num(cpu_thread_num)

# 构建模型格式
det_format = fd.ModelFormat.ONNX
cls_format = fd.ModelFormat.ONNX
rec_format = fd.ModelFormat.ONNX

# 创建检测模型
det_model = fd.vision.ocr.DBDetector(
    det_model_file,
    "",
    runtime_option=det_option,
    model_format=det_format)

# 创建分类模型
cls_model = fd.vision.ocr.Classifier(
    cls_model_file,
    "",
    runtime_option=cls_option,
    model_format=cls_format)

# 创建识别模型
rec_model = fd.vision.ocr.Recognizer(
    rec_model_file,
    "",
    rec_label_file,
    runtime_option=rec_option,
    model_format=rec_format)

# 启用静态shape推理
det_model.preprocessor.static_shape_infer = True
rec_model.preprocessor.static_shape_infer = True

# 创建PP-OCR，串联3个模型，其中cls_model可选，如无需求，可设置为None
ppocr_v3 = fd.vision.ocr.PPOCRv3(
    det_model=det_model, cls_model=cls_model, rec_model=rec_model)

# Cls模型和Rec模型的batch size 必须设置为1, 开启静态shape推理
ppocr_v3.cls_batch_size = 1
ppocr_v3.rec_batch_size = 1

# 打开摄像头
cap = cv2.VideoCapture('/dev/video9')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 预测并打印结果
    result = ppocr_v3.predict(frame)
    print(result)

    # 可视化结果
    vis_frame = fd.vision.vis_ppocr(frame, result)
    cv2.imshow("PPOCR Result", vis_frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
