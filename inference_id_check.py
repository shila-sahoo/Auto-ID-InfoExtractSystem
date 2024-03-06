import detect
from ultralytics import YOLO
import photo_checker
import tqdm
import os
import cv2

labels = {
    'aadhaar': 0.0,
    'name': 1.0,
    'dob': 2.0,
    'gender': 3.0,
    'aadhar_number': 4.0,
    'vid': 5.0,
    'aadhaar_back': 6.0
}
    
class id_check:
    
    def __init__(self, image_path:str):
        self.image_path = image_path
    
    def aadhar_model_prediction(self):
        face_check, image =photo_checker.model_prediction_(self.image_path)
        if face_check:
            info = detect.aadhar_prediction(image)
            try:
                print(info)
                return  info
            except:
                print("Empty")
        else:
            back_flag = 0
            aadhar_flag = 0
            file_path0 = os.path.abspath(os.path.join(os.path.dirname('__file__'), ".."))
            model_path =os.path.join(file_path0, 'aadhar_information_fetch','model_weight','best.pt')
            model = YOLO(model_path)
            results = model(conf=0.30, source=self.image_path)[0]  # results list
            for r in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                if class_id == 6.0: 
                    back_flag = 1
                if class_id == 0.0:
                    aadhar_flag = 1
            if back_flag == 1 and aadhar_flag == 1:
                image = cv2.imread(self.image_path)
                info = detect.aadhar_prediction(image)
                print(info)
                return  info
            elif aadhar_flag == 1:
                print("Now trying to access here")
                image = cv2.imread(self.image_path)
                info = detect.aadhar_prediction(image)
                print(info)
                return  info
            elif aadhar_flag == 0 and back_flag == 1:
                print("Aadhar back is detected")
                return{
                    'name': "NULL", 
                    'dob': "NULL",
                    'gender': "NULL", 
                    'aadhar_number': "NULL", 
                    'vid': "NULL",
                    'message': 'Aadhar back is detected'}
            else:
                return{
                    'name': "NULL", 
                    'dob': "NULL",
                    'gender': "NULL", 
                    'aadhar_number': "NULL", 
                    'vid': "NULL",
                    'message': 'Aadhar not detected'}
                
            
        
# def main():
#     image_path="/workspace/nemo/data/aadhar_information_fetch/images/male_190218220000016_aadhaar.jpg"
#     doc_id = id_check(image_path)
#     id_info = doc_id.aadhar_model_prediction()
#     print(id_info)

# if __name__ == "__main__":
#     main()