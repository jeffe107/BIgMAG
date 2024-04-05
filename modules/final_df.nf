process FINAL_DF {
	tag "final_df"

	input:
	val "std_outputs"

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	final_df.py "${outdir}/paths.txt" $outdir
	"""
}
