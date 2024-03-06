# from paddleocr import PaddleOCR,draw_ocr
#from retinaface import RetinaFace
from datetime import datetime
from ultralytics import YOLO
import numpy as np
import info_fetch
# import easyocr
import textstat
import datetime
import predict
import cv2
import sys
import re
import os

# project_root_path=os.path.abspath(os.path.join(os.path.dirname('__file__'), ".."))

labels = {
    'aadhaar': 0.0,
    'aadhaar_back': 6.0
}

# def extract_text_from_image(extracted_text):
# #     reader = easyocr.Reader(['en'])  # Specify language (e.g., English)
# #     extracted_text = reader.readtext(img_path)
#     return ' '.join([text[1] for text in extracted_text])

# def analyze_readability(text):
#     score = ''
#     dob = ''
#     try:
#         # Calculate Flesch Reading Ease
#         flesch_score = textstat.flesch_reading_ease(text)

#         # Calculate Flesch-Kincaid Grade Level
#         grade_level = textstat.flesch_kincaid_grade(text)

#         # Calculate Automated Readability Index (ARI)
#         ari_score = textstat.automated_readability_index(text)

#         print("Readability Analysis:")
#         print(f"Flesch Reading Ease: {flesch_score}")
#         print(f"Flesch-Kincaid Grade Level: {grade_level}")
#         print(f"Automated Readability Index (ARI): {ari_score}")
#         return flesch_score, ari_score
#     except Exception as e:
#         print(f"Error analyzing readability: {e}")
    

def aadhar_prediction(image_):
    dob = ''
#     cv2.imwrite("aadhar_prediction.jpg",image_)
    res = []
    file_path0 = os.path.abspath(os.path.join(os.path.dirname('__file__'), ".."))
    model_path =os.path.join(file_path0, 'aadhar_information_fetch','model_weight','best.pt')#'/workspace/nemo/data/aadhaar_detection/aadhaar_detection_vid/aadhar_detection_v3/model_result5/YV8/weights/best.pt'
    model = YOLO(model_path)
    try:
        results = model(conf=0.30, source=image_)[0]  # results list
    #         print(results)
        #img = cv2.imread(image_path)
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            if class_id == 0.0:  
    #                 print("aadhar_detected")
                image_crop = image_[int(y1):int(y2), int(x1):int(x2), :]
    #             reader = easyocr.Reader(['en'])  # Specify language (e.g., English)
    #             extracted_text = reader.readtext(image_path)
    #             extracted_text = extract_text_from_image(extracted_text)
    #             print(extracted_text)
    #             extracted_text = extract_text_from_image(image_path)
    #             score, index = analyze_readability(extracted_text)
                res = predict.aadhar_body_prediction(image_crop)
                print(res)
                dates, gender, aadhar_number, vid, res_all = info_fetch.info_fetch(image_crop)
                if len(res)!= 0:
                    name_pattern = re.compile(r'\b(?:government|Govermanorn|covernment|gavernment|-Govemment|Goyernment|Goremment|Gayernmemofindia|Govemment of ndla|GOVEANMENT|Govemment|Govemaerit.ofudin|india|ofindia)\b', re.IGNORECASE)
                    name_match = re.search(name_pattern, res[0])
                    if name_match or len(res[0])<3:
                            name_aadhar = res[1]
                    else:
                        name_aadhar = res[0]
                    if gender == '':
                        gender = "Male"
                    if dates == '':
                        pattern = re.compile(r'\b\d+\b')
                        matches = list()
                        for text1 in res:
    #                         print(text1, "aadhar_body")
                            matches = pattern.findall(text1)
                            print(matches)
                            print(type(matches))
                            if len(matches)>=3:
                                day = matches[0].zfill(2)
                                month = matches[1].zfill(2)
                                year = matches[2]
                                # Format the date as dd/mm/yyyy
                                dates = f'{day}/{month}/{year}'
                            if len(matches) == 1:
                                dates = datetime.strptime(date_list[0], '%Y').strftime('%Y')
                else:
                    name_aadhar = "Not readable"
                a_no = re.sub(r'[^0-9]', '', aadhar_number)
                vid_no = re.sub(r'[^0-9]', '', vid)
                if gender == '' and name_aadhar == "Not readable":
                    gender = "Not readable"

                return {
    #                     'score': score,
    #                     'index': index,
                        'name': name_aadhar, 
                        'dob': dates,
                        'gender': gender, 
                        'aadhar_number': a_no, 
                        'vid': vid_no,
                        'message': 'Success'}
    #                     'ocr-result': res_all,
    #                     'ocr-body-result': res}
            elif class_id == 6.0:
                print("Aadhar back is detected")
    except:
        return{
#                 'score': "NULL",
#                 'index': "NULL",
                'name': "NULL", 
                'dob': "NULL",
                'gender': "NULL", 
                'aadhar_number': "NULL", 
                'vid': "NULL",
                'message': 'Aadhar not detected'}
#                 'ocr-result': res_all,
#                 'ocr-body-result': res}


