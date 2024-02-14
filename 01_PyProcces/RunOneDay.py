
# conda activate PyProcces

# Librerias
import sys
import os

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fnD_01_gen02_spiALL_OneDay_download as fnD_01_download
import fnD_02_gen02_spiALL_OneDay_convert_nc2tiff as fnD_02_nc2tiff
import fnD_03_gen02_spiALL_OneDay_convert_png as fnD_03_png
import fnD_04_gen02_spiALL_OneDay_convert_mp4 as fnD_04_mp4



gregorian_date = "20240101"


def RunOneDay(gregorian_date):

    fnD_01_download.sp_gen02_spiALL_OneDay_Hardcoded(gregorian_date)
    fnD_02_nc2tiff.sp_gen02_spiALL_OneDay_Hardcoded(gregorian_date)
    fnD_03_png.sp_gen02_spiALL_plotALL_OneDay_Hardcoded(gregorian_date)
    fnD_04_mp4.sp_gen02_spiALL_plotALL_OneDay_Hardcoded(gregorian_date)
    
    
    return




RunOneDay(gregorian_date)


