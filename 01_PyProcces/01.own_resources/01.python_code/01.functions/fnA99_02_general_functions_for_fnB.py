# Libraries
import os
from pathlib import Path
import rioxarray as rxr


# Own libraries
import fn01_generic as fn01
import fn02_time as fn02





def str_download_output_folder(gregorian_date, fnBxxx_setup):
    special_output_folder = fnBxxx_setup.hard_setup_02_download()["special_output_folder"]
    subfolder_date = fn02.gregorianCOMP_to_newsubfolder(gregorian_date_str = gregorian_date)
    list_folder = [special_output_folder, subfolder_date]
    output_folder =  str(Path().joinpath(*list_folder, "")) + "/"
    # output_folder = special_output_folder + "/" + subfolder_date + "/"
    return output_folder
    


def str_nc2tiff_output_folder(gregorian_date, fnBxxx_setup):
 
    input_folder = str_download_output_folder(gregorian_date, fnBxxx_setup)
    special_input_folder =  fnBxxx_setup.hard_setup_02_download()["special_output_folder"]   
    special_output_folder = fnBxxx_setup.hard_setup_03_nc2tiff()["special_output_folder"]
 
    
    output_folder = input_folder.replace(special_input_folder, special_output_folder)

    return output_folder




def str_nc2png_output_folder(gregorian_date, fnBxxx_setup):
 
    input_folder = str_download_output_folder(gregorian_date, fnBxxx_setup)
    special_input_folder =  fnBxxx_setup.hard_setup_02_download()["special_output_folder"]
    special_output_folder = fnBxxx_setup.hard_setup_04_png()["special_output_folder"]
    
    output_folder = input_folder.replace(special_input_folder, special_output_folder)

    return output_folder



def str_tiff2png_output_folder(gregorian_date, fnBxxx_setup):
 
    input_folder = str_nc2tiff_output_folder(gregorian_date, fnBxxx_setup)
    special_input_folder =  fnBxxx_setup.hard_setup_03_nc2tiff()["special_output_folder"]
    special_output_folder = fnBxxx_setup.hard_setup_04_png()["special_output_folder"]
    
    output_folder = input_folder.replace(special_input_folder, special_output_folder)

    return output_folder



