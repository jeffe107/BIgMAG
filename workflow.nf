/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT LOCAL MODULES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

//
// MODULE: Local to the pipeline
//
include { BUSCO                 }	from './modules/busco.nf'
include { CHECKM2               }       from './modules/checkm2.nf'
include { CONCAT_DFS            }       from './modules/concat_dfs.nf'
include { DECOMPRESS            }	from './modules/decompress.nf'
include { EMPTY_BINS            }	from './modules/empty_bins.nf'
include { FINAL_DF              }	from './modules/final_df.nf'
include { GTDBTK2               }	from './modules/gtdbtk2.nf'
include { GUNC			}	from './modules/gunc.nf'
include { QUAST                 }       from './modules/quast.nf'

/*
 * workflow
 */

workflow BIgMAGFlow {
		// Input channels
                files_ch = Channel.fromPath( params.files, type: 'dir').map {tuple(it.baseName,it )}
		
		// Workflow including different tools

		decompress_ch = DECOMPRESS(files_ch).collect()
                empty_bins_ch = EMPTY_BINS(files_ch, decompress_ch).collect()
		
		busco_ch = BUSCO(files_ch, empty_bins_ch).collect()
                
                if(params.checkm2_db){
                    checkm2_ch = CHECKM2(files_ch, empty_bins_ch).collect()
                } else {
                    checkm2_ch = []
                }

                if(params.gtdbtk2_db){
                    gtdbtk2_ch = GTDBTK2(files_ch, empty_bins_ch).collect()
                } else {
                    gtdbtk2_ch = []
                }
                           
                if(params.gunc_db){
                    gunc_ch = GUNC(files_ch, empty_bins_ch).collect()
                } else {
                    gunc_ch = []
                }
		
                quast_ch = QUAST(files_ch, params.max_ref_number, empty_bins_ch).collect()

		// Final processing of the outputs
                concat_dfs_ch = CONCAT_DFS(files_ch, checkm2_ch, busco_ch, gunc_ch, quast_ch, gtdbtk2_ch).collect()		
                FINAL_DF(concat_dfs_ch)
}
