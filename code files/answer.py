#This is to generate a perticular type of response for that specific type of question
import nltk
import spacy
import __main__ as m
import fallback_mech_functions as fmf
import pre_process as pp
import ques_type as qt
import script_unhandled_req as sur

#load spacy dataset
spacy.prefer_gpu()
nlp = spacy.load("en_core_web_md")


def ans_gen(svo, user_input):
	''' This function will be the responsible to generate responses of general type questions '''
	#loading the tag directory
	td = pp.tags_dict
	#calling the similarity function
	similarity_dict = pp._similarity(svo, td)
	#fetching the key from the dictionary with the highest confidence
	max_key = pp.maximum(similarity_dict)
	#if max_key confidence value is >75 or not
	if similarity_dict[max_key] > 0.75:
		print("Bot : Yes!")
		print("Cofidence: ", similarity_dict[max_key])
	elif similarity_dict[max_key] >= 0.40 and similarity_dict[max_key] <= 0.75:
		#acitivate fallback mechanism
		fmf.fallback_driver(True, similarity_dict)
	else:
		#Note : else might change based on fallback mechanism
		print("Bot : No! Anything else I can help you with?")
		con_obj = sur.db_unhandled_requests()
		sur.gen_table_unhandled_requests(con_obj)
		sur.create_table_entry(con_obj , user_input , svo , "NULL")


def ans_spe(svo, user_input):
	''' This function will be the responsible to generate responses of special type questions '''
	#loading the tags as well as the response directory
	td = pp.tags_dict
	rd = pp.resp_dict
	#calling the similarity function
	similarity_dict = pp._similarity(svo, td)
	#fetching the key from the dictionary with the highest confidence
	max_key = pp.maximum(similarity_dict)
	#if max_key confidence value is >75 or not
	if similarity_dict[max_key] > 0.75:
		resp_str = pp.response_(max_key, rd)
		print("Bot : ", resp_str)
	elif similarity_dict[max_key] >= 0.40 and similarity_dict[max_key] <= 0.75:
		#acitivate fallback mechanism
		fmf.fallback_driver(True, similarity_dict)
	else:
		#Note : Else might change based on fallback mechanism
		print("Bot : Sorry ! Can't understand your question . Anything else I can help you with?")
		#Here the entry in database of unhandled request has to be made
		con_obj = sur.db_unhandled_requests()
		sur.gen_table_unhandled_requests(con_obj)
		sur.create_table_entry(con_obj , user_input , svo , "NULL")


def ans_chc(user_input):
	''' This function will be the responsible to generate responses of choice type questions '''
	#pre-processing the user input
	lc = pp.tolower_(user_input)
	rp = pp.removepunct_(lc)

    #clause to mark the end of the string
	user = []
	for g in rp:
	    user.append(g)
	user.append(" END")
	#converting this to string
	str_usr = "".join(user)

	#creating the NLP object
	user_nlp = nlp(str_usr)

	#creating a list of nlp type values
	usr = []
	for k in user_nlp:
		usr.append(k)

	#creating a list of indices where or has occured
	or_position_list = []
	count_or = 0
	for i in user_nlp:
		#Note : use tolower function here
		if i.text == "or":
			or_position_list.append(count_or)
			count_or += 1
		else:
			count_or += 1

	#checking for NOUN and PROPN type pos before and after or positions and creating a list to store the choices
	choices = []
	res_tmp_left = []
	res_tmp_right = []
	entry_ctr = 0
	for pos in or_position_list:
		i, j = 1, 1
		if entry_ctr < 1:
			while usr[pos - i].pos_ == "NOUN" or usr[pos - i].pos_ == "PROPN":
				res_tmp_left.append(usr[pos - i].text)
				i += 1

			#the choice on left is fetched it now needs to be entered in the choices list as a string
			chc = []  # temp list to store the choice in the correct reading order
			str_obj = ""
			for read in reversed(res_tmp_left):
				chc.append(read)
			#converting the chc list to string
			str_obj = " ".join(chc)
			#appending this string in the choices list
			choices.append(str_obj)

			while (usr[pos + j].pos_ == "NOUN" or usr[pos + j].pos_ == "PROPN") and (usr[pos + j].text != "END"):
				res_tmp_right.append(usr[pos + j].text)
				j += 1

			# appending the choices fetched to the choices list
			chc_right = []
			str_obj_1 = ""
			for read_choice in res_tmp_right:
				chc_right.append(read_choice)
			#converting this list into string type
			str_obj_1 = " ".join(chc_right)
			#appending this string in the choices list
			choices.append(str_obj_1)

			entry_ctr += 1

		else:
			tmp = []
			if entry_ctr >= 1:
				while (usr[pos + j].pos_ == "NOUN" or usr[pos + j].pos_ == "PROPN") and (usr[pos + j] != "END"):
					tmp.append(usr[pos + j].text)
					j += 1

				#appending the choice to the choices list
				chc_3 = []  # temp list
				str_obj_2 = ""
				for read_chc in tmp:
					chc_3.append(read_chc)
				#converting it to string form
				str_obj_2 = " ".join(chc_3)
				#appending this to choices
				choices.append(str_obj_2)

				entry_ctr += 1

	#clause to generate the responses of choice type questions
	# dictionary to store the (key = key with ax conf in tag dict and value = confidence)
	choices_conf_dict = {}
	for res in choices:
		#converting the res to nlp type
		res_nlp = nlp(res)
		#making the entry of the choice along with confidence value in the choices_conf_dict
		tmp_dict = pp._similarity(res_nlp, pp.tags_dict)
		#fetching the value with the maximum confidence value
		max_key = pp.maximum(tmp_dict)
		choices_conf_dict[max_key] = tmp_dict[max_key]

	#loop to generate responses to the request from the user
	list_of_max_keys = []
	f_ctr = 0
	for conf in choices_conf_dict.keys():
		if choices_conf_dict[conf] >= 0.75:
			list_of_max_keys.append(conf)
	length = len(list_of_max_keys)
	if length == 1:
		for reply in list_of_max_keys:
			print("Bot : We only provide ", pp.tags_dict[reply])
	elif length == 2:
		print("Bot : We peovide both!")
	else:
		if length >= 3:
			print("Bot : We provide all of the above!")
		else:
			if f_ctr < 1:
				print("Bot : Can you please ask that again.")
				f_ctr += 1
			else:
				print("Bot : Sorry! Can't answer that right now.")
				#entry to database of unhandled request is made
				con_obj = sur.db_unhandled_requests()
				sur.gen_table_unhandled_requests(con_obj)
				sur.create_table_entry(con_obj , user_input , "NULL" , "NULL")


def ans_tag(svo, user_input):
	''' This function will be the responsible to generate responses of tag type questions '''
	#loading the tag directory
	td = pp.tags_dict
	#calling the similarity function
	similarity_dict = pp._similarity(svo, td)
	#fetching the key from the dictionary with the highest confidence
	max_key = pp.maximum(similarity_dict)
	#if max_key confidence value is >75 or not
	if similarity_dict[max_key] > 0.75:
		print("Bot : Yes!")
	elif similarity_dict[max_key] >= 0.40 and similarity_dict[max_key] <= 0.75:
		#acitivate fallback mechanism
		fmf.fallback_driver(True, similarity_dict)
	else:
		print("Bot : No! Anything else I can help you with?")
		con_obj = sur.db_unhandled_requests()
		sur.gen_table_unhandled_requests(con_obj)
		sur.create_table_entry(con_obj , user_input , svo , "NULL")


def answer_(user_input):
	''' This is the function that will decide what type of response has to generated based on the grammer and the type of question '''

	#pre-process the user input and fetching the svo
	svo = pp.pre_process(True, user_input)

	#determine the type of question and remove words that are not requiered
	tmp_usr = []
	user_nlp = nlp(user_input)
	
	for j in user_nlp:
		tmp_usr.append(j)
	
	for i in user_nlp:
		if (i.pos_ == "INTJ" and i.text == "hi") or (i.pos_ == "INTJ" and i.text == "okay") or (i.pos_ == "PROPN" and i.text == "allright") or (i.pos_ == "ADJ" and i.text == "great") or (i.pos_ == "ADJ" and i.text == "good"):
			tmp_usr.remove(i)
	
	chk = qt.qtype_(tmp_usr)

	#Genrating the requiered type of response
	if chk == "GEN":
		#answer type is yes/no
		ans_gen(svo, user_input)
	elif chk == "SPE":
		#EG : What is on the table - glass .This is the requiered type of response!
		ans_spe(svo, user_input)
	elif chk == "CHC":
		#EG : Does she like icecream or peanuts - Icecream .This is kind of response that needs to be generated!
		ans_chc(user_input)
	elif chk == "TAG":
		#EG : Our dad will come soon , wont he - Yes he will! This is the kind of response that should be genrated!
		ans_tag(svo, user_input)
	else:
		#if the request can be handled by similarity if yes display the response and if not then make an entry in the database of unhandled requests
		if chk == None:
			sim_tmp = pp._similarity(svo, pp.tags_dict)
			#fetching the key with the maximum confidence
			key_max = pp.maximum(sim_tmp)
			if sim_tmp[key_max] >= 0.75:
				#Display the response
				resp_str = pp.response_(key_max, pp.resp_dict)
				print("Bot : ", resp_str)
			elif sim_tmp[key_max] >= 0.40 and sim_tmp[key_max] < 0.75:
				#Fallback Mechanism
				fmf.fallback_driver(True, sim_tmp)
			else:
				#request can't be handled and the request needs to be entered in the database of unhandled requests
				print("Bot : Sorry! Can't answer that right now. Please ask something else.")
				con_obj = sur.db_unhandled_requests()
				sur.gen_table_unhandled_requests(con_obj)
				sur.create_table_entry(con_obj , user_input , svo , "NULL")
				m.Interact(True)
