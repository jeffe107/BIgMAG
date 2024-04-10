process REMOVE_TMP {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "std_output"

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	[ -d "${outdir}/${sample}/tmp" ] && rm -r "${outdir}/${sample}/tmp"
	[ -d "${outdir}/${sample}/dfs_concat" ] && rm -r "${outdir}/${sample}/dfs_concat"
	echo "Temporary files deleted. Your BIgMAG is ready"
	"""
}
