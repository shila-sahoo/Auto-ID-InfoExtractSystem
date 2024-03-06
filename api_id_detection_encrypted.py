from fastapi import FastAPI, UploadFile, Body
from base64 import b64encode, b64decode
import json
import os
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response, FileResponse
#from PIL import Image
import shutil
import requests 
import hashlib
import torch
import gc
from encryption_decryption import data_security
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()

project_root_path=os.path.abspath(os.path.join(os.path.dirname('__file__'), ".."))

security_key = "Shila@123"

class id_detection_parameters(BaseModel):
    key: str
    job_id: str
    img_str: str

@app.post("/autoid")
#@app.post("/legacy_img_emb_vec")
async def id_detect(id_parameters: Annotated[id_detection_parameters, Body(embed=True)]):  
    key = id_parameters.key
    job_id = id_parameters.job_id
    img_str = id_parameters.img_str
    upload_file_path=os.path.join(project_root_path,'aadhar_information_fetch','input')
    ds = data_security()
    
    if key == security_key:
        try:
            os.mkdir(f"{upload_file_path}/{job_id}")
            #modified_filename = f"{job_id}.{file.filename.split('.')[-1]}"
            #modified_filename = f"{file.filename}"
            img_path=f"{upload_file_path}/{job_id}/input_img_{job_id}.jpg"
            ds.decrypt(img_str, img_path)
            
            
            
            #------------------------Updated this portion---------------------------------
            from inference_id_check import id_check

            doc_id = id_check(img_path)
            id_info = doc_id.aadhar_model_prediction()
            
            
#             print(id_info)
            json_info = jsonable_encoder(id_info)
            
            '''del predicted_class, confidence, potato, pot
            torch.cuda.empty_cache()
            gc.collect()'''

                 
        except:
            #total_count=0
            json_info = jsonable_encoder({'id': 'Error', 'name': 'Error', 'dob': 'Error' , 'gender': 'Error', 'aadhar_number': 'Error', 'vid':'Error'
                                         })
    else:
        json_info = jsonable_encoder({'id': 'Invalid_user', 'name': 'Invalid_user', 'dob': 'Invalid_user', 'gender': 'Invalid_user', 'aadhar_number': 'Invalid_user', 'vid':'Invalid_user' })
        
    path1=f"{upload_file_path}/{job_id}"    
    if os.path.isdir(path1):
        shutil.rmtree(path1)
    
    
    '''if os.path.isdir(path2):
        shutil.rmtree(path2)'''
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # Return a response indicating success
    return JSONResponse(content=json_info)

# Run API 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
