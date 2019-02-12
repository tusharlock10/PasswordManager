import tj,pickle,sys
from members import Members
from members import *


try :
    f=open(FILE,'rb')
    All_Users=pickle.load(f)    # [mem_obj1, mem_obj2, mem_obj3...]
    f.close()
except:
    All_Users=[]
    f=open(FILE,'wb')
    pickle.dump(All_Users,f)
    f.close()



def showUserData(All_Users):
    username=input('Enter your username: ')
    for member in All_Users:
        if member.username==username:
            member.show_data()
            return None
    input('No such user found...')


def saveData(All_Users):
    global FILE
    f=open(FILE,'wb')
    pickle.dump(All_Users,f)
    f.close()

def makeNewMember(All_Users):
    global FILE
    print(All_Users)
    M=Members()
    print(M)
    All_Users+=[M]
    saveData(All_Users)
    

def enterNewData(All_Users):
    username=input('Enter your username: ')
    mp=tj.pinput(f'Enter the master password {username}: ')
    mp=tj.make_hash(mp)
    
    for member in All_Users:
        if member.username==username:
            All_Users.remove(member)
            member.enter_new_data()
            All_Users+=[member]
            saveData(All_Users)
    

menu='''
MENU for password manager:
1) Register a new member
2) See your data
3) Enter new data
4) To quit'''
print(menu)

while True:
    choice=input('\n\n\nEnter your choice: ')
    if choice=='1':
        makeNewMember(All_Users)

    if choice=='2':
        showUserData(All_Users)

    if choice=='3':
        enterNewData(All_Users)

    if choice.upper() in ['4','Q']:
        sys.exit()

        

        
        
