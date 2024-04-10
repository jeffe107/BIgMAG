process QUAST {
	tag "$sample"

	conda "bioconda::quast=5.2.0"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/quast:5.2.0--py38pl5321h5cf8b27_3' :
            'quay.io/biocontainers/quast:5.2.0--py38pl5321h5cf8b27_3' }"

	input:
	tuple val(sample), path(files)
	val "change_dots_for_underscore"
	val "gtdbtk2_db"

	output:
	path "quast"

	script:
	def outdir = params.outdir
	def max_reference = "--max-ref-number ${params.max_ref_number}"
	def min_contig = "--min-contig ${params.min_contig}"
	"""
	quast.sh ${files} $max_reference $min_contig $task.cpus
	software_name="QUAST" && output_file="${outdir}/pipeline_info/versions.txt" \
        && grep -q "\$software_name" "\$output_file" || \
        { quast -v >> "\$output_file"; }
	"""
}
