#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:38:18 2024

@author: yepesgar
"""
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import base64
import io
import numpy as np


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'tsv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), sep="\t")
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

def get_gtdbtk_results(data_df):
        gtdbtk_df = pd.DataFrame()
        for sample in data_df['sample'].unique():
            temp_df = data_df.loc[data_df['sample'] == sample]
            n_bins = len(temp_df)
            unique_bins = len(temp_df['classification'].unique())
            
            temp_df = temp_df.drop_duplicates(subset=['classification'])
            temp_df = temp_df.reset_index()
            extract = pd.Series(temp_df['classification'], index=None)
            
            for i in range(len(extract)):
                if pd.notna(extract[i]): 
                    extract[i] = ';' + extract[i]
                else:
                    extract[i] = 'NaN'

            string = ''
            my_list = []
            column_names = ['Domain', 'phylum', 'class','order','family', 'genus', 'species' ]
            df = pd.DataFrame(columns=column_names)
            
            for i in extract:
                if i != ';Unclassified Bacteria' and i != ';Unclassified' and i != ';Unclassified Archaea' and i != 'NaN':
                    for j in reversed(range(len(i))):
                        if i[j] != ';':
                            string += i[j]
                        else:
                            my_list.append(string)
                            string = ''
                    if len(my_list) == 7:
                        for i in range(len(my_list)):
                            my_list[i] = my_list[i][::-1]
                        for i in range(len(my_list)):
                            my_list[i] = my_list[i][3:]
                    my_list.reverse()
                    df.loc[len(df)] = my_list
                    my_list = []
                else:
                    my_list = ['Unclassified'] * 7
                    df.loc[len(df)] = my_list
                    my_list = []
            
            number_of_species = len([num for num in df['species'] if num != ""])
            
            temp_dict = { 'Sample': [sample] * 3,
                         'Quantity': [n_bins, unique_bins, number_of_species],
                         'Feature': ['Total bins', 'Unique bins', 'Species annotated']
                }

            temp_score_df = pd.DataFrame.from_dict(temp_dict)
            gtdbtk_df = pd.concat([gtdbtk_df,temp_score_df], ignore_index=True)
        return gtdbtk_df

def extract_genus(pd_series, tax_level):
    data = pd.Series()
    extract = pd_series

    for i in range(len(extract)):
        if pd.notna(extract[i]): 
            data = pd.concat([data, pd.Series(';' + extract[i])])
        else:
            data = pd.concat([data, pd.Series('NaN')])
        
    data = data.reset_index(drop=True)

    string = ''
    my_list = []
    column_names = ['Domain',
                    'Phylum',
                    'Class',
                    'Order',
                    'Family',
                    'Genus',
                    'Species' 
                    ]
    
    df = pd.DataFrame(columns=column_names)
    
    for i in data:
        if i != ';Unclassified Bacteria' and i != ';Unclassified' and i != ';Unclassified Archaea' and i != 'NaN':
            for j in reversed(range(len(i))):
                if i[j] != ';':
                    string += i[j]
                else:
                    my_list.append(string)
                    string = ''
            if len(my_list) == 7:
                for i in range(len(my_list)):
                    my_list[i] = my_list[i][::-1]
                for i in range(len(my_list)):
                    my_list[i] = my_list[i][3:]
            my_list.reverse()
            df.loc[len(df)] = my_list
            my_list = []
        else:
            my_list = ['Unclassified'] * 7
            df.loc[len(df)] = my_list
            my_list = []

    return pd.Series(df[tax_level])
