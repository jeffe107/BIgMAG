process GTDBTK2 {
	tag "$sample"

	conda "bioconda::gtdbtk=2.3.2"
        container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/gtdbtk:2.3.2--pyhdfd78af_0' :
            'quay.io/biocontainers/gtdbtk:2.3.2--pyhdfd78af_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files)
	val "change_dots_for_underscore"

	output:
	path "gtdbtk2"

	script:
	def gtdbtk2_db = params.gtdbtk2_db
	def mash_db = "--mash_db ${params.outdir}/databases/gtdbtk2/mash_db"
	def args = task.ext.args2 ?: ''
	"""
	mkdir -p "${params.outdir}/databases/gtdbtk2/mash_db"
	EXTENSION=\$(echo "\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	export GTDBTK_DATA_PATH=$gtdbtk2_db
	gtdbtk classify_wf \
	--genome_dir $files \
	-x \$EXTENSION \
	--out_dir gtdbtk2 --cpus $task.cpus \
	$mash_db $args
	"""
}
