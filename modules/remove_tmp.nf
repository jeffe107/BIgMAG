process REMOVE_TMP {
	tag "$sample"

	input:
	tuple val(sample), path(files), val(change_dot_for_underscore)
	val "std_output"

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	delete_files.sh "${outdir}/${sample}"
	echo "Temporary files deleted. Your BIgMAG is ready"
	"""
}
