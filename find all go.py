#!/usr/bin/env python
# coding: utf-8

import re
import os
WORK_DIR="...\omics"

#findsamego function could find all go terms for the same geneid
def findsamego(list_ori):
    sublist=[]
    golist_ori=[]
    sublist.append(list_ori[0])
    num=list_ori[0].find('\t')
    target=list_ori[0][:num]
    row_num=1
    for i in list_ori[1:]:
        number1=i.find('\t')
        geneid=i[:number1]
        if geneid == target:
            sublist.append(i)
            row_num+=1
        else:
            break
    for i in sublist:
        mid=i[-11:-1]
        golist_ori.append(mid)
    return golist_ori, row_num,target

#subselect function could select module that has target goid
def subselect(goid,alt_id,database):
    subplace=[]
    row_number=0
    if goid in database:
        row_number=database.index(goid)
    else:
        for i in database:
            if i == alt_id:
                row_number=database.index(alt_id)
            else:
                continue
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

#sub_genelist function is to select the other part after finding the all go for the same proteinid 
def sub_genelist(genelist,n):
    return genelist[n:]

#creat the dataset of genelist
path_genelist=os.path.join(WORK_DIR,'1.txt')#set the path
with open(path_genelist,'r') as f:
    genelist=[]
    for i in f:
        genelist.append(i)
f.close()
genelist=genelist[1:]

#creat the dataset of godatabase file
path_godatabase=os.path.join(WORK_DIR,'godatabase.txt')
with open(path_godatabase,'r') as f:
    godatabasefile=[]
    for i in f:
        godatabasefile.append(i)
f.close()

for i in range(len(godatabasefile)):
    godatabasefile[i]=godatabasefile[i].replace("\n","")

#output the result to a txt tile
f = open('output.txt', 'a+')
for i in genelist:
    golist_ori,num,geneid=findsamego(genelist)
    f.write(geneid)
    f.write(":")
    for i in golist_ori:
        ori_go="id:"
        alt_go="alt_id:"+" "+i
        ori_go=ori_go+" "+i
        sub=subselect(ori_go,alt_go,godatabasefile)
        final=findrelgo(sub,golist_ori)
    for j in final:
        f.write(j)
        f.write(" ")
    f.write("\n")   
    genelist=sub_genelist(genelist,num)
f.close()    

#output the result
f = open('output.txt', 'a+')
for i in result:
    f.write(str(i))
    f.write("\n")
f.close()


