import tj,pickle

FILE='data.ppme'


try:
    f=open(FILE,'rb')
    All_Users=pickle.load(f)
except:
    f=open(FILE,'wb')
    f.close()
    f=open(FILE,'rb')
    All_Users=[]

    # [mem_obj1, mem_obj2, mem_obj3...]
f.close()

print(All_Users)

