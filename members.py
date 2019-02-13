import tj,pickle,sys,os


FILE='data.ppme'
KEY1='6JATGN2YC9PPCSEKB4'     # To encrypt the FILE
KEY2='H71OV1R8BFAZK240PP'     # To encrypt master_password



class Members:
    def __init__(self):
        self.name=self.__get_name()
        self.username=self.__get_username()
        self.email=self.__get_email()
        self.show_master_password='' # For showing password to the user, in a safe form
        self.master_password_enc=self.__get_password()  # Encrypted form of the password using KEY2
        self.data={}    # {website:[password,notes]}    this password will be encrypted using the master_password 
        self.__module__='PPM'

    @staticmethod
    def username_in_FILE(username):
        tj.decryptFile(FILE, password=KEY1)
        f=open(FILE, 'rb')
        All_Users=pickle.load(f)
        f.close()
        tj.encryptFile(FILE, password=KEY1)
        print(f'User_in_FILE method-> {All_Users}')

        for member in All_Users:
            if member.username==username:
                return True
        return False


    @staticmethod
    def sendConfirmationEmail(email,username,subject ):
        code=tj.getRandomString(L=[str(i) for i in range(10)], number=6)
        tar='images'
        html_resources=[os.path.join(tar,i) for i in os.listdir(tar)]
        f=open('template.html')
        body=f.read()
        f.close()
        body=body.format(username=username, confirmation=code)
        
        
        sender='tusharlock10@gmail.com'
        sender_pass='jjmcnukthkrncsii'
        reciever=[email]
        tj.email(sender, sender_pass, reciever, body, subject, email_type='html', html_resources=html_resources)

        isConfirmed=False
        
        for i in range(4,0,-1):
            os.system('cls')
            if i!=4:print(f'\nYou have {i+1} chances left...')
            code_user=input('Enter the code: ')
            if code_user==code:
                isConfirmed=True
                break
            print('The code you entered is incorrect, try again...\n\n')

        return isConfirmed 


    
    def __get_email(self):
        print('\n\tEnter your email address,\n\twe will send a confirmation code\n\tto confirm it...')
        email=input('\nEnter email address here: ')
        subject='PICO PASS, email verification code...'
        isConfirmed=self.sendConfirmationEmail(email,self.username,subject)
        if isConfirmed:return email
        else:
            print('Your email could not be confirmed...')
            print('Program will now quit')
            sys.exit()

        
            

    def __get_name(self):
        msg='Enter your name: '
        run=True
        while run:
            run=False
            name=input(msg)
            name=name.split(' ')

            for word in name:   
                if not word.isalpha():
                    run=True
                    msg='Your name should only contain letters: '

            name = " ".join([i.capitalize() for i in name])      # To capitalize the first letter of every word of the name
            
        return name

    def __get_password(self):
        global KEY2
        msg='Set a master password for your account (password will not be shown when you type): '
        run=True
        while run:
            run=False
            mp=tj.pinput(msg)       # mp is master_password of the user

            if not 7<len(mp)<25:
                msg='Password should be between 8 to 24 characters: '
                run=True
                continue

            if mp.isalpha():
                msg='Password should atleast contain a number or a special character: '
                run=True
                continue

            cmp=tj.pinput('Enter password again to confirm: ')
            if mp!=cmp:
                msg='Passowrds do not match: '
                run=True
                continue
        
        show_mp = mp[:1]+(len(mp[1:-1])*"*")+mp[-1:]
        mpe=tj.encrypt(mp,KEY2)     # master_password is now encrypted here
        self.show_master_password=show_mp
        print(f'\nThe password that you have set is: {show_mp}')
        del show_mp,mp
        
        return mpe

    def __get_username(self):
        msg='Enter username: '
        run=True
        while run:
            run=False
            username=input(msg)
            
            if not username.isalnum():
                msg='Username should contain only alphabets and numbers: '
                run=True
                continue

            if not username[0].isalpha():
                msg='Username should start from an alphabet: '
                run=True
                continue

            if self.username_in_FILE(username):
                msg='Username already in use, use another username: '
                run=True
                continue
        
        return username


    def enter_new_data(self):
        global KEY2
        website=input('Enter the website: ')

        msg='Enter the password for this website: '
        run=True
        while run:
            run=False
            password=tj.pinput(msg)
            cpassword=tj.pinput('Enter the conformation for this password: ')

            if password!=cpassword:
                msg= '\nPasswords do not match, enter again: '
                run=True
        p=password
        show_password=p[0]+len(p[1:])*'*'
        notes=input('Enter any short notes with it, if any: ')
        print(f'''\n\nThis is the data you entered-
Website: {website}
Password: {show_password}
Notes: {notes}\n\n''')
        mp=tj.decrypt(self.master_password_enc, KEY2)   # Obtain mp from the mpe using KEY2
        website=tj.encrypt(website, mp)
        password=tj.encrypt(password,mp)
        notes=tj.encrypt(notes, mp)
        del mp
        temp={website:[password, notes]}
        print(f'encrypted-> {temp}')
        self.data.update(temp)


    def show_data(self):
        global KEY2
        master_password_check=tj.pinput(f'Enter the master password for {self.username}: ')
        mp=tj.decrypt(self.master_password_enc,KEY2)    # Obtain mp from the mpe using KEY2
        if master_password_check!=mp:
            print(f'\nWrong password for {self.username}...\n')
            del mp
            return
        print(f'\n\nName: {self.name}\nUsername: {self.username}\n')
        print('------+------------------+------------------+'+('-'*60)+'+')
        print(' Sno. |      Website     |     Password     |                            Notes                           |')
        print('------+------------------+------------------+'+('-'*60)+'+')
        keys=list(self.data.keys())
        for i in range(len(keys)):
            key=keys[i]     # key is website's encrypted form
            data=self.data[key]

            website=tj.decrypt(key,mp) 
            password=tj.decrypt(data[0],mp)
            notes=tj.decrypt(data[1],mp)
            print(' %-5s| %-17s| %-17s| %-59s|' % (i+1, website, password, notes))
            del website, password, notes, key
        print('------+------------------+------------------+'+('-'*60)+'+')


    def change_name(self):
        global KEY2
        cmp=input('Enter your master password: ')
        mp=tj.decrypt(self.master_password_enc,KEY2)
        if cmp!=mp:
            print('Wrong password...')
            return
        del mp
        self.name=self.__get_name()


    def change_password(self, forgot=False):
        global KEY2

        if not forgot:
            cmp=input('Enter your current master password: ')
            mp=tj.decrypt(self.master_password_enc,KEY2)
            if cmp!=mp:
                print('Wrong password....')
                return
        else:
            mp=tj.decrypt(self.master_password_enc,KEY2)
            
        
        mpe_new=self.__get_password()
        self.master_password_enc=mpe_new
        mp_new=tj.decrypt(mpe_new,KEY2)
        data_new={}
        
        for key in self.data:
            data=self.data[key]
            website=tj.decrypt(key, mp)
            password=tj.decrypt(data[0], mp)
            notes=tj.decrypt(data[1], mp)
            
            website=tj.encrypt(website, mp_new)
            password=tj.encrypt(password, mp_new)
            notes=tj.encrypt(notes, mp_new)    
            temp={website: [password, notes]}
            
            data_new.update(temp)
        self.data=data_new
        
        del mp, mp_new, temp

            
    def change_email(self):
        cmp=input('Enter the master password: ')
        if cmp==tj.decrypt(self.master_password_enc, KEY2):
            self.email=self.__get_email()
        else:
            print('Password is incorrect, no change done...')

    def forgot_password(self):
        subject='PICO PASS, master password forgot confirmation code...'
        isConfirmed=self.sendConfirmationEmail(self.email, self.email, subject)

        if isConfirmed:
            self.change_password(forgot=True)
        else:
            print("You couldn't confirm your password forgot request...")
        
                  

    def __str__(self):
        to_print=f'''\n---------------------------------------\n
Name: {self.name}
Username: {self.username}
Password: {self.show_master_password}
Email: {self.email}\t(verified)\n---------------------------------------\n'''
        return to_print
