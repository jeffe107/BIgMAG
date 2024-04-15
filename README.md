
# BIgMAG
<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/BIGMAG.png">
    <img alt="nf-core/mag" src="assets/BIGMAG.png">
  </picture>
</h1>

BIgMAG (Board InteGrating Metagenome-Assembled Genomes) is both a pipeline to measure the quality of metagenomes and dashboard to visualize the results.

[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A521.10.3-23aa62.svg?labelColor=000000)](https://www.nextflow.io/)

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)

[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)

[![run with singularity](https://img.shields.io/badge/run%20with-singularity-1d355c.svg?labelColor=000000)](https://sylabs.io/docs/)

[![Static Badge](https://img.shields.io/badge/developed_with-_plotly-lightblue?style=flat&logo=plotly&logoColor=lightblue&labelColor=black)](https://plotly.com/)


## Installation

The pipeline runs under Nextflow DSL2, you can check how to install Nextflow [here](https://www.nextflow.io/docs/latest/install.html). Please notice that you need to have Java JDK (recommended version 17.0.3) available to be able to install Nextflow. 

To install BIgMAG, you just need to copy this repository:
```bash
 git clone https://github.com/jeffe107/BIgMAG.git 
```
On the other hand, you need Conda or Mamba (recommended versions 23.3.1 and 1.3.1) or [pip](https://pip.pypa.io/en/stable/installation/) in your system to display the dashboard. Create the environment or install the components with:
```bash
 pip install -r requirements.txt 
```
or
```bash
 conda create -n BIgMAG --file requirements.txt
 conda activate BIgMAG
```
## Pipeline summary

BIgMAG receives folders containing bins or MAGs in any format (.fna, .fa, .fasta) decompressed or compressed (.gz) in the following file structure:
```bash
.
└── samples/
    ├── sample1/
    │   ├── bin1
    │   ├── bin2
    │   └── ...
    ├── sample2/
    │   ├── bin1
    │   ├── bin2
    │   ├── bin3
    │   └── ... 
    └── ...
```
In addition, you can provide a .csv file with the names of the samples and the paths:

| sampleID      | files            |
| ------------- | ---------------- |
| sample1       | path/to/sample1  |
| sample2       | path/to/sample2  |
| ...           | ...              |

Please check in the Usage section to see how to input or another.

By default, the Nextflow pipeline currently attempts to analyze bins or MAGs through the following:

- examines completeness and contamination with [CheckM2](https://github.com/chklovski/CheckM2) v1.0.1 and [BUSCO](https://busco.ezlab.org/busco_userguide.html) v5.7.0.
- determines different metrics and statistics using [QUAST](https://quast.sourceforge.net/) v5.2.0.
- detects chimerism and contamination by running [GUNC](https://github.com/grp-bork/gunc) v1.0.6.
- optionally assigns taxonomy to bins using [GTDB-Tk2](https://ecogenomics.github.io/GTDBTk/index.html) v2.3.2.

Finally, a file final_df.tsv will be generated and used to display the dashboard using [Dash and Plotly](https://dash.plotly.com/).

## Pipeline Usage
The basic usage of the pipeline can be achieved by running: 

If you want to test the proper behaviour of the pipeline you can just run:
```bash
 nextflow run BIgMAG/main.nf -profile test,<docker/singularity/podman/shifter/charliecloud/conda/mamba> --outdir <OUTDIR>
```
To run the pipeline with the default workflow:
```bash
 nextflow run BIgMAG/main.nf -profile <docker/singularity/podman/shifter/charliecloud/conda/mamba> --files 'path/to/the/samples/*' --outdir <OUTDIR>
```
In case you wish to input a csv file with the details of your samples, you can change the flag --files for `--files` for `--csv_files 'path/to/your/csv_files'`.
### Databases
Running the pipeline in its default state will attempt to download automaically CheckM2 (~3.5 GB) and GUNC (~12 GB) in your specified output directory. Please make sure you have enough space to store these databases. Moreover, if you have customized or different versions you would like to use, you can use these flags to include them `--gunc_db '/path/to/your/gunc_db.dmnd'` and `--checkm2_db '/path/to/your/checkm2_db.dmnd'`.

In the case of the database required by GTDB-Tk2, BIgMAG does not download by default given its large required space (~85 GB); however if you include the flag `--run_gtdbtk2` to both automatically download the database and run the analysis. As for CheckM2 and GUNC, you can input your own version of the database with `gtdbtk2_db '/pathto/to/your/gtdbtk/release*'`
> [!WARNING]
> Notice that when you untar any GTDB dabatase, its named release*; please keep the word release in the name to guarantee a proper detection by the pipeline.
### Profiles
The pipeline can use different techonologies to run the required software. The available profiles are:
- docker
- singularity
- podman 
- shifter 
- charliecloud
- conda
- mamba
- apptainer

Please select one of these considering your system configuration. Natively, the pipeline will use docker container from [quay.io](https://quay.io/)
> [!WARNING]
> If you are using profiles such as singularity or apptainer, please always include the flag `--singularity_container` during your execution. This will allow to pull containers from [Galaxy project](https://depot.galaxyproject.org/singularity/).

Furthermore, if the execution of the pipeline fails while using profiles that require to mount directories, i.e. apptainer, throwing an error related with problems to find any file you can attempt to solve this by including the flag `--directory_to_bind 'path/to/the/directory'`.

Finally, when using mamba or conda as profiles, you may want to make sure you have only bioconda, conda-forge and defaults as available channels, in that order.

Permalink to reference line of code:
https://github.com/jeffe107/BIgMAG/blob/a7c4247ab63905452b64d82fc4c6264d9bb3e711/nextflow.config#L50
