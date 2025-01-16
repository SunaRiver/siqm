from numpy.core.fromnumeric import mean
import math
import numpy as np
#import cv2
from time import process_time
from time import sleep
import matplotlib.image as img


def rgb2gray(rgb):  # RGB2GRAY Matlab format ITU-R
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = np.round(0.299 * r + 0.587 * g + 0.114 * b)
    #gray = np.ceil(0.299 * r) + np.ceil(0.587 * g) + np.ceil(0.114 * b)
    #gray = 0.299 * r + 0.587 * g + 0.114 * b
    return gray

# from statistics import mean


def blockmetric(im_path):
    #path1 = f"/content/img_ref/{2}.jpg"
    imgInput = img.imread(im_path)

    t1_start = process_time()

    M, N, c = imgInput.shape  # Size of image
    #print('Image size = ', imgInput.shape)

    if c == 3:
        targetImage = rgb2gray(imgInput)  # If RGB change to GRAYscale

    x = np.array(targetImage)
    #print('Gray Image size = ', x.shape)

    # Feature Extraction:
    # ----------  1. Horizontal features ----------
    d_h = x[:, 1:(N)] - x[:, 0:(N-1)]
    #print('d_h size = ', d_h.shape)

    # your_list[start:end:jump]
    B_h = mean(abs(d_h[:, 7:8*(math.floor(N/8)-1):8]))
    #print('B_h = ',B_h)

    A_h = (8*mean(abs(d_h))-B_h)/7
    #print('A_h = ', A_h)

    sig_h = np.sign(d_h)  # 1 if more than 0, 0 if 0, -1 if less than 0
    left_sig = sig_h[:, 0:(N-2)]
    right_sig = sig_h[:, 1:(N-1)]
    # rata-rata dari jumlah seluruh data yang zero crossing secara horizontal
    Z_h = mean((left_sig*right_sig) < 0)
    #print('Z_h = ', Z_h)

    # 2. ---------- Vertical features ----------
    d_v = x[1:M, :] - x[0:(M-1), :]
    #print('d_v size= ', d_v.shape)

    # your_list[start:end:jump]
    B_v = mean(abs(d_v[7:8*(math.floor(N/8)-1):8, :]))
    #print('B_v = ', B_v)

    A_v = (8*mean(abs(d_v))-B_v)/7
    #print('A_v = ', A_v)

    sig_v = np.sign(d_v)  # 1 if more than 0, 0 if 0, -1 if less than 0
    up_sig = sig_v[0:(M-2), :]
    down_sig = sig_v[1:(M-1), :]
    # rata-rata dari jumlah seluruh data yang zero crossing secara vertical
    Z_v = mean((up_sig*down_sig) < 0)
    #print('Z_v = ',Z_v)

    # 3. ---------- Combined features ----------
    B = (B_h + B_v)/2
    A = (A_h + A_v)/2
    Z = (Z_h + Z_v)/2
    #print('B = ', B, 'A = ', A, 'Z = ', Z)

    # Quality Prediction

    alpha = -245.8909
    beta = 261.9373
    gamma1 = -239.8886
    gamma2 = 160.1664
    gamma3 = 64.2859

    score = alpha + beta*((B**(gamma1/10000)) *
                          (A**(gamma2/10000))*Z**(gamma3/10000))
    if math.isnan(score):
        vq = 0
    else:
        vq = round(score*10)
        if vq > 100:
            vq = 100
        elif vq < 0:
            vq = 0

    t1_stop = process_time()
    #print("Elapsed time:", t1_stop-t1_start)
    # print(vq)
    return vq

# while (True):
#   hasil = blockmetric("/home/pi/vlc_snap/scene.jpg")
#   print('vq = ', hasil)
#   time.sleep(5)

# list_hasil = []
# for i in range(500):
#     list_hasil.append(blockmetric(f"C:/Users/affaa/Downloads/IMG_DISTORTED/image_distorted/{i+1}.jpg"))
#     print(i+1)


# dataset = {"Block":list_hasil}
# df = pd.DataFrame(dataset)
# df.to_csv("BLOCK_Dataset.csv")
