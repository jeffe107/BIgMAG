process GTDBTK2 {
	tag "$sample"

	conda "bioconda::gtdbtk=2.3.2"
        container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/gtdbtk:2.3.2--pyhdfd78af_0' :
            'quay.io/biocontainers/gtdbtk:2.3.2--pyhdfd78af_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files), val(change_dot_for_underscore)
	val "gtdbtk2_db"

	output:
	path "gtdbtk2"

	script:
	def outdir = params.outdir
	def mash_db = "${outdir}/databases/mash_db"
	def gtdbtk2_db = params.gtdbtk2_db ?
				params.gtdbtk2_db :
				"${outdir}/databases/gtdbtk2"

	def args = task.ext.args ?: ''
	"""
	mkdir -p $mash_db
	EXTENSION=\$(echo "\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	release="release"; if echo "$gtdbtk2_db" | grep -q -E "\$release"; \
	then version=""; else version=\$(ls "$gtdbtk2_db"); fi
	export GTDBTK_DATA_PATH="$gtdbtk2_db/\$version"
	gtdbtk classify_wf \
	--genome_dir $files \
	-x \$EXTENSION \
	--out_dir gtdbtk2 --cpus $task.cpus \
	--mash_db $mash_db \
	$args
	software_name="gtdbtk" && output_file="${outdir}/pipeline_info/versions.txt" \
        && grep -q "\$software_name" "\$output_file" || \
        { gtdbtk -v >> "\$output_file"; }
	"""
}
