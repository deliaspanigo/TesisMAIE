## Cargar el entorno de python
# source tesis_v004/bin/activate

## Desactivar el entorno de python
# deactivate


# Librerias
import sys
import os
import time

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)

# Common resources
import fn02_time as fn02

# Especial functions
import fn076_01_goes16_spi076_MCMIPF_download as fn076_01
import fn076_02_goes16_spi076_MCMIPF_convert_nc2tiff as fn076_02

import fn076_03_goes16_spi076_MCMIPF_ppi001_convert_nc2png_v001_OrigProj_RGB as fn076_03_ppi001
import fn076_03_goes16_spi076_MCMIPF_ppi002_convert_nc2png_v002_OrigProj_RGB  as fn076_03_ppi002
import fn076_03_goes16_spi076_MCMIPF_ppi003_convert_nc2png_v003_OrigProj_RGB   as fn076_03_ppi003
import fn076_03_goes16_spi076_MCMIPF_ppi004_convert_tiff2png_v001_WGS84Proj_RGB   as fn076_03_ppi004
import fn076_03_goes16_spi076_MCMIPF_ppi005_convert_tiff2png_v002_WGS84Proj_RGB  as fn076_03_ppi005
import fn076_03_goes16_spi076_MCMIPF_ppi006_convert_tiff2png_v003_WGS84Proj_RGB  as fn076_03_ppi006
import fn076_03_goes16_spi076_MCMIPF_ppi007_convert_tiff2png_v004_WGS84Proj_RGB  as fn076_03_ppi007

import fn076_04_goes16_spi076_MCMIPF_convert_png2mp4 as fn076_04



# 5 minutos 30 - Version special_prod = False
# input: 24 .nc
# output: 
# 24 x 1 =  24 tiff
# 24 x 7 = 168 png
#  1 x 7 =   7 mp4
def PROCESS_goes16_spi076_MCMIPF_gen02Full_OneDay_HardCoded(gregorian_date, special_prod = False):


    print("PROCESS_goes16_spi076_MCMIPF_gen02Full_OneDay_HardCoded()")
    print(f"Gregorian Date:{gregorian_date}")

    # 1) Download
    # No lo realizamos aqui.
    
    # 2) Convert - nc2tiff
    if True:
        fn076_02.convert_nc2tiff_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
    
    if False:
        if True:    # Solo FullDisk
            fn076_03_ppi001.convert_goes16_spi076_ppi001_gen02_OneDay_HardCoded(gregorian_date)
            print("\n")
            
        if True:    # Solo FullDisk
            fn076_03_ppi002.convert_goes16_spi076_ppi002_gen02_OneDay_HardCoded(gregorian_date)
            print("\n")
            
        if True:    # Solo FullDisk
            fn076_03_ppi003.convert_goes16_spi076_ppi003_gen02_OneDay_HardCoded(gregorian_date)
            print("\n")
            
        if True:    # Solo FullDisk
            fn076_03_ppi004.convert_goes16_spi076_ppi004_gen02_OneDay_HardCoded(gregorian_date, key_png_setup = "dom002")
            print("\n")
                            
        if True:    # Solo FullDisk
            fn076_03_ppi005.convert_goes16_spi076_ppi005_gen02_OneDay_HardCoded(gregorian_date, key_png_setup = "dom002")
            print("\n")    
            
        if True:    # Solo FullDisk
            fn076_03_ppi006.convert_goes16_spi076_ppi006_gen02_OneDay_HardCoded(gregorian_date, key_png_setup = "dom002")
            print("\n")    
            
        if True:    # Solo FullDisk
            fn076_03_ppi007.convert_goes16_spi076_ppi007_gen02_OneDay_HardCoded(gregorian_date, key_png_setup = "dom002")
            print("\n")    
        
        # if special_prod:    
        #     fn076_03_ppi010.convert_goes16_spi067_ppi010_gen02_OneDay_HardCoded(gregorian_date)

        # if special_prod:    
        #     fn076_03_ppi011.convert_goes16_spi067_ppi011_gen02_OneDay_HardCoded(gregorian_date)
            
        
        # 4) png2mp4 - OneDay
        if True:
            fn076_04.cconvert_png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date)
            print("\n")
        
    
        
        

    print("Close: PROCESS_goes16_spi076_MCMIPF_gen02Full_OneDay_HardCoded()")
    
    return
    




def PROCESS_goes16_spi076_MCMIPF_genMIX_OneDay_HardCoded(gregorian_date, special_prod = False):


    print("PROCESS_goes16_spi076_MCMIPF_gen02Full_OneDay_HardCoded()")
    print(f"Gregorian Date:{gregorian_date}")

    # 1) Download
    # No lo realizamos aqui.
    
    # 2) Convert - nc2tiff
    if True:
        fn076_02.convert_nc2tiff_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
    
    
    if True:    # Solo FullDisk
        fn076_03_ppi001.convert_goes16_spi076_ppi001_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
        
    if True:    # Solo FullDisk
        fn076_03_ppi002.convert_goes16_spi076_ppi002_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
        
    if True:    # Solo FullDisk
        fn076_03_ppi003.convert_goes16_spi076_ppi003_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
        
    if True:    # Solo FullDisk
        fn076_03_ppi004.convert_goes16_spi076_ppi004_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
                        
    if True:    # Solo FullDisk
        fn076_03_ppi005.convert_goes16_spi076_ppi005_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")    
        
    if True:    # Solo FullDisk
        fn076_03_ppi006.convert_goes16_spi076_ppi006_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")    
        
    if True:    # Solo FullDisk
        fn076_03_ppi007.convert_goes16_spi076_ppi007_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")    
    
    
    # 4) png2mp4 - OneDay
    if True:
        fn076_04.convert_png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date)
        print("\n")
    
    
        
        

    print("Close: PROCESS_goes16_spi076_MCMIPF_gen02Full_OneDay_HardCoded()")
    
    return
    
