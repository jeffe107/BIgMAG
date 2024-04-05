process QUAST {
	tag "$sample"
        
	input:
	tuple val(sample), path(files)
	val max_reference_number
	val "empty_bins"

	output:
	path "*"

	script:
	def args = task.ext.args ?: ''
	"""
	quast.sh ${files} ${max_reference_number} $task.cpus $args
	"""
}
