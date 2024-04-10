#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:45:10 2023

@author: yepesgar
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import dash_daq as daq
import argparse
from BIgMAG_functions import extract_genus, get_gtdbtk_results

parser = argparse.ArgumentParser(description="BIgMAG",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--port", help="Port to run the app.", default=8050, type=int)
parser.add_argument("file", help="File with concatenated dataframes.")
args = parser.parse_args()
config = vars(args)
data = config.get("file")
port = config.get("port")

def read_data():
    return pd.read_csv(data, sep='\t')

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "BIgMAG"

labels_gunc = ['n_genes_called',
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

labels_quast = ["# contigs (>= 0 bp)",
                "# contigs (>= 1000 bp)"	,
                "# contigs (>= 5000 bp)",
                "# contigs (>= 10000 bp)",
                "# contigs (>= 25000 bp)",
                "# contigs (>= 50000 bp)",
                "Total length (>= 0 bp)",
                "Total length (>= 1000 bp)",
                "Total length (>= 5000 bp)",
                "Total length (>= 10000 bp)",
                "Total length (>= 25000 bp)",
                "Total length (>= 50000 bp)"	,
                "# contigs",
                "Largest contig",
                "Total length",
                "GC (%)",
                "N50",
                "N90",
                "auN",
                "L50",
                "L90",
                "# N's per 100 kbp"
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
                    children="BIgMAG", className="header-title"
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
        dbc.Row([
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
                                            config={"displayModeBar": True},
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
                                                id="quast-selection",
                                                options=[
                                                    {"label": label_quast, "value": label_quast}
                                                    for label_quast in labels_quast
                                                ],
                                                value="GC (%)",
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
                                                dbc.Row([
                                                    dbc.Col(
                                                        children=[
                                                            daq.Slider(
                                                                vertical=True,
                                                                id='CheckM2-slider',
                                                                min=0,
                                                                max=100,
                                                                step=10,
                                                                value=10,
                                                                marks={1:{'label':'0%', 'style':{'font-size':'16px'}},
                                                                       100:{'label':'100%', 'style':{'font-size':'16px'}}},
                                                                size=350,
                                                                handleLabel={"showCurrentValue": True,"label": "Value"},
                                                                labelPosition='top'
                                                                )
                                                            ],
                                                        width={"size":1, 'offset':1}, align='center'),
                                                    dbc.Col(
                                                        children=[
                                                        dcc.Graph(
                                                            id="CheckM2",
                                                            config={"displayModeBar": True},
                                                            style={'overflowY': 'auto', 'height': '570px'}
                                                                )
                                                        ],
                                                        width=10
                                                        )
                                                    ])
                                                )
                                                ],
                                            className="card", style={'width': '100%', 'display': 'flex'}
                                            )
                                        ],
                                        className="wrapper", style={'height': '683px', 'padding-left': '0px'}
                                    )
                                ], width=12, className="card", style={'width':'100%', 'margin-left': '13px'}),
                        ]
                        )
                ),

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
                                            config={"displayModeBar": True},
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
                                                value='clade_separation_score',
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
                                    html.P(children="BUSCO",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="busco",
                                            config={"displayModeBar": True},
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
                                                        value=[0,100]
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
                                                        value=[0,100]
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
                                                    config={"displayModeBar": True},
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
                                            config={"displayModeBar": True},
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
        


@callback(
    [Output('GTDB-Tk2-slider', 'max'),
     Output('GTDB-Tk2-slider', 'marks')],
    Input('quast-selection', 'value')
    )
def update_sample_number(quast_value):
    data_df = read_data()
    n_samples = len(data_df['sample'].unique())
    marks={0:{'label':'No sample', 'style':{'font-size':'20px'}},
           n_samples:{'label':'All samples', 'style':{'font-size':'20px'}}}
    
    return n_samples, marks
    

@callback(
    Output("busco", "figure"),
    Input("fragmented-slider", "value"),
    Input("missing-slider", "value")
    )
def update_figure_busco(frag_slider,miss_slider):
    data_df = read_data()
    low_frag, high_frag = frag_slider
    low_miss, high_miss = miss_slider
    mask = (data_df["Fragmented"] >= low_frag) & (data_df["Fragmented"] <= high_frag) & (data_df["Missing"] >= low_miss) & (data_df["Missing"] <= high_miss)
    fig = px.scatter(
                    data_df[mask],
                    x = "Duplicated",
                    y = "Complete",
                    color = "sample",
                    hover_data=['Bin']
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
    Output("CheckM2", "figure"),
    Input("CheckM2-slider", "value")
    )
def update_figure_checkm2(checkm2_param):
    data_df = pd.read_csv(data, sep='\t')
    data_df['Genome_Size'] = data_df['Genome_Size']/1000000
    data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
    data_df = data_df.loc[data_df['Completeness'] >= checkm2_param]
    fig = px.scatter(
                    data_df,
                    x = "Contamination",
                    y = "Completeness",
                    color = "sample",
                    size = "Genome size (Mbp)",
                    hover_data=['Bin']
        )
    fig.update_layout(font=dict(size=18),
                          xaxis_title="Contamination(%)",
                          yaxis_title="Completeness (%)",
                          legend_title="Sample/Pipeline:",
                          hoverlabel=dict(font_size=20)
                          )
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                         type="linear")
                          )
    return fig

@callback(
    Output("gunc", "figure"),
    Input("gunc-selection", "value")
    )
def update_figure_gunc(gunc_parameter):
    data_df = read_data()
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
    Output("QUAST", "figure"),
    Input("quast-selection", "value")
    )
def update_figure_quast(quast_parameter):
    data_df = read_data()
    N = len(data_df['sample'].unique())
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
    
    fig = go.Figure(
                    [go.Box(
                    y=data_df.loc[data_df['sample']==sample][quast_parameter],
                    x=data_df.loc[data_df['sample']==sample]['sample'],
                    marker_color = c[i],
                    boxpoints='all',
                    showlegend=False)
                    for i,sample in enumerate(data_df['sample'].unique())])

    fig.update_xaxes(tickangle=-90)
    fig.update_layout(font=dict(size=18),
                      xaxis_title="Sample/Pipeline",
                      yaxis_title=quast_parameter,
                      hoverlabel=dict(font_size=20)
                      )
    fig.update_layout(yaxis = dict(title_font = dict(size=15)))
    return fig

@callback(
    Output("heatmap", "figure"),
    Input("quast-selection", 'value')
    )
def update_figure_heatmap(quast_value):
    data_df = read_data()
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

@app.callback(
    Output('GTDB-Tk2', 'figure'),
    Input("GTDB-Tk2-slider", "value"),
    Input("GTDB-TK2-selection", "value")
    )
def update_gtdb_tk2(gtdbtk_parameter, tax_level):
    data_df = read_data()
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
    app.run(port=port)



