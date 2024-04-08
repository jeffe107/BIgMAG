#!/bin/bash

directory=$1

mkdir -p "${directory}/databases/GUNC_db"
gunc download_db "${directory}/databases/GUNC_db"
