# Own libreries
import os
import fn01_generic as fn01
import fn02_time as fn02


# # # Libreries
# Libreries


def hard_setup_00_general_folders():
    pdict = {
    "download": '02.download_goes16_OrigProj_nc_files',
    "nc2tiff": '03.geot_goes16_wgs84Proj_tiff_files',
    "png": '04.png',
    "mp4_oneday": "05.mp4_OneDay"
    }
    
    
    for x in pdict:
        fn01.create_folder_if_not_exists(pdict[x])
    
        
    return pdict

    

