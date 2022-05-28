from os import system
import sys
from time import sleep
import cv2
import numpy as np

#Configuration
DOWNSCALE_FACTOR = 50
FPS_DELAY = 1/75
ASCII_CHARS =  [' ','.',':',';','+','=','x','X','$','&']

interval_coefficient = (len(ASCII_CHARS)-1)/255

#Transform a RGB image to grayscale
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    grayImage = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return grayImage

#Transform a grayscale frame to ASCII art
def frameToAscii(frame):
    output_string = ""
    height = frame.shape[0]
    width = frame.shape[1]
    new_width =int((width / height)*DOWNSCALE_FACTOR)
    resized_frame = cv2.resize(frame, (new_width, DOWNSCALE_FACTOR), interpolation = cv2.INTER_AREA)

    #Working with numpy arrays instead of lists is more efficient.
    rendered_frame = np.zeros((DOWNSCALE_FACTOR, new_width), dtype=np.int8)
    for i in range(DOWNSCALE_FACTOR):
        for j in range(new_width):
            rendered_frame[i][j] = int(resized_frame[i][j]*interval_coefficient)

    for i in range(DOWNSCALE_FACTOR):
        for j in range(new_width):
            output_string += ASCII_CHARS[rendered_frame[i,j]]
        output_string += "\n"
    print(output_string)


#Read video from path and loops through each frame
def renderVideo(vidcap):
    success,image = vidcap.read()
    system("mode con:cols=" + str(image.shape[1]+1) + " lines=" + str(image.shape[0]))
    count = 0
    while success:
        sleep(FPS_DELAY)
        gray_image = rgb2gray(image)
        frameToAscii(gray_image)    
        success,image = vidcap.read()
        count += 1

    #If we pass a picture instead of a video
    if count==1:
        sleep(10)


#main function call
if __name__ == "__main__":
    if len(sys.argv) in (2,3):
        try:
            vidcap = None
            if len(sys.argv) == 3 and sys.argv[0] in ("python", "python3", "python2"):
                vidcap = cv2.VideoCapture(sys.argv[2])
            else:
                vidcap = cv2.VideoCapture(sys.argv[1])
            renderVideo(vidcap)
        except:
            print("media file is broken or doesn't exist.")
    else:
        print("Please specify the file you want to convert to ASCII.:\nexample (CMD): main.py video.mp4")