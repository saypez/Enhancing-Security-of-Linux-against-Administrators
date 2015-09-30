from pwd import * 
from subprocess import *
from random import *
from crypt import *
from IPython.zmq.completer import readline
from spyderlib.utils.encoding import readlines
from simplepam import authenticate
import os
import getpass

#===================================( Class for Colors )======================================
class colors:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#========================================( Title )============================================
#this function is used to show a title for each task

def title(title_text="", color = colors.GREEN):
    window_size = check_output(["stty","size"]) # check the size of the terminal window
    window_size_list = window_size.split()
    width = int(window_size_list[1])
    print ""
    print (width-1)*"="
    print "|", colors.BOLD +  color  + title_text.center(width-4) + colors.END ,"|"
    print (width-1)*"="
    print ""

#=====================================( Adding a New User )=====================================
#this function is used for adding a new user and setting initial configurations

def useradd():
    
    login_name = raw_input(" Input the login name for this new user or write 'c' to cancel: ")  
    if login_name.upper()!= "C":
        user_home_directory = raw_input(" Specify any special home directory or press Enter to use default home directory defined in /etc/skel: ")
        user_shell = raw_input(" Specify any special shell for this user or press Enter to use the default /bin/bash: ")   
        
        if user_home_directory != "":
            special_home_directory = " -d " + user_home_directory
        else:
            user_home_directory = "/home/"+login_name 
            special_home_directory = " -d /home/"+login_name
 
        if user_shell != "":
            special_user_shell = " -s " + user_shell
        else: special_user_shell = ""      
    
        full_command = "useradd "+ login_name + special_home_directory + special_user_shell   
        list_of_arguments = full_command.split(" ")
        print ""
        adding_user = call(list_of_arguments)
   
        if adding_user == 0: 
            print "\nuser "+ login_name + " was created"
            random_passwd = str(randint(10000000,99999999))
            alphabet = "1234567890abcdefghijklmnopqrstuvwxyz"
            salt = choice(alphabet)+choice(alphabet)
            shadow_passwd = crypt(random_passwd, salt)
            set_pass = call(['usermod', '-p', shadow_passwd, login_name ])

            if set_pass == 0:
                print "The passwd " + random_passwd + " is set to <" + login_name + "> username\n"
                call(['chage', '-d', '0', login_name]) #makes user to change his password at the first login
                first_login = user_home_directory+"/.not_logged_in_yet"
                call(['touch', first_login])
                call(['chown',login_name+":"+login_name ,first_login]) 
                call(['chmod', 'u+rw', first_login])
            else:
                print colors.BOLD + " some problem with adding password" + colors.END
        else:
            print colors.BOLD + " some problem with adding user ..." + colors.END 
            print ""
    else:   print""
#=====================================( Lock a User )=========================================
#this function is used for locking an account 

def lock_user():
    username = raw_input(" Input the account that you want to lock or write 'c' to cancel: ")
    if username.upper()!= "C":
        if username in [x[0] for x in getpwall()]: #check if the username is exist
            locking_account = call(['passwd','-l', username])
        else:
            print colors.BOLD + " the username <%s> is not exist." %username + colors.END      
        
#=====================================( Unlock a User )=======================================
#this function is used for unlocking an account 

def unlock_user():
    username = raw_input(" Input the account that you want to unlock or write 'c' to cancel: ")
    if username.upper()!= "C":
        if username in [x[0] for x in getpwall()]: #check if the username is exist
            unlocking_account = call(['passwd','-u', username])
        else:
            print colors.BOLD + " the username <%s> is not exist." %username + colors.END 
                 
#================================( Forcing to Change Password )===============================
#this function is used to force user for changing his or her password

def force_changing_pass():
    username = raw_input(" Input the account that you want to change his or her password or write 'c' to cancel: ")
    if username.upper()!= "C":
        if username in [x[0] for x in getpwall()]: #check if the username is exist
            forcing_to_change_pass = call(['passwd','-e', username])
        else:
            print colors.BOLD + " the username <%s> is not exist." %username + colors.END 
             
#==================================( Adding a New Group )=====================================
#this function is used for adding a new group

def group_add():
    
    group_name = raw_input("Please specify the name of the new group or write 'c' for cancelation: ")
    if group_name.upper() != "C":
        leader_name = raw_input("Who is the leader of this group? please insert the username: ")
        print ""
        if leader_name in [x[0] for x in getpwall()]:  #this line uses pwd module and cheks whether the name of the leader is exist or not     
            adding_group = call(['groupadd',group_name])
            setting_leader = call(['gpasswd', '-A', leader_name, group_name])
            if adding_group == 0 and setting_leader == 0:
                print colors.BOLD + " Group <%s> was created and its leader is <%s>" %(group_name,leader_name) + colors.END
        else:
            print colors.BOLD + " the username <%s> is not exist, the group was not created." %leader_name + colors.END                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

#======================================( Delete a Group )====================================
#this function is used to force user for changing his or her password

def group_del():
    group_name = raw_input(" Input the name of the group you want to delete or write 'c' to cancel: ")
    if group_name.upper()!= "C":
        delete_group = call(['groupdel', group_name]) 
        if delete_group == 0:
            print colors.BOLD + " The <%s> group was deleted successfully" %group_name+ colors.END           

#========================================( Backup )============================================
#this function is used for making backup of user's data
def backup():
    
    username = raw_input(" Insert a username to make backup from his/her data or press c for cancellation: ")
    if username.upper() != "C":
        if username in [x[0] for x in getpwall()]: #check if the username is exist
            backup_place = raw_input(" Insert the location directory for storing the backup file: ")
            if backup_place == "":
                backup_place = "/tmp"
            if os.path.isdir(backup_place): # check if backup pace is exist in the system or not
                date = check_output(["date","+%F"])
                date=date[:10]
                file_name = username+"-"+date+".tar.gz"
                backup = call(["tar", "-c","-v","-z","-f",file_name, "/home/"+username])
                change_owner = call(["chown", username+":"+username , file_name])    
                move_backup = call(["mv","-f", file_name, backup_place])      
                if backup == 0 and change_owner == 0 and move_backup == 0:
                    print colors.BOLD + " The backup file of %s user was stored on %s" %(username,backup_place)+ colors.END
            else:
                print colors.BOLD + " The <%s> directory is not exist in the system" %backup_place+ colors.END    
        else: 
            print colors.BOLD + " the username <%s> is not exist." %username + colors.END                                                                   
    print ""
    
#===================================( Restricted Command )======================================
#this function is used for filtering some options of commands and runnig command with safe options

def restricted_command():
    full_command = raw_input("insert your command or press c for cancellation: ")
    if full_command.upper() != "C" and len(full_command) != 0:
        full_command_list = full_command.split()
        checker = True
        policy_file = open("commands.txt", "r")
        for line in policy_file:
            list_line = line.split()
        
            if full_command_list[0] == list_line[0]:
                checker = False
                common_argumant = set(full_command_list) & set(list_line)
                        
                if len(common_argumant) > 1:
                    print "your command have this set of option(s) which is not allowed to be used with the <%s> command" % full_command_list[0]
                    common_argumant.remove(full_command_list[0])
                    for item in common_argumant:
                        print colors.BOLD+ item + colors.END
                else :
                    call(full_command_list)
        if checker == True:
            print ""
            print colors.BOLD+"<%s> command is not included in restricted commands policy "%full_command_list[0]+colors.END
        policy_file.close()
        
#===================================( Showing Restricted Command )=============================
#this function is used for showing restricted commands and those options which are not allowed to be used.
def show_commands():
    
    commands_file = open("commands.txt" , "r")
    commands_list = commands_file.readlines()
    commands_list.sort()
    i = 0
    for item in commands_list:
        commands_list[i] = commands_list[i][:len(commands_list[i])-1] #removeing "/n" character from end of each line
        commands_list[i] = commands_list[i].split(" ")
        i += 1
    commands_file.close()       
    
    print 70*"_" 
    print "|",colors.BOLD+'{:^1}'.format('#')+ colors.END,"|",colors.BOLD+'{:^12}'.format('command')+ colors.END,"|",colors.BOLD+'{:^48}'.format('Not allowed options')+ colors.END,"|" 
    print 70*"=" 
    
    i = 0
    line_counter = 1
    for line in commands_list:
        print "|",'{:^1}'.format(line_counter),"|",'{:^12}'.format(commands_list[i][0]),"|",'{:^48}'.format(" ".join(commands_list[i][1:])),"|"
        print 70*"_"        
        i += 1
        line_counter += 1
    
    print "" 

#================================( Slicing file to a List )======================================
#this function read all the lines of the file and seperate it by ";" deliminator
def file_to_list():
    check_file = open("check_file.txt" , "r")
    check_file_list = check_file.readlines()
    i = 0
    for item in check_file_list:
        check_file_list[i] = check_file_list[i][:len(check_file_list[i])-1] #removeing "/n" character from end of each line
        check_file_list[i] = check_file_list[i].split(";")
        i += 1
    check_file.close()
    return check_file_list
#=========================================( joining List )=======================================
#this function is used to joun seperated list

def joining_list(list):
    i = 0
    for item in list:
        list[i] = ";".join(list[i])
        list[i] = str(list[i]) + "\n"
        i += 1
    return list 
#===========================================( List to File)=====================================
#This function is used to write existing list to the file (check_file.txt)
def list_to_file(List):
    check_file = open("check_file.txt", "w")
    for line in List:
        check_file.write(line)
    check_file.close()

#========================================( Ask a Request )=====================================     
#this functin is used to ask for running a task
def request_for_running():
    command = raw_input("Please insert the full command or press c for cancelation: ") 
    if command.upper() != "C" and len(command)!= 0 and command != " ":
        admin_name = raw_input("username: ")
        password = getpass.getpass("password: ")  
        print ""
        admin_permission = ""
        running_checker = "Not Yet"
        real_user = authenticate(admin_name, password)
        if real_user == True:
            requst_command = command + ";" + admin_name + ";" + admin_permission + ";"+ running_checker +  "\n" 
            check_file = open("check_file.txt", "a")
            check_file.write(requst_command)
            check_file.close()
            print colors.BOLD + "your request was successfully recorded, ask other administrators to accept it" + colors.END
        else:
            print colors.BOLD+"Authentication failed"+ colors.END
        
#=======================================( Show Request Table )================================
#this function is used to represent the present list in a table

def show_list(list):       
    print 90*"_"
    print '{:^0}'.format(''),"|",'{:^2}'.format('#'),"|",'{:^30}'.format('Requests'),"|",'{:^15}'.format('Requester'),"|" ,'{:^15}'.format('Checker'),"|",'{:^12}'.format('implemented'),"|"
    print 90*"="
    i = 0
    line_counter = 1
    for line in list:
        print '{:^0}'.format(''),"|",'{:^2}'.format(line_counter),"|",'{:^30}'.format(line[0]),"|",'{:^15}'.format(line[1]),"|" ,'{:^15}'.format(line[2]),"|",'{:^12}'.format(line[3]),"|"
        print 90*"_"        
        i += 1
        line_counter += 1
    print ""   
        
#=========================================( Accepting a Request )===============================
#this function is used to accept or deny any requested command for running
    
def accept_the_request():
    file_list = file_to_list()
    show_list(file_list)
    try:
        selected_command = input("please select which one do you want to approve or deny or 0 for cancelation: ")
        if selected_command != 0: 
            if file_list[selected_command-1][3] != "Yes": #if it is not already done
                admin_name = raw_input("username: ")
                password = getpass.getpass("password: ")  
                real_user = authenticate(admin_name, password)   
                if real_user == True:  #if the authentication was successful
                    select_accept_deny = raw_input("Press a to Accept, d to Deny and c to cancel confirming this request: ")
                    if select_accept_deny.upper() != "C" and len(select_accept_deny)!= 0:
                        if select_accept_deny.upper() == "A":
                            if admin_name != file_list[selected_command-1][1]:  #if the person does not want to accept his own request
                                file_list[selected_command-1][2] = admin_name
                            else:
                                print colors.BOLD+" You cannot accept your own request!"+colors.END 
                        if select_accept_deny.upper() == "D":
                            file_list[selected_command-1][3] = "Denied"
                            file_list[selected_command-1][2] = admin_name                          
                else:
                    print colors.BOLD+"Authentication failed"+ colors.END
            else:
                print colors.BOLD+" This request has been implemented successfully!"+colors.END                         
        joining_list(file_list)
        list_to_file(file_list)
        print ""
                        
    except:
        print""
        print colors.BOLD+" You must insert a number"+ colors.END
    
 #===================================( Running Accepted request )=============================
def run_accepted_request():
    file_list = file_to_list()
    show_list(file_list)
    try:
        selected_command = input("please select one one of your request for running or select or 0 for cancelation: ")
        if selected_command != 0:
            admin_name = raw_input("username: ")
            password = getpass.getpass("password: ")
            real_user = authenticate(admin_name, password)   
            if real_user == True:  #if the authentication was successful
                if file_list[selected_command-1][1] == admin_name:
                    if file_list[selected_command-1][3] != "Denied" and file_list[selected_command-1][2] != "":
                        if file_list[selected_command-1][3] != "Yes": #if it is not already done
                            accepted_request = file_list[selected_command-1][0].split(" ")
                            running_accepted_request = call(accepted_request)
                            if running_accepted_request == 0:
                                file_list[selected_command-1][3] = "Yes"
                            else:
                                file_list[selected_command-1][3] = "Problem"  
                        else:
                            print colors.BOLD+" This request is already successfully done!"+colors.END
                    else:
                        print colors.BOLD+"Your request is not accepted!"+ colors.END                                          
                else:
                    print colors.BOLD+"This is not your reuest!"+ colors.END
            else:
                    print colors.BOLD+"Authentication failed"+ colors.END
                  
        joining_list(file_list)
        list_to_file(file_list)
        print ""               
    except:
        print""
        print colors.BOLD+" You must insert a number"+ colors.END
 
 #================================( Main )================================================
command = ""
while command.upper() != "Q":
    call(['clear'])
    title("Linux ADMINS' USER INTERFACE", colors.RED)
    print " a) Managing accounts and groups"
    print " b) Managing users' resources"
    print " c) Running restricted commands "
    print " d) Special request"
    print " q) Quit"
    print ""
    command = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)      # command  asks user to input what he wants to do 
    print ""
    
    if command.upper() == "A":                                      # if user selected Managing account
        input_command = ""
        while input_command.upper() != "Q":
            title("Managing Accounts and Group", colors.GREEN)
            print " a) Managing Accounts"
            print " b) Managing Groups"
            print " q) Quit"
            print " "
            input_command = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
            print ""
            if input_command.upper() == "A":
                select = ""
                while select.upper() != "Q":
                    title("Managing Accounts", colors.GREEN)
                    print " a) Adding a new user account"
                    print " b) Lock an account"
                    print " c) Unlock an account"
                    print " d) Force user for changing password (Expire the password)"
                    print " q) Quit"
                    print " "
                    select = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
                    print ""
                    if select.upper() == "A":
                        useradd()
                    if select.upper() == "B":
                        lock_user()
                    if select.upper() == "C":
                        unlock_user()
                    if select.upper() == "D":
                        force_changing_pass()
            
            elif input_command.upper() == "B":
                select = ""
                while select.upper() != "Q":
                    title("Managing groups", colors.GREEN)
                    print " a) Creating a new group"
                    print " b) Delete a group"
                    print " q) Quit"
                    print " "
                    select = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
                    print ""
                    if select.upper() == "A":
                        group_add()
                    if select.upper() == "B":
                        group_del()
                
    elif command.upper() == "B": #if user selected making backup
        input_command = ""
        while input_command.upper() != "Q":
            title("Managing Users' Resources", colors.GREEN)
            print " a) Making backup from a users'data"
            print " q) Quit"
            print " "
            input_command = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
            print ""
            if input_command.upper() == "A":
                backup()                                         
        
    elif command.upper() == "C":                                    #if use selected running restricted commands
        input_command = " "
        while input_command.upper() != "Q":
            title("Running Restricted Commands", colors.GREEN)
            print " a) Show existing commands and their not allowd options"
            print " b) running a command"
            print " q) Quit"
            print ""
            input_command = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
            print ""
            if input_command.upper() == "A":
                show_commands()
            elif input_command.upper() == "B":
                restricted_command()
         
    elif command.upper() == "D":                                    #if use selected special request
        input_command = ""
        while input_command.upper() != "Q":
            title("Special Request", colors.GREEN)
            print " a) Ask a request"
            print " b) View the list of requests"
            print " c) Accept or deny a request"
            print " d) Running accepted request"
            print " q) Quit"
            print ""
            input_command = raw_input(colors.BOLD + colors.DARKCYAN + " Please select one option: " + colors.END)
            print ""
            if input_command.upper() == "A":
                request_for_running()
            elif input_command.upper() == "B":
                show_list(file_to_list())
            elif input_command.upper() == "C":
                accept_the_request()
            elif input_command.upper() == "D":
                run_accepted_request()
                
         
