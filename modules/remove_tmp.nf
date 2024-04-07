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
	[ -f "${outdir}/paths.txt" ] && rm -r "${outdir}/paths.txt"
	[ -d "${outdir}/${sample}/tmp" ] && rm -r "${outdir}/${sample}/tmp"
	echo "Temporary files deleted. Your BIgMAG is ready"
	"""
}
