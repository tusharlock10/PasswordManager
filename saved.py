import tj
import sys
import os, pickle, pyperclip
from cryptography.fernet import Fernet
import msvcrt as m



secreteKey1='YOKCCRDNS6QH13JXKK4Y8DXI'  # used to encrypt the whole file
secreteKey2='CGC1ZXKBSFAY73QMIACRH7FX'  # used to encrypt the userdata
save_file='data.pcp'

class Member:
    def __init__(self, All_members):
        self.name = 'Tushar Jain'#input('Enter your name: ')
        self.username = 'tusharlock10'#self.__getUsername(All_members)
        self.master_password= 'tushar123'#self.__getPassword()
        self.email=self.__getEmail()
        self.data={}    # Dictionary of type {website:[username, pass, notes]}
        

    def __getUsername(self, All_members):
        msg = 'Enter a username: '
        while True:
            new_username = input(msg)
            for members in All_members:
                username = members.username
                if new_username.upper() == username.upper():
                    msg = 'Username is already in use, enter a valid username: '
                    continue
            return new_username

    @staticmethod
    def __getPassword(flag=True):
        if flag==True:msg='Set a master password for your account: '
        else:msg=flag
        
        while True:
            p=tj.pinput(msg)
            if (not (6<len(p)<22)) and (flag==True) :
                msg='Enter password in between 6-22 characters: '
                continue
            if (p.isalnum()) and (flag==True):
                msg='Enter a special character like @/#/$/!/% in the password: '
                continue
            if not p==tj.pinput('Enter again to confirm: '):
                msg="Passwords don't match, try again: "
                continue
            return p

    def __getEmail(self):
        msg='Enter your email address: '
        reciever='tusharlock10@gmail.com'#input(msg) 
        print('\nWe are sending an email to your email address,')
        print('the email contains a confirmation code, kindly check it...\n')
        code=tj.getRandomString(L=[str(i) for i in range(10)], number=6)
        tar='images'
        html_resources=[os.path.join(tar,i) for i in os.listdir(tar)]
        username=self.username
        email='tusharlock10@gmail.com'
        email_pass='jjmcnukthkrncsii'
        f=open('template.html')
        body=f.read()
        f.close()
        subject='PICO PASS, confirmation email...'
        body=body.format(username=username, confirmation=code)
        
        tj.email(email, email_pass, [reciever], body, subject, email_type='html', html_resources=html_resources)

        isConfirmed=False

        for i in range(4,0,-1):
            os.system('cls')
            if i!=4:print(f'\nYou have {i+1} chances left...')
            code_user=input('Enter the code: ')
            if code_user==code:
                isConfirmed=True
                break
            print('The code you entered is incorrect, try again...\n\n')

        if not isConfirmed:
            input('You could verify your email, try registring again...')
            sys.exit()
        return reciever

    def save(self, All_members, secreteKey1, save_file):
        All_members+=[self]
        f=open(save_file,'wb')
        pickle.dump(All_members, f)
        All_members=[]
        del All_members
        f.close()
        tj.encryptFile(save_file, password=secreteKey1)
        secreteKey1="Don't even try, you can't get in!"
        del secreteKey1

    def NewEntry(self, secreteKey2):
        sk2=secreteKey2
        website=tj.encrypt(input('Enter the name of the website: '), sk2)
        username=tj.encrypt(input('Enter the username on that website: '), sk2)
        password=tj.encrypt(self.__getPassword('Enter the password of that website: '), sk2)
        notes=tj.encrypt(input('Enter any notes alongside if you want: '), sk2)
        temp={website:[username, password,notes]}
        self.data.update(temp)  # saving data in self.data
        temp, website, username, password, notes=['']*5
        del temp,website,username,password,notes

    def ShowAllEntries(self, secreteKey2):
        sk2=secreteKey2
        print('+------+-------------------+------------------+------------------+-----------+')
        print('| Sno. |      Website      |     Username     |     Password     |   Notes   |')
        print('+------+-------------------+------------------+------------------+-----------+')
        sno=0
        L=[]
        for key in list(self.data.keys()):
            website=key
            sno+=1
            L=self.data[website]
            website=tj.decrypt(website, sk2)
            username=tj.decrypt(L[0], sk2)
            p=tj.decrypt(L[1], sk2)
            L+=[p]
            password='*'*(len(p)-4)
            password=f'{p[:2]}{password}{p[-2:]}'
            notes=tj.decrypt(L[2], sk2)
            notes=f'{notes[:3]}...{notes[-3:]}'
            print("| %-4s | %-17s | %-16s | %-16s | %-9s |" % (str(sno), website, username, password, notes))
        print('+------+-------------------+------------------+------------------+-----------+')
        print('\n\nIf your want to know the pssword of a website, enter its Sno.\n')
        toKnow=int(input('Enter the Sno. of the password you want to know: '))
        p=L[toKnow-1]
        p=tj.decrypt(p, sk2)
        print('Password is:',p)
        del p,L
        
        
        
        

#-------------MAIN-----------------------

try:
    print(1)
    tj.decryptFile(save_file, secreteKey1)
    f=open(save_file,'rb')
except:
    f=open(save_file,'wb')
    pickle.dump([],f)
    f.close()
    f=open(save_file, 'rb')

All_members=pickle.load(f)
print(All_members)
f.close()

M=Member([])
M.NewEntry(secreteKey2)
M.save(All_members, secreteKey1, save_file)
M.ShowAllEntries(secreteKey2)

            

