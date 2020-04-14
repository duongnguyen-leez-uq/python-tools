#============================================#
# feb 13, 2020                               #
# name: watermark remover                    #
# written by: leez_uq (and stack overflow)   #
# require: python 3.5+, opencv-python, numpy #
#============================================#

import cv2
import numpy as np

def _split_0(img, iterator = 2):
   
    # the image to grayscale
    gr = np.copy(img)
    
    # Make a copy of the grayscale image
    bg = gr.copy()

    # Apply morphological transformations
    for i in range(1, iterator+1):
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * i + 1, 2 * i + 1))
        
        bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, kernel2)
        bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, kernel2)
    
    
    # Subtract the grayscale image from its processed copy
    dif = cv2.subtract(bg, gr)

    # Apply thresholding
    bw = cv2.threshold(dif, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    dark = cv2.threshold(bg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # Extract pixels in the dark region
    darkpix = gr[np.where(dark > 0)]

    # Threshold the dark region to get the darker pixels inside it
    darkpix = cv2.threshold(darkpix, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Paste the extracted darker pixels in the watermark region
    bw[np.where(dark > 0)] = darkpix.T

    bw[bw>0] = 255
    
    return bw, bg

def split(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    ct, bg = _split_0(img)
    
    new_ct = cv2.filter2D(ct,-1,np.ones((3,3), dtype='float32')/9)
    new_bg = cv2.dilate(bg,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations = 15)
    new_img = (np.clip(img.astype('float32')/bg, 0, 1) * 255).astype('uint8')

    blank = np.ones(bg.shape, dtype='uint8') * 255
    
    rslt = np.where(new_ct < 255, new_img, blank)
    
    return ct, bg, rslt

import os

if __name__ == '__main__':
    result_fd = 'result'
    content_fd = 'content'
    background_fd = 'background'
    
    print('=======================================')
    print('                ~~UwU~~                ')
    print('=======================================')

    print('Enter the image folder path (skip if you use current working folder):')
    target = input()
    if target == '': target = os.getcwd()
    
    if not os.path.exists(result_fd):
        os.mkdir(result_fd)

    if not os.path.exists(content_fd):
        os.mkdir(content_fd)

    if not os.path.exists(background_fd):
        os.mkdir(background_fd)

    img_list = [img for img in os.listdir(target)
                if img.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'bmp']]

    print('{} image(s) found'.format(len(img_list)))
    
    for img_name in img_list:    
        try:
            img = cv2.imread(img_name)

            ct, bg, rslt = split(img)

            cv2.imwrite(result_fd + '/' + result_fd + '-' + img_name, rslt)
            cv2.imwrite(content_fd + '/' + content_fd + '-' + img_name, ct)
            cv2.imwrite(background_fd + '/' + result_fd + '-' + img_name, bg)
            
            print('[---] ' + img_name)
        except:
            print('[!!!] error :(' + img_name)
    
    exit(0)
