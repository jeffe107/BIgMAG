#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:45:10 2023

@author: yepesgar
"""

from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import base64
import io
import numpy as np
import plotly.graph_objects as go
import dash_daq as daq


app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "BIGMAG"
server=app.server
labels_gunc = ['Number of scaffolds',
               'n_genes_called',
               'n_genes_mapped',
               'n_contigs',
               'proportion_genes_retained_in_major_clades',
               'genes_retained_index',
               'clade_separation_score',
               'contamination_portion',
               'n_effective_surplus_clades',
               'mean_hit_identity',
               'reference_representation_score',
    ]

parameters_heatmap = ['Completeness',
                      'Contamination',
                      'Complete',
                      'Single',
                      'Duplicated',
                      'Fragmented',
                      'Missing',
                      'proportion_genes_retained_in_major_clades',
                      'genes_retained_index',
                      'clade_separation_score',
                      'contamination_portion',
                      'n_effective_surplus_clades',
                      'mean_hit_identity',
                      'reference_representation_score'
    ]

labels_GTDB_Tk2 = [ 'Domain',
                   'Phylum',
                   'Class',
                   'Order',
                   'Family',
                   'Genus',
                   'Species'
    ]


app.layout = html.Div([
        html.Div(
            children=[
                html.P(children="🍔", className="header-emoji"),
                html.H1(
                    children="BIGMAG", className="header-title"
                ),
                html.P(
                    children=(
                        "Board InteGrating Metagenome-Assembled Genomes"
                    ),
                    className="header-description",
                ),
            
            ],
            className="header",
        ),
        dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files', style={"font-weight": "bold"})
                ]),
                style={'lineHeight': '60px',
                       'borderWidth': '1px',
                       'borderStyle': 'dashed',
                       'borderRadius': '5px',
                       'textAlign': 'center',
                       'justifyContent': 'center'
                    },
                className="drag-n-drop",
                # Allow multiple files to be uploaded
                multiple=True
            ),
        dbc.Row([
            dbc.Col(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P(children="CheckM2",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="checkm2",
                                            config={"displayModeBar": False},
                                        ),
                                        className="card", style={'width':'100%'}
                                    )
                                ],
                                className="wrapper",
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(children="Please select after uploading the file:", className="menu-title"),
                                                    dbc.RadioItems(['All bins', 'Only MAGs'],
                                                                   'All bins',
                                                                   id='filter-mags',
                                                                   inline=True,
                                                                   className="dropdown"),
                                        ]
                                    )],
                                className="menu",
                                ),
                            
                        ], className="card")],
                width=6
                ),
            dbc.Col(
                children=[  
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P(children="BUSCO",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="busco",
                                            config={"displayModeBar": False},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            ),
                            html.Div([
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Div(children="Filter by fragmented SCO:", className="menu-title"),
                                                    dcc.RangeSlider(
                                                        id='fragmented-slider',
                                                        min=0, max=100, step=10,
                                                        marks={0:{'label':'0', 'style':{'font-size':'18px'}},
                                                               25:{'label':'25', 'style':{'font-size':'18px'}},
                                                               50:{'label':'50', 'style':{'font-size':'18px'}},
                                                               75:{'label':'75', 'style':{'font-size':'18px'}},
                                                               100: {'label':'100', 'style':{'font-size':'18px'}}},
                                                        value=[0,20]
                                                        ),
                                                ]
                                            )],
                                        className="menu", style={'width': '35%', 'display': 'inline-block',
                                                                 'max-width': '600px', 'margin-left': '128px'}
                                        ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Div(children="Filter by missing SCO:", className="menu-title"),
                                                    dcc.RangeSlider(
                                                        id='missing-slider',
                                                        min=0, max=100, step=10,
                                                        marks={0:{'label':'0', 'style':{'font-size':'18px'}},
                                                               25:{'label':'25', 'style':{'font-size':'18px'}},
                                                               50:{'label':'50', 'style':{'font-size':'18px'}},
                                                               75:{'label':'75', 'style':{'font-size':'18px'}},
                                                               100: {'label':'100', 'style':{'font-size':'18px'}}},
                                                        value=[0,20]
                                                        ),
                                                ]
                                            )],
                                        className="menu", style={'width': '35%', 'float': 'right', 'display': 'inline-block',
                                                                 'max-width': '600px', 'margin-right': '128px'}
                                        )
                                ]),
                        ], className="card")],
                width=6
                )
            ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P(children="GUNC",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="gunc",
                                            config={"displayModeBar": False},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(children="Select parameter:", className="menu-title"),
                                            dcc.Dropdown(
                                                id="gunc-selection",
                                                options=[
                                                    {"label": label_gunc, "value": label_gunc}
                                                    for label_gunc in labels_gunc
                                                ],
                                                value="Number of scaffolds",
                                                clearable=False,
                                                className="dropdown",
                                                style={'width':'500px'}
                                            ),
                                        ]
                                    )],
                                className="menu",
                                )
                        ], className="card")],
                width=6
                ),
            dbc.Col(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P(children="QUAST",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="QUAST",
                                            config={"displayModeBar": False},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            ),
                        ], className="card")],
                width=6
                )
            ]),
        dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="GTDB-Tk2",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        dbc.Row([
                                            dbc.Col(
                                                children=[
                                                dcc.Graph(
                                                    id="GTDB-Tk2",
                                                    config={"displayModeBar": False},
                                                    style={'overflowY': 'auto', 'height': '800px'}
                                                        )
                                                ],
                                                width=11
                                                ),
                                            dbc.Col(
                                                children=[
                                                    daq.Slider(
                                                        vertical=True,
                                                        id='GTDB-Tk2-slider',
                                                        min=1,
                                                        max=10,
                                                        step=1,
                                                        value=1,
                                                        marks={1:{'label':'No sample', 'style':{'font-size':'20px'}},
                                                               10:{'label':'All samples', 'style':{'font-size':'20px'}}},
                                                        size=600,
                                                        handleLabel={"showCurrentValue": True,"label": "Sample"}
                                                        )
                                                    ],
                                                width=1, align="center")
                                            ])
                                        )
                                        ],
                                    className="card", style={'width': '100%', 'height': '800px', 'display': 'flex'}
                                    )
                                ],
                                className="wrapper"
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(children="Select taxonomic level:", className="menu-title"),
                                            dcc.Dropdown(
                                                id="GTDB-TK2-selection",
                                                options=[
                                                    {"label": label_GTDB_Tk2, "value": label_GTDB_Tk2}
                                                    for label_GTDB_Tk2 in labels_GTDB_Tk2
                                                ],
                                                value="Phylum",
                                                clearable=False,
                                                className="dropdown",
                                                style={'width':'500px'}
                                            ),
                                        ]
                                    )],
                                className="menu",
                                )
                            
                        ], width=12, className="card"),
                ]
                ),
        dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="Ponderation of the metrics:",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="heatmap",
                                            config={"displayModeBar": False},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            )
                        ], className="card")],
                width=12,
                )
            ])
        ])
        

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
                extract[i] = ';' + extract[i]

            string = ''
            my_list = []
            column_names = ['Domain', 'phylum', 'class','order','family', 'genus', 'species' ]
            df = pd.DataFrame(columns=column_names)
            
            for i in extract:
                if i != ';Unclassified Bacteria':
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
                    my_list = ['Unclassified Bacteria'] * 7
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
    extract = pd_series
    for i in range(len(extract)):
        extract[i] = ';' + extract[i]
    
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
    
    for i in extract:
        if i != ';Unclassified Bacteria':
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
            my_list = ['Unclassified Bacteria'] * 7
            df.loc[len(df)] = my_list
            my_list = []

    return pd.Series(df[tax_level])

@callback(
    [Output('GTDB-Tk2-slider', 'max'),
     Output('GTDB-Tk2-slider', 'marks')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
def update_sample_number(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        n_samples = len(data_df['sample'].unique())
        marks={0:{'label':'No sample', 'style':{'font-size':'20px'}},
               n_samples:{'label':'All samples', 'style':{'font-size':'20px'}}}
        
        return n_samples, marks
    

@callback(
    Output("busco", "figure"),
    Input("fragmented-slider", "value"),
    Input("missing-slider", "value"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
def update_figure_busco(frag_slider,miss_slider,list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        low_frag, high_frag = frag_slider
        low_miss, high_miss = miss_slider
        mask = (data_df["Fragmented"] >= low_frag) & (data_df["Fragmented"] <= high_frag) & (data_df["Missing"] >= low_miss) & (data_df["Missing"] <= high_miss)
        fig = px.scatter(
                        data_df[mask],
                        x = "Duplicated",
                        y = "Complete",
                        color = "sample",
                        hover_data=['Name']
            )
        fig.update_traces(marker=dict(size=14))
        fig.update_layout(font=dict(size=18),
                          xaxis_title="Duplicated (%)",
                          yaxis_title="Complete (%)",
                          legend_title="Sample/Pipeline:",
                          hoverlabel=dict(font_size=20)
                          )
    return fig

@callback(
    Output("checkm2", "figure"),
    Input("filter-mags", "value"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
def update_figure_checkm2(filter_mags,list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        data_df['Genome_Size'] = data_df['Genome_Size']/1000000
        data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
        if filter_mags == 'All bins':
            fig = px.scatter(
                        data_df,
                        x = "Contamination",
                        y = "Completeness",
                        color = "sample",
                        size = "Genome size (Mbp)",
                        hover_data=['Name']
            )
            fig.update_layout(font=dict(size=18),
                              xaxis_title="Contamination(%)",
                              yaxis_title="Completeness (%)",
                              legend_title="Sample/Pipeline:",
                              hoverlabel=dict(font_size=20)
                              )

        elif filter_mags == 'Only MAGs':
            temp_df = data_df.loc[(data_df['Completeness'] > 50) & (data_df['Contamination'] < 10)]
            fig = px.scatter(
                        temp_df,
                        x = "Contamination",
                        y = "Completeness",
                        color = "sample",
                        size = "Genome size (Mbp)",
                        hover_data=['Name']
            )
            fig.update_layout(font=dict(size=18),
                              xaxis_title="Contamination(%)",
                              yaxis_title="Completeness (%)",
                              legend_title="Sample/Pipeline:",
                              hoverlabel=dict(font_size=20)
                              )
    return fig

@callback(
    Output("gunc", "figure"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    Input("gunc-selection", "value"),
    prevent_initial_call=True
    )
def update_figure_gunc(list_of_contents, list_of_names, list_of_dates, gunc_parameter):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        fig = px.box(data_df, x="sample",
                     y=gunc_parameter,
                     color="pass.GUNC",
                     )
        fig.update_xaxes(tickangle=-90)
        fig.update_layout(font=dict(size=18),
                          xaxis_title="Sample/Pipeline",
                          legend_title="Bins passed GUNC:",
                          hoverlabel=dict(font_size=20)
                          )
        fig.update_layout(yaxis = dict(title_font = dict(size=15)))
    return fig

@callback(
    Output("heatmap", "figure"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
def update_figure_heatmap(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        
        final_df = pd.DataFrame()
        for sample in data_df["sample"].sort_values().unique():
            temp_df = data_df.loc[data_df['sample'] == sample]
            temp_df_2 = temp_df[parameters_heatmap].mean()
            temp_df_3 = temp_df_2.to_frame().transpose()
            temp_df_3['sample'] = sample
            final_df = pd.concat([final_df,temp_df_3], ignore_index = True)

        score_df = pd.DataFrame()
        for ind in final_df.index:

            score_checkm = 0
            score_busco = 0
            score_gunc = 0
            
            score_comp_checkm = (100 - final_df['Completeness'][ind])/100
            score_checkm += score_comp_checkm
            score_cont_checkm = (abs(0 - final_df['Contamination'][ind]))/100
            score_checkm += score_cont_checkm
            score_checkm /= 2
            
            score_comp_busco = (100 - final_df['Complete'][ind])/100
            score_busco += score_comp_busco
            score_sin_busco = (100 - final_df['Single'][ind])/100
            score_busco += score_sin_busco
            score_dupl_busco = (abs(0 - final_df['Duplicated'][ind]))/100
            score_busco += score_dupl_busco
            score_frag_busco = (abs(0 - final_df['Fragmented'][ind]))/100
            score_busco += score_frag_busco
            score_miss_busco = (abs(0 - final_df['Missing'][ind]))/100
            score_busco += score_miss_busco
            score_busco /= 5 
            
            score_prop_gunc = 1 - final_df['proportion_genes_retained_in_major_clades'][ind]
            score_gunc += score_prop_gunc
            score_genes_gunc = 1 - final_df['genes_retained_index'][ind]
            score_gunc += score_genes_gunc
            score_clade_gunc = abs(0 - final_df['clade_separation_score'][ind])
            score_gunc += score_clade_gunc
            score_cont_gunc = abs(0 - final_df['contamination_portion'][ind])
            score_gunc += score_cont_gunc
            score_effect_gunc = abs(0 - final_df['n_effective_surplus_clades'][ind])
            score_gunc += score_effect_gunc
            score_hit_gunc = 1 - final_df['mean_hit_identity'][ind]
            score_gunc += score_hit_gunc
            score_ref_gunc = 1 - final_df['reference_representation_score'][ind]
            score_gunc += score_ref_gunc
            score_gunc /= 7
            
            temp_dict = { [final_df['sample'][ind]][0]: [score_checkm, score_busco, score_gunc],
                         'Software':['CheckM2', 'BUSCO', 'GUNC']
                }

            temp_score_df = pd.DataFrame.from_dict(temp_dict)
            temp_score_df = temp_score_df.set_index('Software')
            score_df = pd.concat([score_df,temp_score_df], axis=1)
           
        results_gtdbtk = get_gtdbtk_results(data_df)
        
        gtdbtk_df = pd.DataFrame()
        for sample in results_gtdbtk['Sample'].unique():
            temp_df = results_gtdbtk.loc[results_gtdbtk['Sample'] == sample]
            temp_df = temp_df.reset_index()
            diff = (temp_df['Quantity'][2]/temp_df['Quantity'][0]) #Score to fix because it's different from the others
            temp_dict_2 = {'Software': ['GTDB-tk2'],
                           sample: [diff],
                           }
            temp_df = pd.DataFrame(temp_dict_2)
            temp_df = temp_df.set_index('Software')
            gtdbtk_df = pd.concat([gtdbtk_df,temp_df], axis=1)
        
        score_df = pd.concat([score_df,gtdbtk_df], axis=0)
        
        fig = px.imshow(score_df,
                        labels=dict(x="Sample/Pipeline", color="Score:"))
        fig.update_xaxes(tickangle=-90)
        fig.update_layout(font=dict(size=18),
                          hoverlabel=dict(font_size=20))
    return fig

@callback(
    Output("QUAST", "figure"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
    )
def update_figure_quast(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        
        results_gtdbtk = get_gtdbtk_results(data_df)

        fig = px.bar(results_gtdbtk,
                     x="Sample",
                     y="Quantity",
                     color='Feature',
                     barmode='group')
        fig.update_xaxes(tickangle=-90)
        fig.update_layout(font=dict(size=18),
                          xaxis_title="Sample/Pipeline",
                          legend_title="Feature:",
                          hoverlabel=dict(font_size=20)
                          )
    return fig


@app.callback(
    Output('GTDB-Tk2', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    Input("GTDB-Tk2-slider", "value"),
    Input("GTDB-TK2-selection", "value"),
    prevent_initial_call=True
    )
def update_gtdb_tk2(list_of_contents, list_of_names, list_of_dates, gtdbtk_parameter, tax_level):
    if list_of_contents is not None:
        data_df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        genera = extract_genus(data_df['classification'], tax_level) #genus is the label for tax_level
        
        data_df['Genus'] = genera
        data_df = data_df.reset_index(drop=True)
        
        unique_genus = data_df['Genus'].unique()
        unique_genus = unique_genus[unique_genus != '']
        
        final_df = pd.DataFrame({'Genus': unique_genus})
        for sample in data_df['sample'].unique():
            true_false_list = []
            temp_df = data_df.loc[data_df['sample'] == sample]
            for genus in unique_genus:
                if genus in list(temp_df['Genus']):
                    true_false_list.append(True)
                else:
                    true_false_list.append(False)
            temp_dict = {sample: true_false_list}
            temp_df = pd.DataFrame.from_dict(temp_dict)
            final_df = pd.concat([final_df,temp_df], axis=1)
        final_df = final_df.set_index('Genus')
        final_df['concatenated_row'] = final_df.apply(lambda x: ''.join(map(str, x)), axis=1)
        final_df = final_df.sort_values(by='concatenated_row', ascending=False)
        final_df = final_df.drop(columns=['concatenated_row'])
        final_df.drop(final_df.columns[gtdbtk_parameter:len(final_df.columns)], axis=1, inplace=True)
        
        
        arr_df = final_df.to_numpy()
    
        # Sample binary matrix
        data = arr_df
    
        # Get the indices of True and False values
        true_indices = np.argwhere(data)
        false_indices = np.argwhere(~data)
    
        # Sort True indices by x-coordinate
        true_indices = true_indices[np.argsort(true_indices[:, 1])]
    
        # Create scatter plot for True values
        scatter_true = go.Scatter(
            x=true_indices[:, 0],
            y=true_indices[:, 1],
            mode='markers',
            marker=dict(color='black', size=16),
            name='Present genus'
        )
    
        # Create scatter plot for False values
        scatter_false = go.Scatter(
            x=false_indices[:, 0],
            y=false_indices[:, 1],
            mode='markers',
            marker=dict(color='gray', size=16, opacity=0.5),
            name='Absent genus',
    
        )
    
        # Create lines for True values within the same category
        lines = []
        current_category = true_indices[0, 1]
        for i in range(1, len(true_indices)):
            if true_indices[i, 1] == current_category:
                line = go.Scatter(
                    x=[true_indices[i-1, 0], true_indices[i, 0]],
                    y=[true_indices[i-1, 1], true_indices[i, 1]],
                    mode='lines',
                    line=dict(color='black', width=2),
                    showlegend=False
                )
                lines.append(line)
            else:
                current_category = true_indices[i, 1]
    
        # Create layout with white background
        layout = go.Layout(
            xaxis=dict(
                tickvals=list(range(data.shape[0])),
                ticktext=final_df.index,
                showgrid=False,
                tickfont=dict(size=20),
                zeroline=False,
                side='top'
            ),
            yaxis=dict(
                tickvals=list(range(data.shape[1])),
                ticktext=final_df.columns,
                title='Samples',
                showgrid=False,
                tickfont=dict(size=20),
                title_font=dict(size=20),
                zeroline=False
            ),
            showlegend=True,
            title_x=0.5,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(size=20),
            shapes=[
                dict(
                    type='rect',
                    xref='paper',
                    yref='y',
                    x0=0,
                    y0=i - 0.5,
                    x1=1,
                    y1=i + 0.5,
                    fillcolor='lightgray',
                    opacity=0.3,
                    layer='below',
                    line=dict(width=0)
                ) for i in range(0, data.shape[1], 2)  # Highlight even rows
            ]
        )
        # Create figure
        fig = go.Figure(data=[scatter_false, scatter_true] + lines, layout=layout)
        fig.update_xaxes(tickangle=-45)
        fig.update_layout(legend=dict(
            yanchor="top",
            y=-0.1,
            xanchor="left",
            x=0.5
            )
                        )
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                             type="linear")
                              )
        return fig

if __name__ == '__main__':
    app.run(debug=True)



