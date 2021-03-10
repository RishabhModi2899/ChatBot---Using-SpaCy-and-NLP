''' This is a file that will generate suggestions based on the context of previous asked question '''

#context in the case of yes/no type questions is noun
#a seperate fumction will be needed to handle choice type question 

import spacy
nlp = spacy.load("en_core_web_md")

def __context__(user_input):
    ''' function to generate fetch the context from the user request '''
    context = []
    #converting the user input to DOC type
    usr_nlp = nlp(user_input)
    for i in usr_nlp:
        if i.pos_ == "NOUN" or i.pos_ == "PROPN":
            context.append(i.text)
    return context

def __suggestion__(context_list):
    ''' this function will make the  suggestion based on the context '''

def gram(sentence):
    sent_nlp = nlp(sentence)
    for i in sent_nlp:
        print(i.pos_ , " " , i.text)

#text = "do you provide enterprise application"
#print(__context__(text)) 
#text1 = "what is enterprise application" 
#print(__context__(text1))
text2 = "who is the ceo of devit"
gram(text2)
print(__context__(text2))