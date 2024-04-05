process GUNC {
	tag "$sample"
	errorStrategy 'ignore'

	conda "bioconda::gunc=1.0.6"
	container "${ params.use_singularity == 'yes' ?
            'https://depot.galaxyproject.org/singularity/gunc:1.0.6--pyhdfd78af_0' :
            'quay.io/biocontainers/gunc:1.0.6--pyhdfd78af_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:		
	path "gunc/GUNC.progenomes_2.1.maxCSS_level.tsv", optional: true

	script:
	def args = task.ext.args
	def args2 = task.ext.args2 ?: ''
	"""
	mkdir gunc
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	gunc run -d ${files} \
	-o gunc \
	--threads $task.cpus \
	--file_suffix \$EXTENSION \
	$args $args2
	"""
}
