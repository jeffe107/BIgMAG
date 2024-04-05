process BUSCO {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "busco"

	script:
	def args = task.ext.args ?: params.busco_options
	"""
	busco -i $files \
        -o busco \
	-m genome -c $task.cpus --force \
	$args
	"""
}
