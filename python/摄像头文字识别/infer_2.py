import fastdeploy as fd
import cv2

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--det_model", required=True, help="Path of Detection model of PPOCR.")
    parser.add_argument(
        "--cls_model",
        required=True,
        help="Path of Classification model of PPOCR.")
    parser.add_argument(
        "--rec_model",
        required=True,
        help="Path of Recognization model of PPOCR.")
    parser.add_argument(
        "--rec_label_file",
        required=True,
        help="Path of Recognization label file.")
    parser.add_argument(
        "--device",
        type=str,
        default='cpu',
        help="Type of inference device, support 'cpu', 'kunlunxin' or 'gpu'.")
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

# Initialize models
det_option, cls_option, rec_option = build_option(args)
det_format, cls_format, rec_format = build_format(args)

det_model = fd.vision.ocr.DBDetector(
    args.det_model,
    runtime_option=det_option,
    model_format=det_format)

cls_model = fd.vision.ocr.Classifier(
    args.cls_model,
    runtime_option=cls_option,
    model_format=cls_format)

rec_model = fd.vision.ocr.Recognizer(
    args.rec_model,
    args.rec_label_file,
    runtime_option=rec_option,
    model_format=rec_format)

# Enable static shape inference
det_model.preprocessor.static_shape_infer = True
rec_model.preprocessor.static_shape_infer = True

# Create PPOCR model
ppocr_v3 = fd.vision.ocr.PPOCRv3(
    det_model=det_model, cls_model=cls_model, rec_model=rec_model)

# Open the USB camera
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform OCR prediction
    result = ppocr_v3.predict(frame)

    # Visualize results
    vis_im = fd.vision.vis_ppocr(frame, result)
    cv2.imshow("PPOCR", vis_im)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
