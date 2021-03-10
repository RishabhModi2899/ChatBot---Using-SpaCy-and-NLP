#PRE-PROCESSING OF THE TEXT FUNCTIONS
import json 
import spacy

#loading the spacy dataset 
spacy.prefer_gpu()
nlp = spacy.load("en_core_web_md")

#load the json file 
with open("C:/Users/rishabh_2/Documents/python projects/chatbot/chatbot ver 5/json files/intents.json") as file:
    data = json.load(file) 

#creating the tags dictionary and the response dictionary
count = 0
ctr = 0
tags_dict = {}
resp_dict = {}
for intent in data['intents']:
    count += 1
    tags_dict[count] = intent['tag']
for res in data['intents']:
    ctr += 1
    resp_dict[ctr] = res['response'] 

def tolower_(sentence):
    ''' to convert the input to lower case '''
    return sentence.lower()

def removepunct_(sentence):
    ''' to remove the punctuation from the input '''
    punctuations = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in sentence.lower():
        if x in punctuations:
            sentence = sentence.replace(x , "")
    return sentence

def svo_(doc):
    ''' Returns the sub verb and object of the sentence '''
    sub = []
    verb = []
    obj = []
    for i in doc:
        if i.pos_ == "NOUN":
            sub.append(i.text)
        elif i.pos_ == "VERB":
            verb.append(i.text)
        elif i.pos_ == "PROPN":
            obj.append(i.text)
        else :
            pass
    res_str = []
    for a in sub :
        res_str.append(a)
    for b in verb :
        res_str.append(b)
    for c in obj :
        res_str.append(c)
    return " ".join(res_str)

def _similarity(SVO , tags):
    ''' This is a function that will create a dictionary of similarities between the user input and the tags list created from the JSON file '''
    res_sim = {}
    temp = []
    count = 0 
    for i in tags.values():
        temp.append(i)
    for j in temp :
        count += 1
        cmp = nlp(j)
        res_sim[count] = cmp.similarity(SVO)
    return res_sim

def maximum(dict1):
    ''' This is a function to extract the key with the maximum value pair '''
    temp = []
    max_temp = 0
    res = 0
    for i in dict1.values():
        temp.append(i)
        max_temp = max(temp)
    for j in dict1.keys():
        if dict1[j] == max_temp:
            res = j
    return res

def response_(max_key , resp_dict):
    ''' This is a function to generate responses to the queries of the user '''
    for i in resp_dict.keys():
        if i == max_key:
            resp = resp_dict[i]
            res = resp[0]
    return res 

#driver function
def pre_process(chk , user):
    ''' Driver function to perform pre-processing '''
    #pre-process the user input
    #lower case 
    user_inp = tolower_(user)
    #remove punctuations
    user_inp_rp = removepunct_(user_inp)
    #convert to doc type 
    user_inp_nlp = nlp(user_inp_rp)
    #extracting the Subject verb object
    svo = svo_(user_inp_nlp)
    #converting the svo to doc type
    svo_nlp = nlp(svo)
    return svo_nlp
