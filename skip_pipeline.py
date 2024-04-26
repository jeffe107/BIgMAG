#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys

path = sys.argv[1]
outdir = sys.argv[2]

data = pd.read_csv(path)
data = data.set_index('sampleID')

list_of_sample_dfs = []
for index,row in data.iterrows():
    
    if pd.notna(row['busco_path']):
        busco_df = pd.read_csv(row['busco_path'], sep='\t')
        busco_df = busco_df.sort_values(by=['Input_file'])
        busco_df['Input_file'] = busco_df['Input_file'].apply(lambda x: x.split('.')[0])
    else:
        busco_df = pd.DataFrame({'Input_file': ['empty_df']})
        
    if pd.notna(row['checkm2_path']):
        checkm2_df = pd.read_csv(row['checkm2_path'], sep='\t')
        checkm2_df = checkm2_df.sort_values(by=['Name'])
    else:
        checkm2_df = pd.DataFrame({'Name': ['empty_df']})
        
    if pd.notna(row['gunc_path']):
        gunc_df = pd.read_csv(row['gunc_path'], sep='\t')
        gunc_df = gunc_df.sort_values(by=['genome'])
    else:
        gunc_df = pd.DataFrame({'genome': ['empty_df']})
    
    if pd.notna(row['quast_path']):
        quast_df = pd.read_csv(row['quast_path'], sep='\t')
        quast_df = quast_df.sort_values(by=['Assembly'])
    else:
        quast_df = pd.DataFrame({'Assembly': ['empty_df']})
        
    if pd.notna(row['gtdbtk2_bac_path']):
        gtdbtk2_bac_df = pd.read_csv(row['gtdbtk2_bac_path'], sep='\t')
        gtdbtk2_bac_df = gtdbtk2_bac_df.sort_values(by=['user_genome'])
    else:
        gtdbtk2_bac_df = pd.DataFrame({'user_genome': ['empty_df']})
        
    if pd.notna(row['gtdbtk2_ar_path']):
        gtdbtk2_ar_df = pd.read_csv(row['gtdbtk2_ar_path'], sep='\t')
        gtdbtk2_ar_df = gtdbtk2_ar_df.sort_values(by=['user_genome'])
        
    if pd.notna(row['gtdbtk2_ar_path']) and pd.notna(row['gtdbtk2_bac_path']):
        gtdbtk2_bac_df = pd.concat([gtdbtk2_bac_df, gtdbtk2_ar_df], axis=0, ignore_index=True)
    
    if pd.notna(row['gtdbtk2_ar_path']) and pd.isna(row['gtdbtk2_bac_path']):
        gtdbtk2_bac_df = gtdbtk2_ar_df
    
    df_list = [busco_df, checkm2_df, gtdbtk2_bac_df, gunc_df, quast_df]
    column_names = ['Input_file','Name', 'user_genome', 'genome', 'Assembly']
    
    
    longest_df = ''
    column_longest_df = ''
    for i in range(len(df_list)):
        length = len(df_list[i])
        if length > len(longest_df):
            longest_df = df_list[i]
            column_longest_df = column_names[i]
    
    for i in range(len(df_list)):
        if df_list[i].equals(longest_df):
            df_list.pop(i)
            column_names.pop(i)
            break
    
    for i in range(len(df_list)):
        longest_df = pd.merge(longest_df, df_list[i], left_on=column_longest_df, right_on=column_names[i], how='left')
        temp_df = df_list[i]
    
    longest_df = longest_df.rename(columns={column_longest_df: "Bin"})
    longest_df['sample'] = [index] * len(longest_df)
    longest_df = longest_df.drop(columns=column_names)
    longest_df = longest_df.reset_index(drop=True)
    first_column = longest_df.pop('sample')
    longest_df.insert(0,'sample',first_column)
    
    list_of_sample_dfs.append(longest_df)

final_df = pd.DataFrame()
for df in list_of_sample_dfs:
    final_df = pd.concat([final_df, df], axis=0, ignore_index=True)

first_column = final_df.pop('sample')
final_df.insert(0,'sample',first_column)
final_df = final_df.sort_values(['sample', 'Bin'])
final_df = final_df.reset_index(drop=True)

final_df = final_df.fillna(0)
final_df.to_csv(f"{outdir}/final_df.tsv", sep="\t")
