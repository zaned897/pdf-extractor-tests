"""
Experimental code for lossruns topics search,

Algorithm 1 and 2: Left and Right search.


version: 0.6
@author: Asymm Developers
date: Jan 2020
"""

# %%                                LOAD DEPENDENCIES
import lossruns.left_bottom
import pytesseract as pt
from configobj import ConfigObj
from pytesseract import Output
from pdf2image import convert_from_path
import spacy



# %%                                READ DATA 
print("Readind data...")
_file = 'LRT001.pdf'
pages = convert_from_path(_file, dpi=350, thread_count=7,grayscale=True)

dictionaries = []

for page in pages:
    dictionaries.append(pt.image_to_data(page, output_type=Output.DICT))
    


#%%                                OCR AND RULES                         
print("Applying ocr rules and rules ...")
TOPICS = ConfigObj('config_topic.ino')
ENTS = ConfigObj('config_ents.ino')
suspects = lossrun.search_rules(dictionaries[0], rules= TOPICS)
spatial_filter_ver, spatial_filter_hor = lossrun.spatial_filter(dictionaries[0], suspects, 'LOSSRUN') 
pass
pass


# %%                                    NLP 
EXTERNAL_RULE = ['indemnity', 'expenses']
try:
    nlp('model?')
except:    
    print('loading model...')
    nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_sm')
for suspect, topic in enumerate(suspects):
#    print("Searching for topic: " + topic[0])
#    print("With ents: " + f'{ENTS[topic[0]]}')
#    print('In vertical sentense: ' + ' '.join(spatial_filter_ver[suspect]))
#    print('In horizontal sentense: ' + ' '.join(spatial_filter_hor[suspect]))

    
    sent_vert = nlp(' '.join(spatial_filter_ver[suspect]))
    sent_horix = nlp(' '.join(spatial_filter_hor[suspect]))
    
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

    pass       

#doc = nlp(' '.join(spatial_filter[0]))
#for ent in doc.ents:
#    print(ent.label_, ent.text)
