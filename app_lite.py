#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bio as dashbio
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import dash_daq as daq
import argparse
from BIgMAG_functions import params_heatmap, params_to_normalize, names_heatmap, extract_genus, labels_summary, patch_file, ExternalResourceParser
import os
import requests
from scipy.stats import kruskal
import scikit_posthocs as sp
import pingouin as pg

parser = argparse.ArgumentParser(description="BIgMAG",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--port", help="Port to run the app.", default=8050, type=int)
parser.add_argument("file", help="File with concatenated dataframes.")
parser.add_argument("--cl_checkm2", help="Genome completeness level for CheckM2", default=10, type=int)
parser.add_argument("--csco_busco", help="Genome completeness of SCO for BUSCO", default=10, type=int)
parser.add_argument("--param_gunc", help="Parameter to show the data distribution for GUNC", default='clade_separation_score', type=str)
parser.add_argument("--param_quast", help="Parameter to show the data distribution for QUAST", default="GC (%)", type=str)
parser.add_argument("--samples_gtdbtk2", help="Number of samples to display on the GTDB-Tk2 plot", type=int)
parser.add_argument("--tax_level", help="Taxonomic level to display information on GTDB-Tk2 plot", default="Phylum", type=str)
parser.add_argument("-o","--outdir", help="Directory to store the html file", type=str)

args = parser.parse_args()
config = vars(args)
data = config.get("file")
port = config.get("port")
completeness_level = config.get("cl_checkm2")
complete_SCO = config.get("csco_busco")
gunc_parameter = config.get("param_gunc")
quast_parameter = config.get("param_quast")
tax_level = config.get("tax_level")
outdir = config.get("outdir")

def read_data():
    return pd.read_csv(data, sep='\t', index_col=0)

temp_data = read_data()
temp_data['id'] = temp_data['sample']
temp_data.set_index('id', inplace=True, drop=False)

if config.get("samples_gtdbtk2"):
    gtdbtk_parameter = config.get("samples_gtdbtk2")
else:
    gtdbtk_parameter = len(temp_data['sample'].unique())


app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], eager_loading=True)
app.title = "BIgMAG"

def write_file(file_path: str, content: bytes, target_dir=f"{outdir}/bigmag", ):
    target_file_path = os.path.join(target_dir, file_path.lstrip('/').split('?')[0])
    target_leaf_dir = os.path.dirname(target_file_path)
    os.makedirs(target_leaf_dir, exist_ok=True)
    with open(target_file_path, 'wb') as f:
        f.write(content)
    pass

def make_static(base_url, target_dir=f"{outdir}/bigmag"):
    index_html_bytes = requests.get(base_url).content
    json_paths = ['_dash-layout', '_dash-dependencies', ]
    extra_json = {}
    for json_path in json_paths:
        json_content = requests.get(base_url + json_path).content
        extra_json[json_path] = json_content

    patched_bytes = patch_file('bigmag.html', index_html_bytes, extra=extra_json)
    write_file('bigmag.html', patched_bytes, target_dir)
    parser = ExternalResourceParser()
    parser.feed(patched_bytes.decode('utf8'))

    for resource_url in parser.resources:
        resource_url_full = base_url + resource_url
        print(f'get {resource_url_full}')
        resource_bytes = requests.get(resource_url_full).content
        patched_bytes = patch_file(resource_url, resource_bytes)
        write_file(resource_url, patched_bytes, target_dir)

def figure_busco(complete_SCO):
    data_df = read_data()

    if "classification" in data_df.columns:
        tax_info = extract_genus(data_df['classification'], tax_level)
        data_df[tax_level] = tax_info
    else:
        data_df[tax_level] = ['Not found'] * len(data_df)

    data_df['Genome_Size'] = data_df['Genome_Size']/1000000
    data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
    data_df = data_df.loc[data_df['Complete'] >= complete_SCO]
    data_df = data_df.rename(columns={"Fragmented": "Fragmented SCO"})
    data_df = data_df.rename(columns={"Missing": "Missing SCO"})
    fig1 = px.scatter(
                    data_df,
                    x = "Duplicated",
                    y = "Complete",
                    color = "sample",
                    size = "Genome size (Mbp)",
                    hover_data=['Bin', tax_level, 'Fragmented SCO', 'Missing SCO'],
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
    
    fig.update_layout(legend={'x':1.1,'y':0.5})
    fig.add_annotation(x=1.15, y=1.15,
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

def figure_checkm2(completeness_level):
    data_df = read_data()

    if "classification" in data_df.columns:
        tax_info = extract_genus(data_df['classification'], tax_level)
        data_df[tax_level] = tax_info
    else:
        data_df[tax_level] = ['Not found'] * len(data_df)

    data_df['Genome_Size'] = data_df['Genome_Size']/1000000
    data_df = data_df.rename(columns={"Genome_Size": "Genome size (Mbp)"})
    data_df = data_df.loc[data_df['Completeness'] >= completeness_level]
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
    
    fig.update_layout(legend={'x':1.1,'y':0.5})
    fig.add_annotation(x=1.15, y=1.15,
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

def figure_gunc(gunc_parameter):
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

def figure_quast(quast_parameter):
    data_df = read_data()

    N = len(data_df['sample'].unique())
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
    data_df_subset = data_df[['sample', quast_parameter]]
    test = pg.welch_anova(dv=quast_parameter, between='sample', data=data_df_subset)

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

    p_value = round(test['p-unc'][0],4)
    if p_value < 0.05:
        color = 'red'
        fig.add_annotation(x=0.3,y=1.1, text=f"<i>p</i>-value <b>Welch ANOVA</b> test: <span style='color:{str(color)}'> {str(p_value)} </span>", showarrow=False, font=dict(size=16),
                       xref="paper", yref="paper")

    else:
        fig.add_annotation(x=0.3,y=1.1, text=f"<i>p</i>-value <b>Welch ANOVA</b> test: {p_value}", showarrow=False, font=dict(size=16),
                       xref="paper", yref="paper")
    
    return fig

def figure_gtdbtk2(gtdbtk_parameter, tax_level):
    data_df = read_data()
    low_samples = 1 
    high_samples = gtdbtk_parameter
    
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

def figure_heatmap():
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
                        [0.0, '#F5F5F5'],
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

def heatmap_Dunn():
    data_df = read_data()
    samples = data_df['sample'].unique()

    if len(samples) > 1:
        df_4_barplot = pd.DataFrame()
        df_4_kruskal = pd.DataFrame()

        for sample in samples:
            if "classification" in data_df.columns:
                genera = extract_genus(data_df['classification'], tax_level) #genus is the label for tax_level
                data_df['Genus'] = genera
                data_df = data_df.reset_index(drop=True)
                tax_tmp_df = data_df.loc[data_df['sample'] == sample]
                n_annotated_bins = len(tax_tmp_df.loc[(tax_tmp_df['Genus'] != "Unclassified")])
                if 'Unclassified' in tax_tmp_df['Genus']:
                    unique_annot_bins = len(tax_tmp_df['Genus'].unique()) - 1
                else:
                    unique_annot_bins = len(tax_tmp_df['Genus'].unique())
            else:
                tax_tmp_df = data_df.loc[data_df['sample'] == sample]

            
            mid_quality_mags = len(tax_tmp_df.loc[(tax_tmp_df['Completeness'] >= 50) & (tax_tmp_df['Contamination'] <= 10)])
            high_quality_mags = len(tax_tmp_df.loc[(tax_tmp_df['Completeness'] >= 90) & (tax_tmp_df['Contamination'] <= 5)])
            bins_pass_GUNC = len(tax_tmp_df.loc[(tax_tmp_df['pass.GUNC'] == True)])
            n_bins = len(tax_tmp_df)

            if "classification" in data_df.columns:
                tmp_dict_tax = {'sample': sample,
                                'N_annotated_bins': n_annotated_bins,
                                "N_unique_annotated_bins": unique_annot_bins,
                                'N_mid_quality_MAGs': mid_quality_mags,
                                'N_high_quality_MAGs': high_quality_mags,
                                'N_bins_passing_GUNC': bins_pass_GUNC,
                                'N_bins': n_bins
                                }
            else:
                tmp_dict_tax = {'sample': f"{sample}, n = {n_bins}",
                                '# of mid-quality MAGs': mid_quality_mags,
                                '# of high-quality MAGs': high_quality_mags,
                                '# of bins passing GUNC': bins_pass_GUNC}
                
            tmp_df_annot = pd.DataFrame([tmp_dict_tax])
            column_names = list(tmp_df_annot.columns[1:])
            
            df_4_kruskal = pd.concat([df_4_kruskal, tmp_df_annot], ignore_index = True)

            for column in column_names:
                tmp_df_annot[column] = (tmp_df_annot[column] / n_bins) * 100
            
            df_4_barplot = pd.concat([df_4_barplot, tmp_df_annot], ignore_index = True)

        df_4_kruskal_long = pd.melt(df_4_kruskal, id_vars=['sample'], var_name='feature', value_name='value')
        groups = [df_4_kruskal_long[df_4_kruskal_long['sample'] == t]['value'].values for t in df_4_kruskal_long['sample'].unique()]
        kruskal_result = kruskal(*groups)
        dunn_result = sp.posthoc_dunn(df_4_kruskal_long, val_col='value', group_col='sample', p_adjust='bonferroni')

        fig = go.Figure()

        custom_color_scale = [
                                    [0.0, '#22ae63'],
                                    [1.0, '#F5F5F5']]
        fig = px.imshow(dunn_result, 
                        labels=dict(x="Sample/Pipeline", y="Sample/Pipeline", color="P-value"),
                        x=dunn_result.columns,
                        y=dunn_result.index,
                        color_continuous_scale=custom_color_scale,
                        zmin=0, zmax=1)

        # Customize axis labels and title
        fig.update_layout(
            title_font=dict(size=16),
            font=dict(size=18),
            hoverlabel=dict(font_size=20)
        )

        if kruskal_result.pvalue < 0.05:
            color = 'red'
            p_value = round(kruskal_result.pvalue, 5)
            fig.update_layout(
                title=dict(text=f"<b>Kruskal-Wallis <i>p</i>-value =</b> <span style='color:{str(color)}'> {str(p_value)} </span><br><i>p</i>-value matrix of a Duncan Test",
                    y=0.97,x=0.5,)
            )
        else:
            p_value = round(kruskal_result.pvalue, 5)
            fig.update_layout(
                title=dict(text=f"<b>Kruskal-Wallis <i>p</i>-value =</b> {p_value}<br><i>p</i>-value matrix of a Duncan Test",
                    y=0.97,x=0.5,)
            )

        return fig

def summary_barplot():
    data_df = read_data()
    samples = data_df['sample'].unique()
    df_4_barplot = pd.DataFrame()

    for sample in samples:
        if "classification" in data_df.columns:
            genera = extract_genus(data_df['classification'], tax_level) #genus is the label for tax_level
            data_df['Genus'] = genera
            data_df = data_df.reset_index(drop=True)
            tax_tmp_df = data_df.loc[data_df['sample'] == sample]
            n_annotated_bins = len(tax_tmp_df.loc[(tax_tmp_df['Genus'] != "Unclassified")])
            if 'Unclassified' in list(tax_tmp_df['Genus']):
                unique_annot_bins = len(tax_tmp_df['Genus'].unique()) - 1
            else:
                unique_annot_bins = len(tax_tmp_df['Genus'].unique())
        else:
            tax_tmp_df = data_df.loc[data_df['sample'] == sample]

        
        mid_quality_mags = len(tax_tmp_df.loc[(tax_tmp_df['Completeness'] >= 50) & (tax_tmp_df['Contamination'] <= 10)])
        high_quality_mags = len(tax_tmp_df.loc[(tax_tmp_df['Completeness'] >= 90) & (tax_tmp_df['Contamination'] <= 5)])
        bins_pass_GUNC = len(tax_tmp_df.loc[(tax_tmp_df['pass.GUNC'] == True)])
        n_bins = len(tax_tmp_df)

        if "classification" in data_df.columns:

            tmp_dict_tax = {'sample': f"{sample},<br>n = {n_bins}",
                            'N_annotated_bins': n_annotated_bins,
                            "N_unique_annotated_bins": unique_annot_bins,
                            'N_mid_quality_MAGs': mid_quality_mags,
                            'N_high_quality_MAGs': high_quality_mags,
                            'N_bins_passing_GUNC': bins_pass_GUNC,
                            }
        else:
            tmp_dict_tax = {'sample': f"{sample},<br>n = {n_bins}",
                            '# of mid-quality MAGs': mid_quality_mags,
                            '# of high-quality MAGs': high_quality_mags,
                            '# of bins passing GUNC': bins_pass_GUNC}
            
        tmp_df_annot = pd.DataFrame([tmp_dict_tax])
        column_names = list(tmp_df_annot.columns[1:])
        
        for column in column_names:
            tmp_df_annot[column] = (tmp_df_annot[column] / n_bins) * 100

        df_4_barplot = pd.concat([df_4_barplot, tmp_df_annot], ignore_index = True)

    fig = go.Figure()

    if "classification" in data_df.columns:
        # Define colors for each variable
        colors = ['#e74c3c', '#f39c12', '#9b59b6', '#22ae63', '#3498db']
        color = 'red'

        legend_names = [f"% of annotated MAGs at <span style='color:{str(color)}'> {str(tax_level)} </span> level (GTDB-Tk2)",
                '% of unique annotated MAGs (GTDB-Tk2)',
                '% of mid-quality MAGs (CheckM2)',
                '% of high-quality MAGs (CheckM2)',
                '% of bins passing GUNC',
        ]

        # Add a bar trace for each variable
        for i, column in enumerate(df_4_barplot.columns[1:]):  # Skip the 'Sample' column
            fig.add_trace(go.Bar(
                x=df_4_barplot['sample'],
                y=df_4_barplot[column],
                name=legend_names[i],
                marker_color=colors[i]
        ))
        
        # Add vertical lines to separate the x-axis labels
        for i in range(1, len(samples)):
            fig.add_shape(
                        type="line",
                        x0=i - 0.5, x1=i - 0.5,
                        y0=0, y1=100,
                        line=dict(color="#000000", width=3)
                        )

        # Update layout for better readability
        fig.update_layout(
            barmode='group',
            xaxis_title='Sample/Pipeline',
            yaxis=dict(
                        title='Percentage (%)',
                        range=[0, 110],  # Ensure the y-axis extends a bit above 100
                            ),
            template="simple_white",
            hoverlabel=dict(font_size=20),
            legend=dict(title="Percentages:", yanchor = "bottom", xanchor = "left", font=dict(size=14), x=0.3, y=1.0),
            font=dict(size=18)
        )
        fig.update_xaxes(tickangle=-45)
        return fig
    
    else:
        # Define colors for each variable
        colors = ['#e74c3c', '#22ae63', '#3498db']

        legend_names = [
                '% of mid-quality MAGs (CheckM2)',
                '% of high-quality MAGs (CheckM2)',
                '% of bins passing GUNC'
        ]

        # Add a bar trace for each variable
        for i, column in enumerate(df_4_barplot.columns[1:]):  # Skip the 'Sample' column
            fig.add_trace(go.Bar(
                x=df_4_barplot['sample'],
                y=df_4_barplot[column],
                name=legend_names[i],
                marker_color=colors[i]
        ))
            
        # Add vertical lines to separate the x-axis labels
        for i in range(1, len(samples)):
            fig.add_shape(
                        type="line",
                        x0=i - 0.5, x1=i - 0.5,
                        y0=0, y1=100,
                        line=dict(color="#000000", width=3)
                        )

        # Update layout for better readability
        fig.update_layout(
            barmode='group',
            xaxis_title='Sample/Pipeline',
            yaxis=dict(
                        title='Percentage (%)',
                        range=[0, 110],  # Ensure the y-axis extends a bit above 100
                            ),
            template="simple_white",
            hoverlabel=dict(font_size=20),
            legend=dict(title="Percentages:", yanchor = "bottom", xanchor = "left", font=dict(size=14), x=0.3, y=1.0),
            font=dict(size=18)
        )
        fig.update_xaxes(tickangle=-45)
        return fig


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
                html.Div(
                    children=[
                        dbc.Button("Save .html", color="dark", n_clicks=0, id='save', className="me-1"),
                    ],
                        style={'textAlign': 'center',
                                'justifyContent': 'center',
                                'margin-left': 'auto',
                                'margin-right': 'auto'}
                ),
                html.P(
                    ["Documentation:", 
                     html.A(" 🔗 Yepes-García J and Falquet L. (2024)", href="https://f1000research.com/articles/13-640", target="_blank", className="custom-link")
                    ], className="header-citation"
                    
                ),
            ],
            className="header", style={'backgroundColor': '#22ae63', 'height': '330px'}
        ),
        dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="Summary",
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
                                                    figure=summary_barplot(),
                                                    config={"displayModeBar": True},
                                                    style={'overflowY': 'auto', 'height': '800px', 'width': '960px'}
                                                        )
                                                ],
                                                width=6
                                                ),
                                            dbc.Col(
                                                children=[
                                                    dcc.Graph(
                                                        figure=heatmap_Dunn(),
                                                        config={"displayModeBar": True},
                                                        style={'overflowY': 'auto', 'height': '800px', 'width': '960px'}
                                                    ),
                                                    ],
                                                width=6)
                                            ])
                                        )
                                        ],
                                    className="card", style={'width': '100%', 'height': '800px', 'display': 'flex'}
                                    )
                                ],
                                className="wrapper"
                            ),  
                        ], width=12, className="card"),
                ]),

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
                                            figure=figure_quast(quast_parameter),
                                            config={"displayModeBar": True},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
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
                                    html.P(children="CheckM2",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            figure=figure_checkm2(completeness_level),
                                            config={"displayModeBar": True},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
                            ),

                        ], className="card")],
                width=6
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
                                            figure=figure_gunc(gunc_parameter),
                                            config={"displayModeBar": True},
                                        ),
                                        className="card",
                                    )
                                ],
                                className="wrapper",
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
                                            figure=figure_busco(complete_SCO),
                                            config={"displayModeBar": True},
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
                                                    figure=figure_gtdbtk2(gtdbtk_parameter, tax_level),
                                                    config={"displayModeBar": True},
                                                    style={'overflowY': 'auto', 'height': '800px'}
                                                        )
                                                ],
                                                width=12
                                                ),

                                            ])
                                        )
                                        ],
                                    className="card", style={'width': '100%', 'height': '800px', 'display': 'flex'}
                                    )
                                ],
                                className="wrapper"
                            ),

                        ], width=12, className="card"),
                ]),
            dbc.Row([
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                            html.Div(
                                children=[
                                    html.P(children="Clustering of samples/pipelines",
                                           className="slider-title")
                                    ]
                                ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=dcc.Graph(
                                            figure=figure_heatmap(),
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
                                    html.P(children="Explore your data",
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
        
@app.callback(
    Output('save', 'children'),
    Input('save', 'n_clicks'),
    prevent_initial_call=True
    )
def save_result(n_clicks):
    if n_clicks == 0:
        return 'Save .html'
    else:
        make_static(f'http://127.0.0.1:{port}/')
        return 'Saved, check your specified directory'

if __name__ == '__main__':
    app.run(port=port, debug=True)
