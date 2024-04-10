process GTDBTK2_DB {
	
	conda "bioconda::gtdbtk=2.3.2"
        container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/gtdbtk:2.3.2--pyhdfd78af_0' :
            'quay.io/biocontainers/gtdbtk:2.3.2--pyhdfd78af_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"        

	input:
	val "change_dots_for_underscore"

	output:
	stdout

	script:
	def outdir = params.outdir
	def path_db = "${outdir}/databases/gtdbtk2"
	"""
	[ ! -d $path_db/*/ ] && gtdbtk2_download_db.sh $outdir
	echo "GTDB-Tk2 database is ready"
	"""
}
