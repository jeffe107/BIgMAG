#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:38:18 2024

@author: yepesgar
"""
import pandas as pd
from html.parser import HTMLParser

def labels_gunc():
    labels = ['n_genes_called',
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
    return labels

def labels_quast():
    labels = ["# contigs (>= 0 bp)",
                    "# contigs (>= 1000 bp)",
                    "# contigs (>= 5000 bp)",
                    "# contigs (>= 10000 bp)",
                    "# contigs (>= 25000 bp)",
                    "# contigs (>= 50000 bp)",
                    "Total length (>= 0 bp)",
                    "Total length (>= 1000 bp)",
                    "Total length (>= 5000 bp)",
                    "Total length (>= 10000 bp)",
                    "Total length (>= 25000 bp)",
                    "Total length (>= 50000 bp)",
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
    return labels

def params_heatmap():
    parameters = ['Completeness',
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
                          'reference_representation_score',
        ]
    return parameters

def params_to_normalize():
    parameters = ['Completeness',
                           'Contamination',
                           'Complete',
                           'Single',
                           'Duplicated',
                           'Fragmented',
                           'Missing']

    return parameters

def names_heatmap(): 
    names = [ 'Completeness (CheckM2)',
                      'Contamination (CheckM2)',
                      'Complete SCO (BUSCO)',
                      'Single SCO (BUSCO)',
                      'Duplicated SCO (BUSCO)',
                      'Fragmented SCO (BUSCO)',
                      'Missing SCO (BUSCO)',
                      'proportion_genes_retained_in_major_clades (GUNC)',
                      'genes_retained_index (GUNC)',
                      'clade_separation_score (GUNC)',
                      'contamination_portion (GUNC)',
                      'n_effective_surplus_clades (GUNC)',
                      'mean_hit_identity (GUNC)',
                      'reference_representation_score (GUNC)',
                      'Proportion of bins passing the filter (GUNC)',
    ]
    return names

def labels_GTDB_Tk2 ():
    labels = [ 'Domain',
                   'Phylum',
                   'Class',
                   'Order',
                   'Family',
                   'Genus',
                   'Species'
    ]
    return labels

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
    df = df.replace('','Unclassified')
    df = df.fillna('Unclassified')
    return pd.Series(df[tax_level])

def patch_file(file_path: str, content: bytes, extra: dict = None) -> bytes:
    if file_path == 'bigmag.html':
        index_html_content = content.decode('utf8')
        extra_jsons = f'''
        var patched_jsons_content={{
        {','.join(["'/" + k + "':" + v.decode("utf8") + "" for k, v in extra.items()])}
        }};
        '''
        patched_content = index_html_content.replace(
            '<footer>',
            f'''
            <footer>
            <script>
            ''' + extra_jsons + '''
            const origFetch = window.fetch;
            window.fetch = function () {
                const e = arguments[0]
                if (patched_jsons_content.hasOwnProperty(e)) {
                    return Promise.resolve({
                        json: () => Promise.resolve(patched_jsons_content[e]),
                        headers: new Headers({'content-type': 'application/json'}),
                        status: 200,
                    });
                } else {
                    return origFetch.apply(this, arguments)
                }
            }
            </script>
            '''
        ).replace(
            'href="/',
            'href="'
        ).replace(
            'src="/',
            'src="'
        )
        return patched_content.encode('utf8')
    else:
        return content


class ExternalResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'link':
            for k, v in attrs:
                if k == 'href':
                    self.resources.append(v)
        if tag == 'script':
            for k, v in attrs:
                if k == 'src':
                    self.resources.append(v)
