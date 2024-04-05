#!/bin/bash

files=$1
max_reference_number=$2
cpus=$3
additional_params=$4

file_array=()
for file in ${files}/*; do
	if [ -f "$file" ]; then
		if [ -s "$file" ]; then
        		file_array+=("$file")
		fi
        fi
done

if [ -n "$additional_params" ]; then
	metaquast ${file_array[*]} \
	-o quast \
	-t "$cpus" --max-ref-number "$max_reference_number" \
	"$additional_params"
else
	metaquast ${file_array[*]} \
       	-o quast \
       	-t "$cpus" --max-ref-number "$max_reference_number"
fi
