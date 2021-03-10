''' Types of questoins in the english language and create an engine to tackle these types of questions'''

'''Various types of questions available are as follows :
1) general question 
2) special or what type of questions
3) choice questions 
4) disjunctive or type question'''

import spacy
from pre_process import tolower_

#loading the spacy dataset 
spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")

def qtype_(sentence):
    if len(sentence) == 0: 
        type_ = None
        return type_
    else :
        sent_nlp = sentence
        usr = []
        for char in sent_nlp:
            usr.append(char)
        len_usr = len(usr)
        if (usr[0].pos_ == "AUX" and usr[1].pos_ == "PRON") or (usr[0].pos_ == "AUX" and usr[0].pos_ == "DET"):
            type_ = "GEN"
            for j in usr:
                if j.text == "or" and j.pos_ == "CCONJ":
                    type_ = "CHC"
        elif (usr[0].pos_ == "PRON" and usr[1].pos_ == "AUX"):
            type_ = "SPE"
            for k in usr:
                if k.text == "or" and k.pos_ == "CCONJ":
                    type_ = "CHC"
        else :
            if (usr[0].pos_ == "PRON" and (usr[len_usr - 1].pos_ == "PRON" and usr[len_usr - 2].pos_ == "PART" and usr[len_usr - 3].pos_ == "AUX" )):
                type_ = "TAG"
            else :
                type_ = None
        return type_


