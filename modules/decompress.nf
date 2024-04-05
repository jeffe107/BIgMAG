process DECOMPRESS {
	tag "$sample"
	publishDir "${params.outdir}/$sample", mode:'copy'

	input:
	tuple val(sample), path(files)

	output:
	stdout

	script:
	"""
	if ls ${files}/*.gz; then gzip -d ${files}/*.gz; fi
	echo 'files are ready'
	"""
}
