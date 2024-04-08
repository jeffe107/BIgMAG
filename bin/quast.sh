#!/bin/bash

files=$1
max_r_n_flag=$2
max_r_n_value=$3
min_contig_flag=$4
min_contig_value=$5
cpus=$6

file_array=()
for file in ${files}/*; do
	if [ -f "$file" ]; then
		if [ -s "$file" ]; then
        		file_array+=("$file")
		fi
        fi
done

metaquast ${file_array[*]} \
	-o quast \
	"${max_r_n_flag}" "${max_r_n_value}" \
	"${min_contig_flag}" "${min_contig_value}" \
	-t "$cpus"
