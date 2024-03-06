from retinaface import RetinaFace
from retinaface.commons import postprocess
# from ultralytics import YOLO
import numpy as np
import datetime
# import detect
import cv2
import sys
import re
import os













def pad_to_square(input_image_path,output_image_path):
    # Step 1: Read the rectangle image
    # Step 2: Determine the size of the square image
    rectangle_image = cv2.imread(input_image_path)
    max_dim = max(rectangle_image.shape[0], rectangle_image.shape[1])
    square_size = (max_dim, max_dim)

    # Step 3: Create a new square image with a white background
    square_image = np.ones((square_size[0], square_size[1], 3), dtype=np.uint8) * 255

    # Step 4: Place the rectangle image in the center of the square image
    x_offset = (square_size[1] - rectangle_image.shape[1]) // 2
    y_offset = (square_size[0] - rectangle_image.shape[0]) // 2
    square_image[y_offset:y_offset+rectangle_image.shape[0], x_offset:x_offset+rectangle_image.shape[1]] = rectangle_image

    # Step 5: Save or display the resulting square image
#     cv2.imwrite(output_image_path, square_image)
    
    
    
    
    
    
    
    
    
    
    
    
    
def model_prediction_(img_path):
    face_flag = 0
    try:
#         img_path_='123.jpg'
        pad_to_square(img_path, img_path_)
        resp = RetinaFace.detect_faces(img_path_)
        if isinstance(resp, dict) and 'face_1' in resp:
            print("Human face detected!")
            face_flag = 1
            score = resp['face_1']['score']
            #img_=cv2.imread(img_path)
            #img__=pad_to_square(img_)
            landmarks = resp["face_1"]["landmarks"]
            left_eye = landmarks["left_eye"]
            right_eye = landmarks["right_eye"]
            nose = landmarks["nose"]
            # align the original image with respect to the eye coordinates
            
            
            img = cv2.imread(img_path_)
            img_aligned = postprocess.alignment_procedure(img, right_eye, left_eye, nose)
            img = img_aligned
            #img = cv2.cvtColor(img_aligned, cv2.COLOR_BGR2RGB)
            #img = cv2.cvtColor(img_aligned, cv2.COLOR_BGR2GRAY)
            print(f"Score: {score}")
#             cv2.imwrite('img_aligned.jpg',img_aligned)
            
        else:
            print("Human face not detected!")
            img = cv2.imread(img_path)
#             print("Here it is locked1")
           
    except:
        print("Human face not detected!")
#         print("Here it is 2nd locked")
        img = cv2.imread(img_path)
    return face_flag, img





