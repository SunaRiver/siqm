import os
import time
import cv2
import subprocess
import shlex
import numpy as np
from nr_blur_marziliano import blurmetric
from nr_activity import activitymetric
from nr_temporal import mses
from nr_block import blockmetric

def scoring(com):
    list_blok = []
    list_blur = []
    list_act = []
    list_temporal = []
    first_freeze = 1
    count_freeze = 0
    act_score = 0
    
    # running screenshot -frames:v 20 take screenshot 20 images
    command = com
    subprocess.call(shlex.split(command))
    dir_path = r'/'
    pathImg = []

    #print("================== Start Add Image ======================")
    # Iterate directory
    for path in os.listdir("image"):
        # check if current path is a file
        if(path[0:6] == "output"):
            pathImg.append(path)

            
    print("================== START SCORING ============================")
    for i in range(1, len(pathImg)+1):
        print(f"======== scoring {i} ===================")
        image = cv2.imread(f"./image/output{i}.jpg")
        
        #blur_function_call
        blur = blurmetric(f"./image/output{i}.jpg")
        list_blur.append(blur)
        print(f"blur:{list_blur}")
        
        #blok_function_call
        blok = blockmetric(f"./image/output{i}.jpg")
        list_blok.append(blok)
        print(f"blok:{list_blok}")
        
        #act_function_call
        act=activitymetric(f"./image/output{i}.jpg")
        list_act.append(act)
        print(f"act:{list_act}")
        
        
        # Logic For Temporal
        try:
            treshold = 1
            if(i == 1):
                temporalNow = 2; #Tidak perlu dicompare dengan frame sebelum untuk frame pertama.
            else:
                temporalNow = mses(
                        f"./image/output{i}.jpg", f"./image/output{i-1}.jpg")
            
            if(temporalNow <= treshold):
                list_temporal.append(1)
                count_freeze += 1 
            else:
                list_temporal.append(0)       

            if(i == 2 and temporalNow <= treshold): #Jika frame kedua freeze maka frame kesatu dianggap freeze
                list_temporal[0]=1
            elif (i == 2 and temporalNow > treshold):
                list_temporal.append(0)
        except:
            list_temporal.append(0)
        print(f"freeze = {list_temporal}")
    
    #merata-ratakan masing-masing metrik untuk seluruh frame yang diukur
    blok_score = round(sum(list_blok)/len(list_blok))
    blur_score = round(sum(list_blur) / len(list_blur))
    temp_score = round((1-sum(list_temporal)/len(list_temporal))*100)
    act_score = round(sum(list_act) / len(list_act),1)
        
    list_act = np.array(list_act)
    act_std = round(np.std(list_act),1)
    
    
    #dependent antara blur terhadap blok
    if(blok_score<80):   
        blur_score = round(50+blur_score/10)
    elif(blok_score<90):
        blur_score = round(70+blur_score/10)
    elif(blok_score<=100):
        blur_score = round(90+blur_score/10)
        
    #dependent temporal act_score terhadap std nya
    if(act_score<0):
        act_score = round(50+act_score)
    if(act_std-act_score>2):
        act_score = round(75-act_score)
    else:
        act_score =round(100-act_score)
    
    #memasukkan hasil pengukuran ke array
    dataAll = {
        "blok": blok_score, 
        "blur": blur_score, 
        "temp": temp_score,
        "act" : act_score
    }
    
    print(dataAll)

    for i in range(1, len(pathImg)+1):
        os.remove(f"./image/output{i}.jpg")
        
    return dataAll
