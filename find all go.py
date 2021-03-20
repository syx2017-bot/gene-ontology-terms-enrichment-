#!/usr/bin/env python
# coding: utf-8

# In[23]:


import re

#findname function：find the row that has the same geneid with the fisrt row,and return to a list that contain same geneid
def findsame(list_ori):
    sublist=[]
    sublist.append(list_ori[0])
    num=list_ori[0].find('\t')
    target=list_ori[0][:num]
    for i in list_ori[1:]:
        number1=i.find('\t')
        geneid=i[:number1]
        if geneid == target:
            sublist.append(i)
        else:
            break
    return sublist

#gathergo function could find all go terms with the same geneid
def gathergo(sublist):
    golist_ori=[]
    for i in sublist:
        mid=i[-11:-1]
        golist_ori.append(mid)
    return golist_ori

#findsamego function could find all go terms for the same geneid
def findsamego(list_ori):
    sublist=[]
    golist_ori=[]
    sublist.append(list_ori[0])
    num=list_ori[0].find('\t')
    target=list_ori[0][:num]
    for i in list_ori[1:]:
        number1=i.find('\t')
        geneid=i[:number1]
        if geneid == target:
            sublist.append(i)
        else:
            break
    for i in sublist:
        mid=i[-11:-1]
        golist_ori.append(mid)
    return golist_ori
genelist=[]

#subselect function could select module that has target goid
def subselect(goid,database):
    subplace=[]
    row_number=database.index(goid)
    for i in range(row_number,len(database)):
        if database[i]!='':
            subplace.append(database[i])
        else:
            break
    return subplace        

#findrelgo function is to find the go terms that has relationship with the current terms
def findrelgo(sublist,targetlist):
    relationship=['is_a','part_of']
    for i in sublist:
        for j in relationship:
            if j in i:
                s=re.findall(r'GO:\d+',i)
                s=','.join(s)
                if s in targetlist:
                    continue
                else:
                    targetlist.append(s)
            else:
                continue
    return targetlist
with open('1.txt','r') as f:
    for i in f:
        genelist.append(i)
f.close()
genelist=genelist[1:]
with open('2.txt','r') as f:
    godatabasefile=[]
    for i in f:
        godatabasefile.append(i)
f.close()
for i in range(len(godatabasefile)):
    godatabasefile[i]=godatabasefile[i].replace("\n","")

test=findsamego(genelist)

for i in test:
    ori_go="id:"
    ori_go=ori_go+" "+i
    sub=subselect(ori_go,godatabasefile)
    final=findrelgo(sub,test)


# In[24]:


final


# In[12]:





# In[7]:





# In[ ]:




