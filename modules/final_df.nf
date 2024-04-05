process FINAL_DF {
	tag "final_df"

        conda "conda-forge::pandas=2.2.1"
	container "${ params.use_singularity == 'yes' ?
            'https://depot.galaxyproject.org/singularity/pandas:1.5.2' :
            'quay.io/biocontainers/bioframe:0.6.2--pyhdfd78af_0' }"

	input:
	val "std_outputs"

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	final_df.py "${outdir}/paths.txt" $outdir
	rm "${outdir}/paths.txt"
	"""
}
