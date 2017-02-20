#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 22:36:52 2017

@author: bhumihar
"""

    
import pandas as pd
from pandas import ExcelWriter
import re
import numpy as np


def del_fun(lst):
    for x in lst :
        if (not x) or (' ' in x) :
            del x
    return lst

###State Code And State Name

stt_code =['AP',
    'AR',
    'AS',
    'BR',
    'CG',
    'GA',
    'GJ',
    'HR',
    'HP',
    'JK',
    'JH',
    'KA',
    'KL',
    'MP',
    'MH',
    'MN',
    'ML',
    'MZ',
    'NL',
    'OD',
    'OR',
    'PB',
    'RJ',
    'SK',
    'TN',
    'TR',
    'UP',
    'UK',
    'WB']

stt_list =['Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jammu and Kashmir',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Orissa',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Chennai',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal']

fun = lambda x:re.compile('[ a-zA-Z]+').findall(x)
fun1 = lambda x:x.replace('Dstt','')
fun2 = lambda x:x.replace('District','')
fun3 = lambda x: x.split('(Id')[0]
fun4 = lambda x:x.replace('Distt','')
fun5 = lambda x: re.split(r'[,\n]', x)
uni = pd.read_excel('universities -list.xlsx');
uni['detail'] = uni['College Name'].apply(fun5[1:])
uni['detail1'] = uni['detail'] 

i=-1

for x in uni['detail'] :
    i = i+1
    if not x :
        continue;
    else :
        word1 = x[-1]
        word1 = fun3(word1)
        word1 = fun1(word1)
        word1 = fun2(word1)
        word1 = fun4(word1)
        word1 = fun(word1)
        word1 = [x for x in word1 if ((not(x==' ')) or (not x)) and (len(x)>1)]
        word1 = [x for x in word1 if (not('University' in x))]
        uni['detail1'][i] = word1
        
        if pd.isnull(uni['State'][i]) and word1:
            if ((word1[-1] in stt_list) or (word1[-1] in stt_code)):
                uni['State'][i] = word1[-1]
                del word1[-1] 
                
        if pd.isnull(uni['Dist/Location'][i]) and word1:
            wordv = word1[-1].strip()
            if ((wordv in stt_list) or (wordv in stt_code) or (len(wordv)==1)):
                del word1[-1]
                
        if pd.isnull(uni['Dist/Location'][i]) :
            try :
                dword = x[0:len(x)-1]
                if word1:
                    dword.append(word1[0])
                dword = [x for x in dword if ((not(x==' ')) or (not x)) and (len(x)>1)]
                val = ",".join(dword)
                val1 = val.strip()
                
            except IndexError:
                continue ;
            uni['Dist/Location'][i] = val1
i=-1
for x in uni['State']:
    i =i+1
    if type(x) is float :
        continue ;
    else :
        if (x not in stt_list) and (x not in stt_code) :
            val1 = funw(x.lower(),stt_list)
            val = stt_list[val1.index(min(val1))]
            uni['State'][i] = val

uni['College Name'] = uni['College Name'].apply(fun5[0])
uni['College Name'] = uni['College Name'].apply(fun3)


uni.drop_duplicates(['College Name','State'],inplace = True)
uni.drop_duplicates(['College Name','Dist/Location'],inplace = True)
uni.drop(['detail','detail1'],axis=1,inplace=True)

writer = ExcelWriter('Update-universities -list.xlsx')
uni.to_excel(writer,'Sheet5', na_rep="     ",header=True)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet5']

# Set the column width and format.
worksheet.set_column('B:B', 50)
worksheet.set_column('C:C', 35)
worksheet.set_column('D:D', 15)


writer.save()
