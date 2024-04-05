process BUSCO {
	tag "$sample"

	conda "bioconda::busco=5.7.0"
	container "${ params.use_singularity == 'yes' ?
            'https://depot.galaxyproject.org/singularity/busco:5.7.0--pyhdfd78af_1' :
            'quay.io/biocontainers/busco:5.7.0--pyhdfd78af_1' }"
	
	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "busco"

	script:
	def args = task.ext.args
	def args2 = task.ext.args2 ?: ''
	"""
	busco -i $files \
        -o busco \
	-m genome -c $task.cpus --force \
	$args $args2
	"""
}
