#!/usr/bin/env python3

import sys
import pandas as pd

txt_file = sys.argv[1]
publish_dir = sys.argv[2]

file = open(txt_file, 'r')
lines = file.read().splitlines()

dfs_list = [pd.read_csv(line, sep='\t') for line in lines]

final_df = pd.DataFrame()
for df in dfs_list:
    final_df = pd.concat([final_df, df], axis=0, ignore_index=True)

first_column = final_df.pop('sample')
final_df.insert(0,'sample',first_column)
final_df = final_df.sort_values(['sample', 'Bin'])
final_df = final_df.reset_index(drop=True)

final_df.to_csv(f"{publish_dir}/final_df.tsv", sep="\t")
print(f"BIgMAG is ready", file=sys.stdout)
