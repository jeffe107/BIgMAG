process BUSCO {
	tag "$sample"

	conda "bioconda::busco=5.7.0"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/busco:5.7.0--pyhdfd78af_1' :
            'quay.io/biocontainers/busco:5.7.0--pyhdfd78af_1' }"
	
	input:
	tuple val(sample), path(files)
	val "change_dots_for_underscore"
	val "gtdbtk2_db"

	output:
	path "busco"

	script:
	def outdir = params.outdir
	def lineage = params.lineage == 'auto_lineage' ? "--auto-lineage" : "-l ${params.lineage}"
	def args = task.ext.args ?: ''
	"""
	busco -i $files \
        -o busco \
	-m genome -c $task.cpus --force \
	$lineage $args
	software_name="BUSCO" && output_file="${outdir}/pipeline_info/versions.txt" \
        && grep -q "\$software_name" "\$output_file" || \
        { busco -v >> "\$output_file"; }
	"""
}
