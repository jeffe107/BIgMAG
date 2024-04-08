#!/bin/bash

directory=$1

mkdir -p "${directory}/databases" && cd "${directory}/databases"
wget https://zenodo.org/record/5571251/files/checkm2_database.tar.gz
tar xvzf checkm2_database.tar.gz
rm checkm2_database.tar.gz
rm CONTENTS.json
