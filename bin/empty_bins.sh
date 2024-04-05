#!/bin/bash

files=$1
publish_dir=$2

for file in ${files}/*; do
	if [ -f "$file" ]; then
		if [ ! -s "$file" ]; then
			mkdir -p "${publish_dir}"/empty_bins
			mv "$file" "${publish_dir}/empty_bins"
		fi
        fi
done
