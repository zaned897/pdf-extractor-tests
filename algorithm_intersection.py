"""
Experimental code for lossruns topics search,

Algorithm 3: Intersection search
version: 0.6
@author: Asymm Developers
date: Jan 2020
"""


# %%  loasd dependencies import lossruns.intersectionimport pytesseract as pt
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import pytesseract as pt
from lossruns import intersection
from pdf2image import convert_from_path
from pytesseract import Output
from configobj import ConfigObj
#%   read data
FILE = 'cross_test.pdf'
images = convert_from_path(FILE, dpi=350, grayscale=True)
dictionaries = []


for image in images:
    dictionaries.append(pt.image_to_data(image, output_type=Output.DICT))



#   PROTOTYPE FUNCTION TO THE GET THE CENTER OF MASS OF THE SUSPECTS
page = 0
TOPIC = ['TOTAL', 'PAID']
topic_coords = []
for index, word in enumerate(dictionaries[page]['text']):
    if word.upper() in TOPIC:
        #print(dictionaries[1]['top'][i],dictionaries[0]['left'][i],dictionaries[0]['text'][i])
       topic_coords.append(intersection.center_of_mass(dictionaries[page], index))

#print(dictionaries[0]['text'])
print('The center of mass for the suspects are:', f'{topic_coords}')


#%%     VISUALIZATE THE CENTRAL POINTS
plt.figure(figsize=(23,20))
image_res = np.array(images[page])

inter = []
for (x,y) in topic_coords:
    #print(x,y)
    cv2.circle(image_res, center= (y,x), radius=10, color=(0), thickness=15)

plt.imshow(image_res,cmap='gray')
#%%     INTERSECTION TEST 1
y_coords = []
x_coords = []

for (x ,y) in topic_coords:
    x_coords.append(x)
    y_coords.append(y)

for index, word in enumerate(dictionaries[page]['text']):
        top = dictionaries[page]['top'][index] + dictionaries[page]['height'][index] // 2
        left = dictionaries[page]['left'][index] + dictionaries[page]['width'][index] // 2
        if any(abs(top-np.array(x_coords)) < 50 ) and any(abs(left-np.array(y_coords)) < 50 ) :
            #print(top - np.array(x_coords))
            #print(left - np.array(y_coords))
            print (word)

#%% INTERSECTION TEST 3
for index, word in enumerate(dictionaries[page]['text']):
        top = dictionaries[page]['top'][index]
        left = dictionaries[page]['left'][index]
        candidate = (abs(top-np.array(x_coords)) < 100 ) & (abs(left-np.array(y_coords)) < 100 )
        print(word)
        print(abs(top-np.array(x_coords))) 
        print(abs(left-np.array(y_coords)))
        
#        if any(candidate):
#            print(top - np.array(x_coords))
#            print(left - np.array(y_coords))
#            print (word)

