process CHECKM2_DB {
	
        conda "bioconda::checkm2=1.0.1 conda-forge::python=3.7.12"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/checkm2:1.0.1--pyh7cba7a3_0' :
            'quay.io/biocontainers/checkm2:1.0.1--pyh7cba7a3_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	val "change_dots_for_underscore"

	output:
	stdout

	script:
	def outdir = params.outdir
	def path_db = "${outdir}/databases/CheckM2_database/uniref100.KO.1.dmnd"
	"""
	[ -f $path_db ] || checkm2_download_db.sh $outdir
	echo "CheckM2 database is ready"
	"""
}
