process GTDBTK2 {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "gtdbtk2"

	script:
	def args = task.ext.args
	def gtdbtk2_db = params.gtdbtk2_db
	"""
	EXTENSION=\$(echo "\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	export GTDBTK_DATA_PATH=$gtdbtk2_db
	gtdbtk classify_wf \
	--genome_dir $files \
	-x \$EXTENSION \
	--out_dir gtdbtk2 --cpus $task.cpus \
	$args
	"""
}
