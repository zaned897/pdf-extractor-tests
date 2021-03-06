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
FILE = 'LRT001.pdf'
images = convert_from_path(FILE, dpi=350, grayscale=True)

dictionaries = []


for image in images:
    dictionaries.append(pt.image_to_data(image, output_type=Output.DICT))



# %%  PROTOTYPE FUNCTION TO THE GET THE CENTER OF MASS OF THE SUSPECTS
page = 3
TOPIC = ['TOTAL', 'PAID']
topic_coords = []
for index, word in enumerate(dictionaries[page]['text']):
    if word.upper() in TOPIC:
        #print(dictionaries[1]['top'][i],dictionaries[0]['left'][i],dictionaries[0]['text'][i])
       topic_coords.append(intersection.center_of_mass(dictionaries[page], index))

#print(dictionaries[0]['text'])
print('The center of mass for the suspects are:', f'{topic_coords}')

#%%
#%     VISUALIZATE THE CENTRAL POINTS

plt.figure(figsize=(23,20))
image_res = np.array(images[page])

inter = []
for (x,y) in topic_coords:
    #print(x,y)
    cv2.circle(image_res, center= (x[1],x[0]), radius=10, color=(0), thickness=15)

plt.imshow(image_res,cmap='gray')

# %%   INTERSECTION TEST 1
y_coords = []
x_coords = []

for (x ,y) in topic_coords:
    x_coords.append(x)
    y_coords.append(y)
#%
for index, word in enumerate(dictionaries[page]['text']):
        top = dictionaries[page]['top'][index] + dictionaries[page]['height'][index] // 2
        left = dictionaries[page]['left'][index] + dictionaries[page]['width'][index] // 2
        if any(abs(top-np.array(x_coords)) < 300 ) and any(abs(left-np.array(y_coords)) < 300 ) and not(word.upper() in TOPIC) and (word!=''):
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
#%% INSTERSECTION TEST 4

# get the word in the same row 
words_in_row =[]
for index, word in enumerate(dictionaries[page]['text']):
    t2 = dictionaries[page]['top'][index]
    h2 = dictionaries[page]['height'][index] + t2
    l2 = dictionaries[page]['left'][index]
    w2 = dictionaries[page]['width'][index] + l2
    [words_in_row.append((word,l2,w2)) for coord in topic_coords if h2>coord[0][0] and t2 < coord[1][0] and word != '' and not word.upper() in TOPIC]

#get the word in row if they are in  the same column

words_in_inter = []

for match in words_in_row:
    l2 = match[1]
    w2 = match[2]

    [words_in_inter.append(match[0]) for coord in topic_coords if l2 < coord[1][1] and w2 > coord [0][1]]

print(words_in_inter)
# %%
#plt.figure(figsize=(17,15))
#plt.imshow(np.array(images[0]), cmap='gray')


for index, field in enumerate(dictionaries[0]):
    
    print(field, dictionaries[0][field][10:15])