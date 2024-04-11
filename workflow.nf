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
include { GTDBTK2                       }	from './modules/gtdbtk2.nf'
include { GTDBTK2_DB			}	from './modules/gtdbtk2_db.nf'
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
				
		decompress_ch = DECOMPRESS(files_ch)
                empty_bins_ch = EMPTY_BINS(decompress_ch)
		change_dot_for_underscore_ch = CHANGE_DOT_FOR_UNDERSCORE(empty_bins_ch)	

		if(params.run_gtdbtk2){
                    gtdbtk2_db_ch = GTDBTK2_DB()
                } else {
                    gtdbtk2_db_ch = []
                }

		busco_ch = BUSCO(change_dot_for_underscore_ch, gtdbtk2_db_ch).collect()
                
                if(!params.checkm2_db){
                    checkm2_db_ch = CHECKM2_DB()
                } else {
                    checkm2_db_ch = []
                }

		checkm2_ch = CHECKM2(change_dot_for_underscore_ch, checkm2_db_ch, gtdbtk2_db_ch).collect()

                if(params.gtdbtk2_db || params.run_gtdbtk2){
                    gtdbtk2_ch = GTDBTK2(change_dot_for_underscore_ch, gtdbtk2_db_ch).collect()
                } else {
                    gtdbtk2_ch = []
                }
                           
                if(!params.gunc_db){
                    gunc_db_ch = GUNC_DB()
                } else {
                    gunc_db_ch = []
                }

                gunc_ch = GUNC(change_dot_for_underscore_ch, gunc_db_ch, gtdbtk2_db_ch).collect()
		
                quast_ch = QUAST(change_dot_for_underscore_ch, gtdbtk2_db_ch).collect()

		// Final processing of the outputs
                concat_dfs_ch = CONCAT_DFS(change_dot_for_underscore_ch, checkm2_ch, busco_ch, gunc_ch, quast_ch, gtdbtk2_ch).collect()
                final_df_ch = FINAL_DF(concat_dfs_ch)
                REMOVE_TMP(change_dot_for_underscore_ch, final_df_ch)
}
