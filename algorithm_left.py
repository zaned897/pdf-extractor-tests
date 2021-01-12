"""
Experimental code for lossruns topics search, cross search Algorithm


version: 0.6
@author: Asymm Developers
date: Jan 2020
"""

# %%                                LOAD DEPENDENCIES
import lossrun
import pytesseract as pt
from configobj import ConfigObj
from pytesseract import Output
from pdf2image import convert_from_path
import spacy



# %%                                READ DATA 
print("Readind data...")
_file = '/home/zned897/Proyects/pdf_text_extractor/test_lossruns/LRT004.pdf'
pages = convert_from_path(_file, dpi=350, thread_count=7,grayscale=True)

dictionaries = []

for page in pages:
    dictionaries.append(pt.image_to_data(page, output_type=Output.DICT))
    


#%%                                OCR AND RULES                         
print("Applying ocr rules and rules ...")
TOPICS = ConfigObj('config_topic.ino')
ENTS = ConfigObj('config_ents.ino')
suspects = lossrun.search_rules(dictionaries[0], rules= TOPICS)
spatial_filter = lossrun.spatial_filter(dictionaries[0], suspects, 'LOSSRUN') 
pass


# %%                                    NLP 
EXTERNAL_RULE = ['indemnity', 'expenses']
try:
    nlp('model?')
except:    
    print('loading model...')
    nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('/home/zned897/Proyects/pdf_text_extractor/external_models/lossruns_models/lossrun_ner_jan112021')
for suspect, topic in enumerate(suspects):
    #print("Searching for topic: " + topic[0])
    #print("With ents: " + f'{ENTS[topic[0]]}')
    #print('in sentense: ' + ' '.join(spatial_filter[suspect]))
    
    sent_vert = nlp(' '.join(spatial_filter[(suspect*2+1)-1][0])) #0 2
    sent_horix = nlp(' '.join(spatial_filter[suspect*2+1][0]))    #1 3 
    
    for ent in sent_vert.ents:
        if ent.label_ in ENTS[topic[0]]:
            print(topic[0] + ': ' + ent.text)
            print("FOUNDED IN VERTICAL")
            # save result and if is long search cntinue, if not: break
            # if ENTS[topic[0]] not in EXTERNAL_RULE:
            #    break
    
    for ent in sent_horix.ents:
        if ent.label_ in ENTS[topic[0]]:
            print(topic[0] + ': ' + ent.text)
            print("FOUNDED IN HORIZONTAL")
       

#doc = nlp(' '.join(spatial_filter[0]))
#for ent in doc.ents:
#    print(ent.label_, ent.text)