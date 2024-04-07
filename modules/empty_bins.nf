process EMPTY_BINS {
	tag "$sample"
	
	input:
	tuple val(sample), path(files)
	val "decompress"

	output:
	stdout

	script:
	outdir = "${params.outdir}/$sample"

	"""
	empty_bins.sh ${files} $outdir 
	echo 'files are ready'
	"""
}
