from paddleocr import PaddleOCR
# from PIL import Image
import datetime
import cv2
import sys
import os
import os.path
import re
import numpy as np
import predict

def info_fetch( img):
    name = ''
    dates = ''
    gender = ''
    aadhar_number = ''
    vid = ''
    dob_match = False
    gender_match = False
    #resize the image
    img = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    #convert the image to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    OCR = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)
    text = OCR.ocr(img, cls=True)
    print(text)
    ocr_output = text
    test_list = list()
    try:
        for i in range(len(ocr_output[0])):
            test_list.append(ocr_output[0][i][1])
        #     print(ocr_output[0][i][1])
        threshold = 0.8
        filtered_data = [(text, confidence) for text, confidence in test_list if confidence >= threshold]
        res = [lis[0] for lis in filtered_data]
        # Define regex pattern to match any word in "government of India" in any case
        pattern = re.compile(r'\b(?:government|Govermanorn|covernment|gavernment|-Govemment|Goyernment|Goremment|Gayernmemofindia|Govemment of ndla|GOVEANMENT|Govemment|Govemaerit.ofudin)\b', re.IGNORECASE)
        print(res)
        for index, word in enumerate(res):
            # Search for the pattern in the current string
            match = pattern.search(word)
            # If a match is found, extract and print it
            if match:
    #             result = find_next_string(res)
    #             name = result
                print ("Aadhar card is valid and the details are below:")
                break
        for text in res:
    #         name_pattern = re.compile(r'^(?!.*:)(?=.*\s)([A-Za-z]{3,}(?: [A-Za-z]{3,})+)\b')
     #re.compile(r'^(?!.*:)(?=.*\s)([A-Za-z]{3,}+\s[A-Za-z]{3,}+)$')     # Exclude specific prefixes #name pattern
    #         name_match= name_pattern.search(text)
            issue_date_pattern = re.compile(r'issue|issuedate|download|downloaddate|issue date|ssue date|ssue')
            issue_date_match = re.search(issue_date_pattern, text.lower())
            if not issue_date_match:
                dob_pattern = re.compile(r'(?:db|/db|/dob|/dob:|dob:|/d8:|/d08|/008.|do|/do|ob|/db:|db|fh/q:|date ofirth/dob:|/d0b||date ofirth:/|date of birth|date of birth/dob:|date of birth/db:|/|birth|/date of birth)(\d{2}/(0[1-9]|1[0-2])/\d{4})')#     dob pattern
                dob_match = re.search(dob_pattern, text.lower())
            p = re.compile('d+/d+/d+/d+') #second pattern
            year_of_birth_pattern = re.compile(r"(?:yearofirth|year0fbinn:|/yearof|/year|yearb|year|/year of birth|year of birth|/year of birth|/yearlbh|/yearofbirth|yearofbirth)(\d{4})") #yob pattern
            year_match= re.search(year_of_birth_pattern, text.lower())
            gender_p= re.compile(r"/FE|FE|fe", re.IGNORECASE) #gender pattern
            gender_match = re.search(gender_p, text.lower())
            
            vid_check_pattern = re.compile(r'vid|vd |vi|vjd')
            vid_check_match = re.search(vid_check_pattern, text.lower())
            if not vid_check_match:
                aadhar_pattern = re.compile(r'\b\d(?:\s?\d){11}\b(?<!vid)(?<!vjd)')  #aadhar pattern re.compile(r'\b(?:\d[ -]*){12}\b(?<!vid)(?<!vjd)')#
                aadhar_match = re.search(aadhar_pattern, text.lower())
            vid_pattern = re.compile(r'\b(vi?d|vjd|vjd:|vid:)[:\s]*((\d\s*){16})\b')
    # re.compile(r'\b(vid|vid:|vd|id:)(\d{16})\b') #vid pattern
            vid_match = re.search(vid_pattern, text.lower())
             # If a name (sequence of alphabetic characters without digits) is found, extract and print it
    #         if name_match and not any(char.isdigit() for char in name_match.group(1)):  # Check if the matched string contains no digits
    #             name = name_match.group(1) 

            if (p.findall(text)):
                dates=p.findall(text)
            if (dob_match):
                dates = dob_match.group(1)
            if (year_match):
                dates = year_match.group(1)
            if (gender_match):
                print('TRUE')
                gender = 'Female'
            if (aadhar_match):
                aadhar_number=aadhar_match.group()
            if (vid_match):
                vid = vid+text
        return dates, gender, aadhar_number, vid,res
    except:
        return 'null', 'null', 'null', 'null','null'

    
    

