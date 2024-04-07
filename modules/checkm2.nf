process CHECKM2 {
	tag "$sample"

        conda "bioconda::checkm2=1.0.1 conda-forge::python=3.7.12"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/checkm2:1.0.1--pyh7cba7a3_0' :
            'quay.io/biocontainers/checkm2:1.0.1--pyh7cba7a3_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	path "checkm2"

	script:
	def args = task.ext.args
        def args2 = task.ext.args2 ?: ''
	"""
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	checkm2 predict \
        --threads $task.cpus \
        --input $files -x \$EXTENSION \
        --output-directory checkm2 \
	$args $args2
	"""
}
