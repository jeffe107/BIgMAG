process QUAST {
	tag "$sample"

	conda "bioconda::quast=5.2.0"
	container "${ params.use_singularity == 'yes' ?
            'https://depot.galaxyproject.org/singularity/quast:5.2.0--py38pl5321h5cf8b27_3' :
            'quay.io/biocontainers/quast:5.2.0--py38pl5321h5cf8b27_3' }"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "*"

	script:
	def args = task.ext.args
	"""
	quast.sh ${files} $args $task.cpus
	"""
}
