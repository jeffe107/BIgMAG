process CHANGE_DOT_FOR_UNDERSCORE {
	tag "$sample"

	input:
	tuple val(sample), path(files)
	val "empty_bins"

	output:
	stdout

	script:
	"""
	change_dot_for_underscore.sh ${files}
	echo 'files are ready'
	"""
}
