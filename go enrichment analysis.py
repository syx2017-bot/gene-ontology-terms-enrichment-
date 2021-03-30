#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import re
import math

#your work path
WORK_DIR='E:\\组学重构'
#load the expression data file 
gene_expression_path=os.path.join(WORK_DIR,'gene_expression.csv')
gene_expression_read_file=pd.read_csv(gene_expression_path,engine='python')#when the path contain Chinese,engine='python'is needed
#load the go database file
godatabasefile_path=os.path.join(WORK_DIR,'2.txt')
with open(godatabasefile_path,'r') as f:
    godatabasefile=[]
    for i in f:
        godatabasefile.append(i)
f.close()
for i in range(len(godatabasefile)):
    godatabasefile[i]=godatabasefile[i].replace("\n","")

#remove blank GO terms as well as redundancy columns
def remove_redundancy_infor(gene_ex_file):
    target_label=['gene_id','p_value','GO']
    row_counter=0
    for i in gene_ex_file.GO:
        if i == "-":
            gene_ex_file=gene_ex_file.drop([row_counter])
            row_counter+=1
        else:
            row_counter+=1
    for i in gene_ex_file:
        if i not in target_label:
            gene_ex_file=gene_ex_file.drop(i,axis=1)
    gene_ex_file=gene_ex_file.dropna()# remove NaN
    gene_ex_file=gene_ex_file.reset_index(drop=True)#reconstruct the index
    return gene_ex_file

#select the differential expression gene according to the p_value
def diff_gene(gene_ex_file2):
    row_counterd=0
    for i in gene_ex_file2.p_value:
        if i<0.05:
            row_counterd+=1
        else:
            gene_ex_file2=gene_ex_file2.drop([row_counterd])
            row_counterd+=1
    gene_ex_file2=gene_ex_file2.reset_index(drop=True)
    return  gene_ex_file2

#extract the goterms from the differential expression gene
def find_ori_go(dif_ex_gene):
    diff_ex_list=[]
    for i in dif_ex_gene.GO:
        go_terms_diff=re.findall(r'GO:\d+',i)
        go_diff=','.join(go_terms_diff)
        diff_ex_list.append(go_diff)
    return diff_ex_list
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

#find all the go terms related to the original go terms list
def find_all_go(element,godatabase):
    element=element.split(',')
    for i in element:
        ori_go="id:"
        alt_go="alt_id:"+" "+i
        ori_go=ori_go+" "+i
        sub=subselect(ori_go,alt_go,godatabase)
        element=findrelgo(sub,element)
        result=','.join(element)
    return result

#find all go terms in the differential expression genes
def find_golist(go_list):
    total_go_list=[]
    for i in go_list:
        tem_list=i.split(',')
        total_go_list+=tem_list
    total_go_list_set=list(set(total_go_list))
    #remove the blank
    for i in total_go_list_set:
        if i=='':
            total_go_list_set.remove(i)
    return total_go_list_set, total_go_list

#calculate the number of genes in each go term
def counter_go(go_terms_list,go_list):
    dic_count={}
    for i in go_terms_list:
        dic_count[i]=go_list.count(i)
    return dic_count

#Combination formula
def comb(n,m):
    return math.factorial(n)//(math.factorial(n-m)*math.factorial(m))

#calculate the hypergeometric_distribution p_value for the go_terms
def hypergeometric_distribution(target_go_list,dic_count_diff,dic_count_total,number_total_genes,number_differential_genes):
    dic_final={}
    denominator=comb(number_total_genes,number_differential_genes)
    for i in target_go_list:
        p_value=0
        gene_go_dif=dic_count_diff[i]
        gene_go_total=dic_count_total[i]
        sum_p=0
        for j in range(gene_go_dif):
            mid_number=0
            if number_total_genes-gene_go_total<number_differential_genes-j:
                p_value=0
                break
            molecule1=comb((number_total_genes-gene_go_total),(number_differential_genes-j))
            molecule2=comb(gene_go_total,j)
            mid_number=molecule1*molecule2/denominator
            sum_p+=mid_number
        p_value=1-sum_p
        dic_final[i]=p_value
    return dic_final
#sort the go terms according to the p_value
def sort_final(final_dic):
    return sorted(final_dic.items(),key=lambda item:item[1])

#remove redundancy information like genes that hasn't been go annotated and columns like log2c_change
gene_expression_red=remove_redundancy_infor(gene_expression_read_file)
#create a copy:one for the analysis of dofferential expression genes,another for the total genes
gene_expression_red_copy=gene_expression_red
#calculate the total gene numbers for the enrichment analysis
number_total_genes=len(gene_expression_red.gene_id)
#select the differential genes according to the p_value
gene_expression_diff=diff_gene(gene_expression_red)
#calculate the number of differential expression genes
number_differential_genes=len(gene_expression_diff.gene_id)
#Go is treated as information only containing go number, not including its annotation
go_ori=find_ori_go(gene_expression_diff)
total_ori=find_ori_go(gene_expression_red_copy)
#find all go terms in the godatabasefile for the differential expression gene
for i in range(len(go_ori)):
    go_ori[i]=find_all_go(go_ori[i],godatabasefile)
#find all go terms in the databasefile for all genes
# total 19 min
for j in range(len(total_ori)):
    total_ori[j]=find_all_go(total_ori[j],godatabasefile)
#find the gene dataset for differential expression genes and total genes,since next step is to calculate the number of genes in each go term
go_dif_set,go_dif=find_golist(go_ori)
total_gene_set,total_gene=find_golist(total_ori)
#count the number of differential expression genes in each go term
dic_count_diff=counter_go(go_dif_set,go_dif)
#count the number of total genes in each go term
dic_count_total=counter_go(go_dif_set,total_gene)
#out put the final p_value
final=hypergeometric_distribution(go_dif_set,dic_count_diff,dic_count_total,number_total_genes,number_differential_genes)
#sort the go terms according to the p_value
final_file=sort_final(final)

