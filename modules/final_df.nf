process FINAL_DF {
	tag "final_df"

        conda "conda-forge::pandas=2.2.1"
	container "${ params.use_singularity ?
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
	[ -f "${outdir}/paths.txt" ] && rm -r "${outdir}/paths.txt"
	echo -n "pandas: " >> ${outdir}/pipeline_info/versions.txt
	pandas_version.py >> ${outdir}/pipeline_info/versions.txt
	sort ${outdir}/pipeline_info/versions.txt | uniq > ${outdir}/pipeline_info/version.txt
	[ -f "${outdir}/pipeline_info/versions.txt" ] && rm -r "${outdir}/pipeline_info/versions.txt"
	echo "Final DF is ready"
	"""
}
