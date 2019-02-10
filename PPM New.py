import tj,pickle,sys


FILE='data.ppme'


try:
    f=open(FILE,'rb')
    All_Users=pickle.load(f)    # [mem_obj1, mem_obj2, mem_obj3...]
except:
    f=open(FILE,'wb')
    f.close()
    f=open(FILE,'rb')
    All_Users=[]

    
f.close()

class Members:
    def __init__(self):
        self.name=self.__get_name()
        self.username=self.__get_username()
        self.email=self.__get_email()
        self.master_password=self.__get_password()
        self.data={}    # {website:[password,notes]}

    def __get_email(self):
        email=input('Enter your email address: ')
        return email

    def __get_name(self):
        name=input('Enter your name: ')
        return name

    def __get_password(self):
        mp=tj.pinput('Set a password: ')
        return mp

    def __get_username(self):
        username=input('Enter username: ')
        return username

    def enter_new_data(self):
        website=input('Enter the website: ')
        password=tj.pinput('Enter the password for this website: ')
        notes=input('Enter any short notes with it, if any: ')
        temp={website:[password, notes]}
        self.data.update(temp)

    def show_data(self):
        master_password_check=input(f'Enter the master password for {self.username}: ')
        if master_password_check!=self.master_password:
            print('Wrong password...')
            return

        keys=list(self.data.keys())
        for key in keys:
            data=self.data[key]
            print(key,data)

            



def showUserData():
    global All_Users
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

def makeNewMember():
    global FILE, All_Users
    print(All_Users)
    M=Members()
    All_Users+=[M]
    saveData(All_Users)
    

def enterNewData():
    global All_Users
    All_Users_New=[]
    username=input('Enter your username: ')
    
    for member in All_Users:
        print(member.username,username)
        if member.username==username:
            print('NEW DATA ENTRY----')
            member.enter_new_data()
        All_Users_New+=[member]

    saveData(All_Users_New)
    

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
        makeNewMember()

    if choice=='2':
        showUserData()

    if choice=='3':
        enterNewData()

    if choice.upper() in ['4','Q']:
        sys.exit()

        

        
        
