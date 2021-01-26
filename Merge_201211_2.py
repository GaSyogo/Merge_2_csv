# -*- coding: utf-8 -*-
#get_txt_from_sdf.py written by He
#2021.01.17
'''
note:this is a python script to merge several columns of the csv file which can be merged
the csv file is like:
solubility_ec_norm.csv

Command line arguments include
 - filename of a csvF file
 - filename of output file
'''

import sys
import pandas as pd 

def str2int(column): 
    # by ASCII
    A_Z=[chr(i) for i in range(65,91)]
    if len(column)==1:
        column=A_Z.index(column)
    elif len(column)==2:
        column=(A_Z.index(column[-2])+1)*26+A_Z.index(column[-1])
    return column

def mergecol(df):
    ##### Q ##### 
    new_df0 = df.iloc[:,0:20]
    #print("new_df0:",new_df0)

    ##### Q1 ##### 
    start_column='U'
    end_column='AV'

    # get id in column
    start_column=str2int(start_column)
    end_column=str2int(end_column)

    # Compare whether the last two digits of columns are the same
    new_data_list=[]
    new_name_list=[]
    for i in range(start_column,end_column+1):
        for j in range(i+1,end_column+1):
            if df.columns[i][-2:]==df.columns[j][-2:]:
                # df.loc[index,columns]:by real name; df.iloc[index,columns]:by id
                new_data_list.append(df.iloc[:,i]+df.iloc[:,j])
                new_name_list.append(df.columns[i][0:3]+df.columns[i][-2:])
            
    new_df1=pd.DataFrame(data=new_data_list)
    new_df1=new_df1.T
    new_df1.columns=new_name_list

    ##### Q2 #####        
    start_column='AW'
    end_column='GW'

    # get id in column
    start_column=str2int(start_column)
    end_column=str2int(end_column)

    # Compare whether the last 7 digits of columns are the same
    new_list=[]
    _list=list(df.columns[start_column:end_column+1])
    _data=df.iloc[:,start_column:end_column+1]
    c=0
    for column in _list:
        repeat_column=[x for x in range(len(_list)) if _list[x][-7:]==column[-7:]]
        _sum=0
        for i in repeat_column:
            _sum=_sum+_data.iloc[:,i]
        new_list.append([column[0:3]+column[-7:],_sum])

    new_dict = dict(new_list)
    new_df2 = pd.DataFrame(new_dict)

    # concat 3 new dataframes horizontally
    result_df = pd.concat([new_df0,new_df1,new_df2],axis=1)
    return result_df



def main(argv):
    inf = argv[1]
    outname = argv[2]
    #df=pd.read_csv(r'./solubility_ec_norm.csv',sep=',')
    df=pd.read_csv(r''+inf,sep=',')
    df.info()
    result_df = mergecol(df)
    result_df.to_csv(str(outname+'.csv'),index=False)

main(sys.argv)