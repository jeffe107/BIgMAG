process GUNC {
	tag "$sample"
	errorStrategy 'ignore'

	conda "bioconda::gunc=1.0.6"
	container "${ params.use_singularity ?
            'https://depot.galaxyproject.org/singularity/gunc:1.0.6--pyhdfd78af_0' :
            'quay.io/biocontainers/gunc:1.0.6--pyhdfd78af_0' }"
	containerOptions "${ params.directory_to_bind == null ? '' : "--bind ${params.directory_to_bind}" }"

	input:
	tuple val(sample), path(files), val(change_dot_for_underscore)
	val "gunc_db"
	val "gtdbtk2_db"

	output:		
	path "gunc/GUNC.progenomes_2.1.maxCSS_level.tsv", optional: true

	script:
	def outdir = params.outdir
	def gunc_db = params.gunc_db ?
				"-r ${params.gunc_db}" :
				"-r ${outdir}/databases/GUNC_db/gunc_db_progenomes2.1.dmnd"
	def args = task.ext.args ?: ''
	"""
	mkdir gunc
	EXTENSION=\$(echo ".\$(ls ${files}/* | head -n 1 | rev | cut -d. -f1 | rev)")
	gunc run -d ${files} \
	-o gunc \
	--threads $task.cpus \
	--file_suffix \$EXTENSION \
	$gunc_db $args
	software_name="GUNC" && output_file="${outdir}/pipeline_info/versions.txt" \
        && grep -q "\$software_name" "\$output_file" || \
        { echo -n "\$software_name Version: " >> "\$output_file" && gunc -v >> "\$output_file"; }
	"""
}
