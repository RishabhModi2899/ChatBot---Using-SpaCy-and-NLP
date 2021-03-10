#This is a script that will be used to handle fallback mechanism of different types of questions 
import pre_process as pp
import spacy
import __main__ as m

#loading the spacy dataset
spacy.prefer_gpu()
nlp = spacy.load("en_core_web_md")

#loading the response and tags dictionaries
td = pp.tags_dict
rd = pp.resp_dict

def __fallback__(dict_sim):
    ''' To handle gen , spe , tag type of questions '''
    #store the key with the maximum confidence
    max_key_1 = pp.maximum(dict_sim)
    #ierate through the dit_sim and generate a new dictionary
    temp = {}
    ctr = 0 #ctr for the temporary dictionary 
    for i in dict_sim.values():
        ctr += 1 
        #if the value of i is less than dict_sim[max_key_1] place it in the temp dictionary
        if i < dict_sim[max_key_1]:
            temp[ctr] = i
    #key of the 2nd highest confidence value is stored here
    max_key_2 = pp.maximum(temp)
    #creating another temp dictionary
    temp_1 = {}
    ctr_1 = 0 #ctr for the temp_1 dict    
    for j in temp.values():
        ctr_1 += 1
        if j < temp[max_key_2] :
            temp_1[ctr] = j
    #storing the key of the 3rd highest confidence value  
    max_key_3 = pp.maximum(temp_1)  
    list_of_keys = [max_key_1 , max_key_2 , max_key_3]
    #mapping the keys in the list 
    res_list_fallback = []
    for i in list_of_keys:
        if dict_sim[i] >= 0.50: 
            res_list_fallback.append(td[i])
    return res_list_fallback

def fallback_driver(chk , sim_dict):
    ''' This is the driver function for the fallback mechanism '''
    if chk == True:
        fallback_resp_list = __fallback__(sim_dict)
        count = len(fallback_resp_list)
        fallback_resultant_str = " "
        temp_list = []
        temp_list.append("Bot : Did you mean")  
        for k in range(count):
            temp_list.append(fallback_resp_list[k])
            if k < count-1:
                temp_list.append("or")
        print(fallback_resultant_str.join(temp_list))  

        if len(fallback_resp_list) == 1:
            #taking the input from the user
            user_input_check_yes = input("You : ")
            #converting the input to lowercase 
            user_input_check_yes_lowercase = pp.tolower_(user_input_check_yes)
            if user_input_check_yes_lowercase == "yes":
            #display the response of the corresponding tag
                for j in fallback_resp_list:
                    if j != None:
                        #printing the response 
                        print("Bot : " , rd[j])
                        m.Interact(True)
                        
        else :
            #the response from the fallback mechanism is not a single value
            f_usr_inp = input("You :")
            #check if the request from the user is to quit 
            if pp.tolower_(f_usr_inp) == "bye":
                m.__driver__()
            else :
                #pre_processing the updated request from the user and then generating the response
                res1 = pp.pre_process(True , f_usr_inp)
                #calling the similarity function 
                sim_dict = pp._similarity(res1 , pp.tags_dict)
                #displaying the response for the fallback
                result_fallback_key = pp.maximum(sim_dict)
                #mapping the key to the response dictionary
                res_str = pp.response_(result_fallback_key , pp.resp_dict)
                print("Bot : " , res_str)
                m.Interact(True)
    else : 
        chk = False
        exit()