#!/usr/bin/env python3

import sys
import pandas as pd
import os.path

files = sys.argv[1]
sample = sys.argv[2]
outdir = sys.argv[3]

path_checkm2 = f"{files}/checkm2/quality_report.tsv"
if  os.path.isfile(path_checkm2):
     df_checkm2 = pd.read_table(f"{files}/checkm2/quality_report.tsv", sep="\t").sort_values(['Name'])
     df_checkm2 = df_checkm2.reset_index(drop=True)
else:
     df_checkm2 = pd.DataFrame()

path_gunc = f"{files}/gunc/GUNC.progenomes_2.1.maxCSS_level.tsv"
if os.path.isfile(path_gunc):
    df_gunc = pd.read_table(f"{files}/gunc/GUNC.progenomes_2.1.maxCSS_level.tsv", sep="\t").sort_values(['genome'])
    df_gunc = df_gunc.drop(columns=['genome'])
    df_gunc = df_gunc.reset_index(drop=True)
else:
    df_gunc = pd.DataFrame()

df_gtdbtk2 = pd.DataFrame()
path_gtdbtk2_bac = f"{files}/gtdbtk2/gtdbtk.bac120.summary.tsv"
if os.path.isfile(path_gtdbtk2_bac):
    df_gtdbtk2_bac = pd.read_table(f"{files}/gtdbtk2/gtdbtk.bac120.summary.tsv")
    df_gtdbtk2 = pd.concat([df_gtdbtk2, df_gtdbtk2_bac], axis=0)

path_gtdbtk2_ar = f"{files}/gtdbtk2/gtdbtk.ar53.summary.tsv"
if os.path.isfile(path_gtdbtk2_ar):
    df_gtdbtk2_ar = pd.read_csv(path_gtdbtk2_ar, sep="\t")
    df_gtdbtk2 = pd.concat([df_gtdbtk2, df_gtdbtk2_ar], axis=0)

if len(df_gtdbtk2) > 0:
    df_gtdbtk2 = df_gtdbtk2_bac.sort_values(['user_genome'])
    df_gtdbtk2 = df_gtdbtk2_bac.drop(columns=['user_genome'])
    df_gtdbtk2 = df_gtdbtk2_bac.reset_index(drop=True)

df_busco = pd.read_table(f"{files}/busco/batch_summary.txt", sep="\t").sort_values(['Input_file'])
df_busco = df_busco.drop(columns=['Input_file'])
df_busco = df_busco.reset_index(drop=True)

df_quast = pd.read_table(f"{files}/quast/transposed_report.tsv", sep="\t").sort_values(['Assembly'])
df_quast = df_quast.drop(columns=['Assembly'])
df_quast = df_quast.reset_index(drop=True)

df_concat = pd.concat([df_checkm2,df_busco,df_gunc,df_gtdbtk2, df_quast], axis=1)
df_concat['sample'] = [sample] * len(df_concat)
df_concat.to_csv(f"{files}/dfs_concat/dfs.tsv", sep="\t")

file_path = f"{outdir}/paths.txt"
paths = open(file_path, "a")
paths.write(f"{files}/dfs_concat/dfs.tsv" + '\n')
paths.close()

print(f"{sample} ready", file=sys.stdout)
