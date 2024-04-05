process EMPTY_BINS {
	tag "$sample"
	publishDir "${params.outdir}/$sample", mode:'copy'
	
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
