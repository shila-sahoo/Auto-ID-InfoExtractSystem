from ultralytics import YOLO
from paddleocr import PaddleOCR
import os
import cv2
labels = {
    'aadhaar_body': 0.0
}

def aadhar_body_prediction(img):
    res = []
    try: 
        result = ''
        file_path0 = os.path.abspath(os.path.join(os.path.dirname('__file__'), ".."))
        model_path = os.path.join(file_path0, 'aadhar_information_fetch','model_weight','aadhar_body.pt')
        model = YOLO(model_path)
    #     try:
        results = model(conf=0.30, source=img)[0]  # results list
#         img = cv2.imread(image_path)
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            if class_id == 0.0:   
                image_crop = img[int(y1):int(y2), int(x1):int(x2), :]
#                 cv2.imwrite('adhar_body_test.jpg', image_crop)
                img = cv2.resize(image_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                #convert the image to gray
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                OCR = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)
                text = OCR.ocr(img, cls=True)
#                 print(text)
                ocr_output = text
                test_list = list()
                len(ocr_output[0])
                for i in range(len(ocr_output[0])):
                    test_list.append(ocr_output[0][i][1])
                #     print(ocr_output[0][i][1])
                threshold = 0.8
                filtered_data = [(text, confidence) for text, confidence in test_list if confidence >= threshold]
                res = [lis[0] for lis in filtered_data]
#                 pattern = re.compile(r'[0-9/]+')
#                 dob = ''.join(pattern.findall(' '.join(res)))
#                 print("date of birth", dob)
                
                print("Name of the aadhar is:", result)
                return res
        
#                 break
        
    except:
        print("Name is not detected")
        return res
            
# aadhar_prediction('/workspace/nemo/data/aadhar_information_fetch/snehendu/190704220000018_aadhaar.jpg')