import tj,pickle,sys,os
from members import Members
from members import *


try :
    tj.decryptFile(FILE, password=KEY1)
    f=open(FILE,'rb')
    All_Users=pickle.load(f)    # [mem_obj1, mem_obj2, mem_obj3...]
    f.close()
    tj.encryptFile(FILE, password=KEY1)
    
except:
    All_Users=[]
    f=open(FILE,'wb')
    pickle.dump(All_Users,f)
    f.close()
    tj.encryptFile(FILE, password=KEY1)



def showUserData(All_Users):
    username=input('Enter your username: ')
    for member in All_Users:
        if member.username==username:
            member.show_data()
            return None
    input('No such user found...')


def saveData(All_Users):
    global FILE
    tj.decryptFile(FILE, password=KEY1)
    f=open(FILE,'wb')
    pickle.dump(All_Users,f)
    f.close()
    tj.encryptFile(FILE, password=KEY1)

def makeNewMember(All_Users):
    global FILE
    print(All_Users)
    M=Members()
    print(M)
    All_Users+=[M]
    saveData(All_Users)
    

def enterNewData(All_Users):
    username=input('Enter your username: ')
    
    for member in All_Users:
        if member.username==username:
            cmp=tj.pinput(f'Enter the master password {username}: ')
            mp=tj.decrypt(member.master_password_enc,KEY2)
            if cmp!=mp:
                print(f'Wrong password for {username}\n')
                break
            All_Users.remove(member)
            member.enter_new_data()
            All_Users+=[member]
            saveData(All_Users)


def doChange(member):
    menu='''\n\n
1) Change Name
2) Change Password
3) Change Email
4) Delete Account
5) Forgot Master Password
6) Do Noting and Quit'''
    run=True
    msg='Enter your choice: '
    print(menu)
    while run:
        run=False
        choice = input(msg)
        if choice=='1':
            member.change_name()
            return [member]

        elif choice=='2':
            member.change_password()
            return [member]

        elif choice=='3':
            member.change_email()
            return [member]

        elif choice=='4':
            x=input('Enter DELETE to confirm deletion: ')
            if x.upper()=='DELETE':
                return []

        elif choice=='5':
            member.forgot_password()
            return [member]

        elif choice=='6':return [member]
        else:
            msg='\nChoice should be between 1-5: '
            run=True
    

def manageAccount(All_Users):
    username=input('Enter your username: ')

    for member in All_Users:
        if member.username==username:
            All_Users.remove(member)
            member_in_a_list=doChange(member)
            All_Users+=member_in_a_list
            saveData(All_Users)
                
    
    

menu='''
MENU for password manager:
1) Register a new member
2) See your data
3) Enter new data
4) Manage Account
5) To quit'''

while True:
    os.system('cls')
    print(menu)
    choice=input('\n\n\nEnter your choice: ')
    if choice=='1':
        makeNewMember(All_Users)

    if choice=='2':
        showUserData(All_Users)

    if choice=='3':
        enterNewData(All_Users)

    if choice=='4':
        manageAccount(All_Users)

    if choice.upper() in ['5','Q']:
        sys.exit()

    input('\n\nEnter to continue...')

        

        
        
