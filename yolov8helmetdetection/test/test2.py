from ultralytics import YOLO
import cv2
import numpy as np
from paddleocr import PaddleOCR

# 1. Load YOLOv8 model
model = YOLO(r'C:\Users\rguja\OneDrive\Desktop\Helmet detection\yolov8helmetdetection\test\best.pt')  # Path to your .pt file

# 2. Load PaddleOCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# 3. Load Video
video_path = (r'C:\Users\rguja\OneDrive\Desktop\Helmet detection\yolov8helmetdetection\test\h2.mp4') # Replace with your video path
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

# 4. Video Processing Loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    # 5. Perform Inference with YOLO
    results = model.predict(frame, verbose=False)

    # 6. Process Results and Display (Example)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Confidence score
            confidence = box.conf[0]
            confidence = float(confidence)

            # Class ID
            class_id = int(box.cls[0])

            # Draw bounding box and label
            label = f'{model.names[class_id]} {confidence:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # 7. Check for Helmet violation
            if model.names[class_id] == 'no-helmet': # Replace no-helmet by whatever code is specified
                # 8. Extract Number Plate (Assumes number plate is near the bike)
                # You may want to refine this ROI extraction based on your model's behavior
                plate_roi = frame[y1:y2, x1:x2]
                if plate_roi.shape[0] > 0 and plate_roi.shape[1] > 0:
                    # 9. Perform OCR on Number Plate
                    ocr_result = ocr.ocr(plate_roi, cls=True)
                    if len(ocr_result) > 0:
                        plate_text = ocr_result[0][0][1][0]
                        cv2.putText(frame, f'Plate: {plate_text}', (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


    # Display the resulting frame
    cv2.imshow('YOLOv8 Detection', frame)

    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10. Release Video and Destroy Windows
cap.release()
cv2.destroyAllWindows()