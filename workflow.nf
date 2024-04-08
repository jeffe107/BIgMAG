/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT LOCAL MODULES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

//
// MODULE: Local to the pipeline
//
include { BUSCO				}	from './modules/busco.nf'
include { CHANGE_DOT_FOR_UNDERSCORE	}	from './modules/change_dot_for_underscore.nf'
include { CHECKM2			}	from './modules/checkm2.nf'
include { CHECKM2_DB			}	from './modules/checkm2_db.nf'
include { CONCAT_DFS			}	from './modules/concat_dfs.nf'
include { DECOMPRESS			}	from './modules/decompress.nf'
include { EMPTY_BINS			}	from './modules/empty_bins.nf'
include { FINAL_DF			}	from './modules/final_df.nf'
include { GTDBTK2			}	from './modules/gtdbtk2.nf'
include { GUNC				}	from './modules/gunc.nf'
include { GUNC_DB			}	from './modules/gunc_db'
include { QUAST				}	from './modules/quast.nf'
include { REMOVE_TMP			}	from './modules/remove_tmp.nf'

/*
 * workflow
 */

workflow BIgMAGFlow {
		// Input channels
                files_ch = Channel.fromPath( params.files, type: 'dir').map {tuple(it.baseName,it )}
		
		// Workflow including different tools

		decompress_ch = DECOMPRESS(files_ch).collect()
                empty_bins_ch = EMPTY_BINS(files_ch, decompress_ch).collect()
		change_dot_for_underscore_ch = CHANGE_DOT_FOR_UNDERSCORE(files_ch, empty_bins_ch).collect()	

		busco_ch = BUSCO(files_ch, change_dot_for_underscore_ch).collect()
                
                if(!params.checkm2_db){
                    checkm2_db_ch = CHECKM2_DB(change_dot_for_underscore_ch)
                } else {
                    checkm2_db_ch = []
                }

		checkm2_ch = CHECKM2(files_ch, checkm2_db_ch).collect()

                if(params.gtdbtk2_db){
                    gtdbtk2_ch = GTDBTK2(files_ch, change_dot_for_underscore_ch).collect()
                } else {
                    gtdbtk2_ch = []
                }
                           
                if(!params.gunc_db){
                    gunc_db_ch = GUNC_DB(change_dot_for_underscore_ch)
                } else {
                    gunc_db_ch = []
                }

                gunc_ch = GUNC(files_ch, gunc_db_ch).collect()
		
                quast_ch = QUAST(files_ch, change_dot_for_underscore_ch).collect()

		// Final processing of the outputs
                concat_dfs_ch = CONCAT_DFS(files_ch, checkm2_ch, busco_ch, gunc_ch, quast_ch, gtdbtk2_ch).collect()
                final_df_ch = FINAL_DF(concat_dfs_ch)
                REMOVE_TMP(files_ch, final_df_ch)
}
