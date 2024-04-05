process GUNC {
	tag "$sample"
	errorStrategy 'ignore'

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:		
	path "gunc/GUNC.progenomes_2.1.maxCSS_level.tsv", optional: true

	script:
	def args = task.ext.args
	"""
	mkdir gunc
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	gunc run -d ${files} \
	-o gunc \
	--threads $task.cpus \
	--file_suffix \$EXTENSION \
	$args
	"""
}
