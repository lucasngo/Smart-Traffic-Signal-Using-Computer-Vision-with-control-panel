import cv2
# import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import numpy as np
import json 

# from tracker import add_new_blobs, remove_duplicates, update_blob_tracker
# from detectors.detector import get_bounding_boxes




def get_roi_frame(current_frame, polygon):
    mask = np.zeros(current_frame.shape, dtype=np.uint8)
    polygon = np.array([polygon], dtype=np.int32)
    num_frame_channels = current_frame.shape[2]
    mask_ignore_color = (255,) * num_frame_channels
    cv2.fillPoly(mask, polygon, mask_ignore_color)
    masked_frame = cv2.bitwise_and(current_frame, mask)
    return masked_frame

def draw_roi(frame, polygon,polygon1):
    frame_overlay = frame.copy()
    polygon = np.array([polygon], dtype=np.int32)
    polygon1 = np.array([polygon1], dtype=np.int32)
    cv2.fillPoly(frame_overlay, polygon, (0, 255, 255))
    cv2.fillPoly(frame_overlay, polygon1, (205, 202, 106))
    alpha = 0.3
    output_frame = cv2.addWeighted(frame_overlay, alpha, frame, 1 - alpha, 0)
    return output_frame

cap=cv2.VideoCapture('main.mp4')
droi=[(500, 50), (670, 50), (730, 1028), (0, 1028)]
droi1=[(680,50),(950,50),(1300,1028),(750,1028)]
# f_height, f_width, _ = cap.shape

count = 0

while cap.isOpened():
    ret, frame = cap.read()
    droi_frame = get_roi_frame(frame,droi)
    droi_frame1=get_roi_frame(frame,droi1)
    if ret:
        frame = draw_roi(frame, droi,droi1)
        bbox, label, conf = cv.detect_common_objects(droi_frame)
        bbox1, label1, conf1 = cv.detect_common_objects(droi_frame1)
        output_image = draw_bbox(frame, bbox+bbox1, label+label1, conf+conf1)
        
        result={
            "lane 1":{
                "car": label.count('car'),
                "truck/bus": label.count('bus')+label.count('truck')
            },
            "lane 2":{
                "car":label1.count("car")+label1.count('train')+label1.count('boat'),
                "truck/bus":label1.count("truck")+label1.count("bus")
            }
        }
        json_result=json.dumps(result)
        print(json_result)
        cv2.imshow('Video', frame)
        count += 30 # i.e. at 30 fps, this advances one second
        cap.set(1, count)
    else:
        cap.release()
        break
    if cv2.waitKey(20) & 0xFF==ord('d'):  #stop the video
        break
    
cap.release()
cv2.destroyAllWindows()
# _bounding_boxes, _classes, _confidences = get_bounding_boxes(droi_frame, detector)
# blobs = add_new_blobs(_bounding_boxes, _classes, _confidences, blobs, frame, tracker, mcdf)


# cv2.imshow('pic',droi_frame)
# cv2.waitKey(0)

