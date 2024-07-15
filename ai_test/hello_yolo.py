from ultralytics import YOLO

modle = YOLO('yolov8s.pt')


results = modle(source="D:\\screenshot\\zJP.jpg", show=False, conf=0.4, save=True)




