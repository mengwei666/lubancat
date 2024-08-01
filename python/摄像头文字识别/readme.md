./rknn_ppocr_system_demo ./model/ppocrv4_det_rk3568.rknn ./model/ppocrv4_rec_rk3568.rknn ./model/2.jpg


查看摄像头列出所有连接的摄像头设备

> v4l2-ctl --list-devices

查看 `/dev/video9` 设备支持的格式和帧率

> v4l2-ctl --device=/dev/video9 --list-formats-ext
