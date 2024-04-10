process DECOMPRESS {
	tag "$sample"

	input:
	tuple val(sample), path(files)

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	if ls ${files}/*.gz; then gzip -d ${files}/*.gz; fi
	touch ${outdir}/pipeline_info/versions.txt
	echo 'files are ready'
	"""
}
