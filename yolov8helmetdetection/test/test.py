import cv2
import torch

# 1. Load the Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=(r'C:\Users\rguja\OneDrive\Desktop\Helmet detection\yolov8helmetdetection\test\best.pt'), force_reload=True)  # Load custom model with force_reload

# 2. Load Video
video_path = (r'C:\Users\rguja\OneDrive\Desktop\Helmet detection\yolov8helmetdetection\test\h2.mp4')  # Replace with your video path
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

# 3. Video Processing Loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    # 4. Perform Inference
    results = model(frame)

    # 5. Process Results and Display (Example)
    for *xyxy, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, xyxy)
        label = f'{model.names[int(cls)]} {conf:.2f}'
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('YOLOv5 Detection', frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 6. Release Video and Destroy Windows
cap.release()
cv2.destroyAllWindows()