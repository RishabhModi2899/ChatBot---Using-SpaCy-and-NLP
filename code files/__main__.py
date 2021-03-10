#contains the driver code of the CHATBOT

#imports 
import ap_book as ab
import answer as ans
import pre_process as pp

def appoint(chk):
    ''' This function contains the driver code for appointment booking '''
    ''' chk is a boolean variable '''
    #fetching the list of details from the user
    user_details = ab.appointment(True)
    #making the connection to the database 
    con_obj = ab.database_connection()
    #creating the table in the database
    ab.table_create(con_obj)
    #making an entry in the table of appointments database 
    ab.table_entry(con_obj , user_details)
    print("Bot : Done! We will be in touch with you soon.")
    __driver__()

def Interact(chk):
    ''' This function gets called when the user wishes to interact with the chatbot '''    
    while chk: 
        user_input = input("You :")
        #calling the answer_ function that will pre process the input and generate the response 
        if pp.tolower_(user_input) == 'bye':
            chk = False
            print("Bot : Thanks for visiting . Goodbye")
            __driver__()
        else :
            chk = True
            ans.answer_(user_input)

def __driver__():
    ''' This is a function that contains the various options of the chatbot '''
    print("Menu : ")
    print("1 : Interact with the Bot")
    print("2 : Book an appointment")
    print("3 : exit")
    usr_chc = input("You : Please enter your choice (1 or 2 or 3).")

    if usr_chc == "1":
        #the interact function is called
        print("Bot : Hi , How can I help you?")
        print("Bot : Just type bye to exit")
        Interact(True)

    elif usr_chc == '2':
        #the appoint function is called 
        appoint(True)

    elif usr_chc == '3':
        #exit 
        exit()

    else :
        #default case 
        print("Bot : Please enter a valid choice (1 or 2 or 3). Thanks!")
        __driver__()

#calling the driver 
__driver__()

