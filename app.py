#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bio as dashbio
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import dash_daq as daq
import argparse
from BIgMAG_functions import labels_quast, labels_gunc, params_heatmap, params_to_normalize, names_heatmap, labels_GTDB_Tk2, extract_genus

labels_quast = labels_quast()
labels_gunc = labels_gunc()
labels_GTDB_Tk2 = labels_GTDB_Tk2()

parser = argparse.ArgumentParser(description="BIgMAG",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--port", help="Port to run the app.", default=8050, type=int)
parser.add_argument("file", help="File with concatenated dataframes.")
args = parser.parse_args()
config = vars(args)
data = config.get("file")
port = config.get("port")

def read_data():
    return pd.read_csv(data, sep='\t', index_col=0)
temp_data = read_data()
max_samples = len(temp_data['sample'].unique())
temp_data['id'] = temp_data['sample']
temp_data.set_index('id', inplace=True, drop=False)


app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "BIgMAG"

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
            className="header", style={'backgroundColor': '#22ae63'}
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
                dbc.Row([
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
                                                dbc.Row([
                                                    dbc.Col(
                                                        children=[
                                                            daq.Slider(
                                                                vertical=True,
                                                                id='busco-slider',
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
                                                            id="busco",
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
                                                    dcc.RangeSlider(1, max_samples,1, value=[1, max_samples],
                                                                    marks={1:{'label':'One sample', 'style':{'font-size':'20px'}},
                                                                           max_samples:{'label':'All samples', 'style':{'font-size':'20px'}}},
                                                                    tooltip={"placement": "bottom", "always_visible": True,
                                                                             "style": {"fontSize": "20px"}},
                                                                    allowCross=False, vertical=True,
                                                                    id='GTDB-Tk2-slider')
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
                                                value="Genus",
                                                clearable=False,
                                                className="dropdown",
                                                style={'width':'500px'}
                                            ),
                                        ]
                                    )],
                                className="menu",
                                )  
                        ], width=12, className="card"),
                ]),
            dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="Metrics at a glance:",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            id="heatmap",
                                            config={"displayModeBar": True},
                                            style={'overflowY': 'auto', 'height': '1080px', 'width': '1920px'}
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            )   
                        ], className="card"),
                        ],                    
                width=12,
                )
            ]),
            dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="Explore your data:",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                        html.Div(
                                        children=dash_table.DataTable(
                                                                    id='datatable-row-ids',
                                                                    columns=[
                                                                        {'name': i, 'id': i, 'deletable': True} for i in temp_data.columns
                                                                        # omit the id column
                                                                        if i != 'id'
                                                                    ],
                                                                    data=temp_data.to_dict('records'),
                                                                    editable=True,
                                                                    filter_action="native",
                                                                    sort_action="native",
                                                                    sort_mode='multi',
                                                                    row_selectable='multi',
                                                                    row_deletable=True,
                                                                    selected_rows=[],
                                                                    page_action='native',
                                                                    page_current= 0,
                                                                    page_size= 20,
                                                                    style_table={'overflowX': 'auto'}
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            )   
                        ], className="card"),
                        ],                    
                width=12,
                )
            ]),
        ])

@callback(
    Output("busco", "figure"),
    Input("busco-slider", "value"),
    Input("GTDB-TK2-selection", "value")
    )
def update_figure_busco(busco_param, tax_level):
    data_df = read_data()

    if "classification" in data_df.columns:
        tax_info = extract_genus(data_df['classification'], tax_level)
        data_df[tax_level] = tax_info
    else:
        data_df[tax_level] = [None] * len(data_df)

    data_df['Genome_Size'] = data_df['Genome_Size']/1000000
    data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
    data_df = data_df.loc[data_df['Complete'] >= busco_param]
    data_df = data_df.rename(columns={"Fragmented": "Fragmented SCO"})
    data_df = data_df.rename(columns={"Missing": "Missing SCO"})

    fig1 = px.scatter(
                    data_df,
                    x = "Duplicated",
                    y = "Complete",
                    color = "sample",
                    size = "Genome size (Mbp)",
                    hover_data=['Bin', "Fragmented SCO", "Missing SCO", tax_level],
                    template="simple_white"
        )
    
    df_l = data_df.sort_values("Genome size (Mbp)")
    min_size = data_df['Genome size (Mbp)'].min()
    max_size = data_df['Genome size (Mbp)'].max()
    sizes_legend = np.linspace(min_size, max_size, 5)
    sizes_legend = np.round(sizes_legend, 2)

    fig2 = px.scatter(
        df_l,
        x=np.zeros(len(data_df)),
        y=pd.qcut(df_l["Genome size (Mbp)"], q=5, precision=0, labels=sizes_legend).astype(str),
        size="Genome size (Mbp)", color_discrete_sequence=['black']
    )
    
    fig = go.Figure(
        data=[t for t in fig1.data] + [t.update(xaxis="x2", yaxis="y2") for t in fig2.data],
        layout=fig1.layout
    )
    
    fig.update_layout(
        xaxis_domain=[0, 0.92],
        xaxis2={"domain": [0.92, 1], "matches": None, "visible": False},
        yaxis2={"anchor": "free", "overlaying": "y", "side": "right", "position": 1},
        showlegend=True,
    )
    
    fig.update_layout(legend={'x':1.17,'y':0.5})
    fig.add_annotation(x=1.25, y=1.07,
                       xref='paper',
                       yref='paper',
                text="Genome size (Mbp)",
                showarrow=False)
    
    fig.update_layout(font=dict(size=18),
                          xaxis_title="Duplicated SCO (%)",
                          yaxis_title="Complete SCO (%)",
                          legend_title="Sample/Pipeline:",
                          hoverlabel=dict(font_size=20)
                          )
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                         type="linear")
                          )
    return fig

@callback(
    Output("CheckM2", "figure"),
    Input("CheckM2-slider", "value"),
    Input("GTDB-TK2-selection", "value")
    )
def update_figure_checkm2(checkm2_param, tax_level):
    data_df = read_data()

    if "classification" in data_df.columns:
        tax_info = extract_genus(data_df['classification'], tax_level)
        data_df[tax_level] = tax_info
    else:
        data_df[tax_level] = [None] * len(data_df)

    data_df['Genome_Size'] = data_df['Genome_Size']/1000000
    data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
    data_df = data_df.loc[data_df['Completeness'] >= checkm2_param]
    fig1 = px.scatter(
                    data_df,
                    x = "Contamination",
                    y = "Completeness",
                    color = "sample",
                    size = "Genome size (Mbp)",
                    hover_data=['Bin', tax_level],
                    template="simple_white"
        )
    
    df_l = data_df.sort_values("Genome size (Mbp)")
    min_size = data_df['Genome size (Mbp)'].min()
    max_size = data_df['Genome size (Mbp)'].max()
    sizes_legend = np.linspace(min_size, max_size, 5)
    sizes_legend = np.round(sizes_legend, 2)

    fig2 = px.scatter(
        df_l,
        x=np.zeros(len(data_df)),
        y=pd.qcut(df_l["Genome size (Mbp)"], q=5, precision=0, labels=sizes_legend).astype(str),
        size="Genome size (Mbp)", color_discrete_sequence=['black']
    )
    
    fig = go.Figure(
        data=[t for t in fig1.data] + [t.update(xaxis="x2", yaxis="y2") for t in fig2.data],
        layout=fig1.layout
    )
    
    fig.update_layout(
        xaxis_domain=[0, 0.92],
        xaxis2={"domain": [0.92, 1], "matches": None, "visible": False},
        yaxis2={"anchor": "free", "overlaying": "y", "side": "right", "position": 1},
        showlegend=True,
    )
    
    fig.update_layout(legend={'x':1.17,'y':0.5})
    fig.add_annotation(x=1.25, y=1.07,
                       xref='paper',
                       yref='paper',
                text="Genome size (Mbp)",
                showarrow=False)
    
    fig.update_layout(font=dict(size=18),
                          xaxis_title="Contamination (%)",
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
                 color_discrete_sequence = ['red', '#22ae63'],
                 template="simple_white"
                 )
    fig.update_xaxes(tickangle=-45)
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

    fig.update_xaxes(tickangle=-45)
    fig.update_layout(font=dict(size=18),
                      xaxis_title="Sample/Pipeline",
                      yaxis_title=quast_parameter,
                      hoverlabel=dict(font_size=20),
                      template="simple_white"
                      )
    fig.update_layout(yaxis = dict(title_font = dict(size=15)))
    return fig

@app.callback(
    Output('GTDB-Tk2', 'figure'),
    Input("GTDB-Tk2-slider", "value"),
    Input("GTDB-TK2-selection", "value")
    )
def update_gtdb_tk2(gtdbtk_parameter, tax_level):
    data_df = read_data()
    low_samples, high_samples = gtdbtk_parameter
    
    if "classification" in data_df.columns:
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
        final_df = final_df.transpose()
        final_df = final_df.reset_index(drop=False)
        final_df.index = final_df.index + 1
        final_df = final_df.loc[(final_df.index >= low_samples) & (final_df.index <= high_samples)]
        final_df = final_df.set_index('index', drop=True)
        final_df = final_df.transpose()
    
        final_df['concatenated_row'] = final_df.apply(lambda x: ''.join(map(str, x)), axis=1)
        final_df = final_df.sort_values(by='concatenated_row', ascending=False)
        final_df = final_df.drop(columns=['concatenated_row'])
        
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
            name='Present taxa'
        )
    
        # Create scatter plot for False values
        scatter_false = go.Scatter(
            x=false_indices[:, 0],
            y=false_indices[:, 1],
            mode='markers',
            marker=dict(color='gray', size=16, opacity=0.5),
            name='Absent taxa',
    
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
                title='Samples/Pipelines',
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
            y=2,
            xanchor="left",
            x=0.5))
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                             type="linear"))
        
        highlight_label = 'Unclassified'
        color_unclassified = 'red'
        color_all = 'dark blue'
        text_colors = [f"<span style='color:{str(color_unclassified)}'> {str(highlight_label)} </span>" if label == highlight_label else f"<span style='color:{str(color_all)}'> {str(label)} </span>" for label in final_df.index]
        fig.update_layout(xaxis=dict(ticktext=text_colors, tickmode='array', tickvals=list(range(data.shape[0]))))
        
        return fig

@callback(
    Output("heatmap", "figure"),
    Input("GTDB-TK2-selection", "value")
    )
def update_figure_heatmap(tax_level):
    data_df = read_data()
    parameters_heatmap = params_heatmap()
    parameters_to_normalize = params_to_normalize()
    names_for_heatmap = names_heatmap()
    final_df = pd.DataFrame()
    
    for sample in data_df["sample"].sort_values().unique():
        temp_df = data_df.loc[data_df['sample'] == sample]
        temp_df_2 = temp_df[parameters_heatmap].mean()
        temp_df_3 = temp_df_2.to_frame().transpose()
        temp_df_3['sample'] = sample
        pass_GUNC = temp_df['pass.GUNC'].value_counts()[True]/len(temp_df)
        temp_df_3['pass.GUNC'] = pass_GUNC
        
        temp_df = temp_df.reset_index(drop=True)        
        if "classification" in temp_df.columns:
            tax_series = temp_df['classification']
            gtdbtk = extract_genus(tax_series, tax_level)
            prop_gtdbtk = ((gtdbtk != 'Unclassified').sum())/(len(gtdbtk))
            temp_df_3['prop_gtdbtk'] = prop_gtdbtk
            final_df = pd.concat([final_df,temp_df_3], ignore_index = True)
        else:
            final_df = pd.concat([final_df,temp_df_3], ignore_index = True)
            
    for parameter in parameters_to_normalize:
        final_df[parameter] = final_df[parameter]/100
    
    parameters_heatmap.append('passed_GUNC')
    
    if "classification" in temp_df.columns:
        parameters_heatmap.append('gtdbtk2')
        color='red'
        names_for_heatmap.append(f"Proportion of annotated <span style='color:{str(color)}'> {str(tax_level)} </span> (GTDB-Tk2)")
    
    final_df = final_df.set_index('sample')
    final_df.columns = names_for_heatmap
    final_df = final_df.round(3)

    fig = dashbio.Clustergram(
            data=final_df,
            column_labels=list(final_df.columns.values),
            row_labels=list(final_df.index),
            height=1080,
            width=1920,
            cluster='row',
            color_map= [
                        [0.0, 'white'],
                        [1.0, '#22ae63']
            ],
            line_width=2,
            color_threshold={'row': 1.5,},
            color_list={'row': ['#636EFA', '#00CC96', '#19D3F3']}
    )

    fig.update_layout(font=dict(size=20,color='black'),
                      hoverlabel=dict(font_size=18))
    fig.update_xaxes(tickangle=-45,tickfont=dict(size=16))

    return fig

if __name__ == '__main__':
    app.run(port=port)
