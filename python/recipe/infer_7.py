import fastdeploy as fd
import cv2
import os


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--det_model", 
        default='ch_PP-OCRv3_det_infer_rk3568_unquantized.rknn',
        help="Path of Detection model of PPOCR.")
    parser.add_argument(
        "--cls_model",
        default='ch_ppocr_mobile_v20_cls_infer_rk3568_unquantized.rknn',
        help="Path of Classification model of PPOCR.")
    parser.add_argument(
        "--rec_model",
        default='ch_PP-OCRv3_rec_infer_rk3568_unquantized.rknn',
        help="Path of Recognization model of PPOCR.")
    parser.add_argument(
        "--rec_label_file",
        default='ppocr_keys_v1.txt',
        help="Path of Recognization model of PPOCR.")
    parser.add_argument(
        "--device",
        type=str,
        default='npu',
        help="Type of inference device, support 'cpu', 'kunlunxin' or 'gpu'.")
    parser.add_argument(
        "--cpu_thread_num",
        type=int,
        default=9,
        help="Number of threads while inference on CPU.")
    return parser.parse_args()


def build_option(args):

    det_option = fd.RuntimeOption()
    cls_option = fd.RuntimeOption()
    rec_option = fd.RuntimeOption()
    if args.device == "npu":
        det_option.use_rknpu2()
        cls_option.use_rknpu2()
        rec_option.use_rknpu2()

    return det_option, cls_option, rec_option


def build_format(args):
    det_format = fd.ModelFormat.ONNX
    cls_format = fd.ModelFormat.ONNX
    rec_format = fd.ModelFormat.ONNX
    if args.device == "npu":
        det_format = fd.ModelFormat.RKNN
        cls_format = fd.ModelFormat.RKNN
        rec_format = fd.ModelFormat.RKNN

    return det_format, cls_format, rec_format


args = parse_arguments()

# Detection模型, 检测文字框
det_model_file = args.det_model
det_params_file = ""
# Classification模型，方向分类，可选
cls_model_file = args.cls_model
cls_params_file = ""
# Recognition模型，文字识别模型
rec_model_file = args.rec_model
rec_params_file = ""
rec_label_file = args.rec_label_file

det_option, cls_option, rec_option = build_option(args)
det_format, cls_format, rec_format = build_format(args)

det_model = fd.vision.ocr.DBDetector(
    det_model_file,
    det_params_file,
    runtime_option=det_option,
    model_format=det_format)

cls_model = fd.vision.ocr.Classifier(
    cls_model_file,
    cls_params_file,
    runtime_option=cls_option,
    model_format=cls_format)

rec_model = fd.vision.ocr.Recognizer(
    rec_model_file,
    rec_params_file,
    rec_label_file,
    runtime_option=rec_option,
    model_format=rec_format)

# Det,Rec模型启用静态shape推理
det_model.preprocessor.static_shape_infer = True
rec_model.preprocessor.static_shape_infer = True

if args.device == "npu":
    det_model.preprocessor.disable_normalize()
    det_model.preprocessor.disable_permute()
    cls_model.preprocessor.disable_normalize()
    cls_model.preprocessor.disable_permute()
    rec_model.preprocessor.disable_normalize()
    rec_model.preprocessor.disable_permute()

# 创建PP-OCR，串联3个模型，其中cls_model可选，如无需求，可设置为None
ppocr_v3 = fd.vision.ocr.PPOCRv3(
    det_model=det_model, cls_model=cls_model, rec_model=rec_model)

# Cls模型和Rec模型的batch size 必须设置为1, 开启静态shape推理
ppocr_v3.cls_batch_size = 1
ppocr_v3.rec_batch_size = 1

# 打开摄像头
cap = cv2.VideoCapture('/dev/video9')

# 获取当前分辨率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Current resolution: {width}x{height}")

# 设置分辨率，例如640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
