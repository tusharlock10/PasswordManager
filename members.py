import tj,pickle,sys
FILE='data.ppme'

class Members:
    def __init__(self):
        self.name=self.__get_name()
        self.username=self.__get_username()
        self.email=self.__get_email()
        self.master_password=self.__get_password()  # Hashed form of the password
        self.data={}    # {website:[password,notes]}
        self.show_master_password='' # For showing password to the user, in a safe form
        self.__module__='PPM'


    def username_in_FILE(self,username):
        f=open(FILE, 'rb')
        All_Users=pickle.load(f)
        f.close()
        print(f'User_in_FILE method-> {All_Users}')

        for member in All_Users:
            if member.username==username:
                return True
        return False

    def __get_email(self):
        email=input('Enter your email address: ')
        return email

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

            name = "".join([i.capitalize() for i in name])      # To capitalize the first letter of every word of the name
            
        return name

    def __get_password(self):
        msg='Set a master password for your account (your password will not be shown when you type): '
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
        
        show_mp = mp[:1]+(len(mp[1:-2])*"*")+mp[-2:]
        mp=tj.make_hash(mp)
        self.show_master_password=show_mp
        print(f'THis-> {self.show_master_password}, This2-> {show_mp}')
        print(f'\nThe password that you have set is: {show_mp}')
        return mp

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
        temp={website:[password, notes]}
        self.data.update(temp)


    def show_data(self):
        master_password_check=tj.pinput(f'Enter the master password for {self.username}: ')
        master_password_check=tj.make_hash(master_password_check)
        if master_password_check!=self.master_password:
            print(f'\nWrong password for {self.username}...\n')
            return
        print('------+------------------+------------------+'+('-'*30)+'+')
        print(' Sno. |      Website     |     Password     |    Notes                     |')
        print('------+------------------+------------------+'+('-'*30)+'+')
        keys=list(self.data.keys())
        for i in range(len(keys)):
            key=keys[i]     # key is website
            data=self.data[key]

            website=key
            password=data[0]
            notes=data[1]
            print(' %-5s| %-17s| %-17s| %-29s|' % (i+1, website, password, notes))
        print('------+------------------+------------------+'+('-'*30)+'+')
            


    def __str__(self):
        to_print=f'''\n---------------------------------------\n
Name: {self.name}
Username: {self.username}
Password: {self.show_master_password}
Email: {self.email}\t(verified)\n---------------------------------------\n'''
        return to_print
