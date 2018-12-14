dic = {1:'a', 2:'b', 3:'c'}
dic2 = {}
for key, value in dic.items():
    dic2[key+2]=value
print(dic2)
print(dic)
