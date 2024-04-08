process BUSCO {
	tag "$sample"

	conda "bioconda::busco=5.7.0"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/busco:5.7.0--pyhdfd78af_1' :
            'quay.io/biocontainers/busco:5.7.0--pyhdfd78af_1' }"
	
	input:
	tuple val(sample), path(files)
	val "change_dots_for_underscore"

	output:
	path "busco"

	script:
	def lineage = params.lineage == 'auto_lineage' ? "--auto-lineage" : "-l ${params.lineage}"
	def args = task.ext.args ?: ''
	"""
	busco -i $files \
        -o busco \
	-m genome -c $task.cpus --force \
	$lineage $args
	"""
}
