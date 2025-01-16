import os
import cv2
import numpy as np

def activitymetric(targetImage):
    # convert image to grayscale
    imageInput = cv2.imread(targetImage, cv2.IMREAD_GRAYSCALE)
    image2Input = imageInput.astype(float)
    imageSize1 = imageInput.shape[0]
    imageSize2 = imageInput.shape[1]
    imageSize = imageSize1 * imageSize2
    IAME = 0
    nilai = 0
    IAMG_vert = 0
    IAMG_horz = 0

    # IAM from Edges
#     eImage = cv2.Canny(imageInput, 100, 200)

#     for n in range(imageSize):
#         IAME += eImage.ravel()[n]

    # IAM from Gradient
    # Vertical
    gx = np.abs(np.diff(image2Input, axis=1))
    gy = np.abs(np.diff(image2Input, axis=0))

    IAMG_vert = gx.sum()
    IAMG_horz = gy.sum()

    IAMgrad = round(-(IAMG_vert-IAMG_horz)/imageSize,1)
    nilai = IAMgrad

#     if(IAMgrad > 1):
#         nilai = 0
#     elif(IAMgrad > 0 and IAMgrad <= 1):
#         nilai = 2
#     elif(IAMgrad < 0):
#         nilai = 1


    return nilai
