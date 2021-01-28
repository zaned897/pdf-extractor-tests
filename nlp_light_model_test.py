"""General test for NLP improved NER model

    Reduce the size from 700M to 11M performig a big brother 
    tranfer learning. 

    Big brother: en_core_web_lg
    base model: en_core_web_sm
    result model en_core_lossruns_lexicon

version: 0.1 (test on NPDB formats)
date: jan 2021
@author: Eduardo Santos, Asymm Developers
mail: eduardo@asymmdevelopers.com
"""


#  %% load dependencies
import spacy
import numpy as np 
from pdf2image import convert_from_path
from nltk.stem.porter import *
import nltk 
import pytesseract as pt
from pytesseract import Output
import concurrent.futures
from cv2 import blur

#%%
#hard code file 
FILE = '/home/zned897/Proyects/pdf_text_extractor/nowinsurance-loss-runs/NPDB/data/NPDBQA1.pdf'
print('Reading file: ...' + str(FILE[-12:]))

# load the data
images = convert_from_path(FILE, grayscale=True, dpi=350)
print('The image size is: ' + str(np.array(images[0]).shape))


#appy image enhanced if necessary (typically a blur works fine)

#multi-threads
def main_ocr(image):
    image = np.array(image)
    image[image<=125]=0
    image[image>126] = 255
    image = blur(image, (2,2))
    return pt.image_to_data(image, output_type=Output.DICT)


#apply ocr in dictionary format #pre-proc the text applying tokenizer and  stem if needed #create sentences #label the ner in sentences using the big brother model #use the data to retrain the little broter model based on
print('Applying OCR in multi threads in ' + str(len(images))+ ' pages')
dictionaries = []
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
    results = [executor.submit(main_ocr, image) for image in images]
    for result in concurrent.futures.as_completed(results):
        dictionaries.append(result.result())

#%%      PRE-PROC THE TEXT 
import string as String
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
punkt = String.punctuation 
raw_text = ' '.join(dictionaries[2]['text'])

print(raw_text)

