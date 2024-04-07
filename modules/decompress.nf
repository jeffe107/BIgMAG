process DECOMPRESS {
	tag "$sample"

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
