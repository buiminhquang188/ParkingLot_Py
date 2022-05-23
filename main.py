from turtle import pos
import cv2
import time
from utils.traker import *
from car_info.plate_detection import *
from server.post import *
# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("./assets/video/video_parking.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=50)
lastPlate = ""
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    x_box_1 = 0
    y_box_1 = 500
    w_box_1 = 500
    h_box_1 = 300

    x_box_2 = 700
    y_box_2 = 500
    w_box_2 = 500
    h_box_2 = 300
    # Object detection
    box_1 = frame[x_box_1:x_box_1+w_box_1, y_box_1:y_box_1+h_box_1]

    box_2 = frame[x_box_2: x_box_2+w_box_2, y_box_2: y_box_2+h_box_2]

    mask_box_1 = object_detector.apply(box_2)
    _, mask_box_1 = cv2.threshold(mask_box_1, 254, 255, cv2.THRESH_BINARY)
    contours_box_1, _ = cv2.findContours(
        mask_box_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.rectangle(frame, (x_box_1, y_box_1),
                  (x_box_1+w_box_1, y_box_1+h_box_1), (0, 255, 0), 3)
    cv2.rectangle(frame, (x_box_2, y_box_2),
                  (x_box_2+w_box_2, y_box_2+h_box_2), (0, 255, 0), 3)
    cv2.putText(frame, "Spot 1", (x_box_1+200, y_box_1 - 15),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(frame, "Spot 2", (x_box_2+200, y_box_2 - 15),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    detections = []
    for cnt in contours_box_1:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 4000:
            #cv2.drawcontours_box_1(box_1, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            resp, plate_info = plate_detection()
            detections.append([x, y, w, h])
            cv2.rectangle(box_2, (x_box_1, y_box_1),
                          (x_box_1+w_box_1, y_box_1+h_box_1), (0, 255, 0), 3)
            if resp == SUCCESS and plate_info != lastPlate:
                print(post(plate_info, "2"))
                lastPlate = plate_info

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(  1)
