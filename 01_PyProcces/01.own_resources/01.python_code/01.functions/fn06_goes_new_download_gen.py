# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # functions03_goes_download.py
# Funciones en relacion a:
# - gen00: simple download without function
# - gen01: gen00 inside as a function
# - gen02: gen01 + subfolder creation


# Own libreries
import fn01_generic as fn01
import fn02_time as fn02


# # # Libreries
# Libreries
import os
import GOES

info_goes_product_names = ['ABI-L2-ACMF', 'ABI-L2-FDCC', 
                           'ABI-L2-FDCF', 'ABI-L2-LSTF', 'GLM-L2-LCFA']














# # # GOES functions -------------------------------------------------------------------

def download_goes16_gen01(product, gregorian_date, output_folder, time_init = "000000", time_fin = "235959"):
    
    datetimeini = str(gregorian_date) + str("-") + str(time_init)
    datetimefin = str(gregorian_date) + str("-") + str(time_fin)
        
   
    GOES.download(Satellite = 'goes16', Product = product,
                DateTimeIni = datetimeini, DateTimeFin = datetimefin, 
                rename_fmt = '%Y%m%d%H%M%S',
                path_out = output_folder, 
                retries = 10,
                backoff = 10,
                size_format = 'Decimal',
                show_download_progress = True,
                overwrite_file = False)
    
    return



def download_goes16_gen02(product, gregorian_date, general_output_folder,  time_init = "000000", time_fin = "235959"):
    new_folder = fn02.gregorianCOMP_to_newsubfolder(gregorian_date_str = gregorian_date)
    output_folder = general_output_folder + product + "/" + new_folder
    fn01.create_folder_if_not_exists(output_folder)
    
    print(f'Output folder: {output_folder}')
    
    # Download goes 16 example - gen01
    download_goes16_gen01(product = product, 
                               gregorian_date = gregorian_date, 
                               output_folder = output_folder, 
                               time_init = time_init,
                               time_fin = time_fin)
    
    
    return

##################################################################################################

