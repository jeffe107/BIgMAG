process CHECKM2 {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "checkm2"

	script:
	def args = task.ext.args
	"""
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	checkm2 predict \
        --threads $task.cpus \
        --input $files -x \$EXTENSION \
        --output-directory checkm2 \
	$args
	"""
}
