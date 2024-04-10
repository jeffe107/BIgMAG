#!/bin/bash

directory=$1

mkdir -p "${directory}/databases/gtdbtk2" && cd "${directory}/databases/gtdbtk2"
wget https://data.gtdb.ecogenomic.org/releases/latest/auxillary_files/gtdbtk_data.tar.gz
tar xvzf gtdbtk_data.tar.gz
rm gtdbtk_data.tar.gz
