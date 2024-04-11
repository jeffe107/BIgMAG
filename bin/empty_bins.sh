#!/bin/bash

files=$1
publish_dir=$2
sample=$3

for file in ${files}/*; do
	if [ -f "$file" ]; then
		if [ ! -s "$file" ]; then
			mkdir -p "${publish_dir}/${sample}/empty_bins"
			mv "$file" "${publish_dir}/${sample}/empty_bins"
		fi
        fi
done
