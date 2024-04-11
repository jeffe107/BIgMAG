process CHECKM2 {
	tag "$sample"

        conda "bioconda::checkm2=1.0.1 conda-forge::python=3.7.12"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/checkm2:1.0.1--pyh7cba7a3_0' :
            'quay.io/biocontainers/checkm2:1.0.1--pyh7cba7a3_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files), val(change_dot_for_underscore)
	val "checkm2_db"
	val "gtdbtk2_db"

	output:
	path "checkm2"

	script:
	def outdir = params.outdir
	def checkm2_db = params.checkm2_db ? 
				"--database_path ${params.checkm2_db}" :
				"--database_path ${params.outdir}/databases/CheckM2_database/uniref100.KO.1.dmnd"
	def args = task.ext.args ?: ''
	"""
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	checkm2 predict \
        --threads $task.cpus \
        --input $files -x \$EXTENSION \
        --output-directory checkm2 \
	$checkm2_db $args
	software_name="CheckM2" && output_file="${outdir}/pipeline_info/versions.txt" \
	&& grep -q "\$software_name" "\$output_file" || \
	{ echo -n "\$software_name Version: " >> "\$output_file" && checkm2 --version >> "\$output_file"; }
	"""
}
