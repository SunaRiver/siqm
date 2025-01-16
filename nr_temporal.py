import cv2
import numpy as np


def temporal(imgPath):
    image = cv2.imread(imgPath)
    image = np.array(image)
    sum = 0.0
    x, y = 0, 0
    height, width, channel = image.shape

    # GET AVERAGE OF IMAGE
    averageImage = 0
    sumAVG = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):
                sumAVG += image[i][j][k]
    averageImage = sumAVG / (height * width)

    # GET MSE
    sumMSE = 0
    mse = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):
                temp = (image[i][j][k]-averageImage)**2
                sumMSE += temp
    mse = sumMSE/(width*height)
    return round(mse)

    # for x in  range(width):
    #     for y in range(height):
    #         difference = (A[x,y] - B[x,y])
    #         sum = sum + difference*difference
    # mse = sum /(width*height)
    # print("The mean square error is %f\n",mse)


def mses(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    imageA = cv2.imread(imageA)
    imageA = np.array(imageA)
    imageB = cv2.imread(imageB)
    imageB = np.array(imageB)
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err