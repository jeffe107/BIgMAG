process CONCAT_DFS {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "checkm2"
	val "busco"
	val "gunc"
	val "quast"
	val "gtdbtk2"

	output:
	stdout

	script:
	def outdir = params.outdir
	"""
	mkdir -p "${outdir}/${sample}/dfs_concat"
	concat_dfs.py "${outdir}/${sample}" ${sample} "${outdir}"
	"""
}
