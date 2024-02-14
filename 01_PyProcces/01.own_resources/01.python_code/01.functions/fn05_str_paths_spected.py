
# # # Own functions
import fn01_generic as fn01
import fn02_time as fn02



# Libraries
import os
import rioxarray as rxr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import imread
from itertools import compress
import re




# File .nc Original projection on K
def project_goes16_folder_total_view_subfolder_structure(selected_setup):
    principal_dic = {
        "f00": {
            "download_nc": "01.goes16_files_nc/",
            "nc2png": "02.goes16_nc2png/",
            "nc2tiff": "03.goes16_nc2tiff/",
            "tiff2png": "04.goes16_tiff2png/"
            
        },
        "f00": {
            "download_nc": "01.goes16_files_nc/",
            "convert_nc2png": "02.goes16_nc2png/",
            "convert_nc2tiff": "03.goes16_nc2tiff/",
            "convert_tiff2png": "04.goes16_tiff2png/"
            
        }
    }
    
##################################################################################

# # # # 2) .nc to .png    
def list_output_paths_nc2png(input_paths, input_folder, output_folder):
    
    output_paths = []
    for x in range(len(input_paths)):
        selected_input_path = input_paths[x]
        prev_ext = ".nc"
        new_ext = ".png"


        # Usar una expresión regular para reemplazar la subcadena al final
        new_str = selected_input_path
        new_str = re.sub(f'{re.escape(prev_ext)}$', f'{new_ext}', new_str)
        new_str = re.sub(input_folder, output_folder, new_str)
       
        output_paths.append(new_str)

    return(output_paths)

# 
def generator_input_and_output_paths_nc2png_OnlyOneBand(selected_png_setup, input_folder, output_folder, gregorian_date):
    new_tail = selected_png_setup["new_tail"]
    new_format = selected_png_setup["new_format"]
    prefix_file_name = selected_png_setup["prefix_file_name"]
    original_format = selected_png_setup["original_format"]
    subfolder_prod_info =  selected_png_setup["subfolder_prod_info"]
    subfolder_version =  selected_png_setup["subfolder_version"]
    
    domain = selected_png_setup["domain"]
 
    # Fusion subfolder
    subfolder_fusion = subfolder_prod_info + subfolder_version       
        
        
    # Input paths
    input_paths = fn01.list_paths_in_folder(input_folder)
    input_paths = [element for element in input_paths if subfolder_prod_info in element]
    input_paths = [element for element in input_paths if gregorian_date in element]
    input_paths = [element for element in input_paths if prefix_file_name in element]
    input_paths = [element for element in input_paths if element.endswith(original_format)]

    # Output paths
    output_paths = list_output_paths_nc2png(input_paths, input_folder, output_folder)
    output_paths = [re.sub(f'{new_format}$', f'{new_tail}', x) for x in output_paths] 
    output_paths = [re.sub(f'{subfolder_prod_info}', f'{subfolder_fusion}', x) for x in output_paths]  

    return input_paths, output_paths


def generator_input_and_output_paths_nc2png_MIX01(selected_png_setup, selected_png_setup01, selected_png_setup02, input_folder, output_folder, gregorian_date):
    new_tail = selected_png_setup["new_tail"]
    prefix_file_name = selected_png_setup["prefix_file_name"]
    original_format = selected_png_setup["original_format"]
    new_format = selected_png_setup["new_format"]
    subfolder_prod_info =  selected_png_setup["subfolder_prod_info"]
    subfolder_version =  selected_png_setup["subfolder_version"]
    
    # Fusion subfolder
    subfolder_fusion = subfolder_prod_info + subfolder_version 
        
    # # # # # Details 01 - MCMIPF    
    prefix_file_name01 = selected_png_setup01["prefix_file_name"]
    original_format01 = selected_png_setup01["original_format"]
    subfolder_prod_info01 =  selected_png_setup01["subfolder_prod_info"]
        
        
    # Input and output paths for each file
    input_paths01 = fn01.list_paths_in_folder(input_folder)
    input_paths01 = [element for element in input_paths01 if prefix_file_name01 in element]
    input_paths01 = [element for element in input_paths01 if element.endswith(original_format01)]
    input_paths01 = [element for element in input_paths01 if gregorian_date in element]


    # # # # # # Details02 - LSTF
    prefix_file_name02 = selected_png_setup02["prefix_file_name"]
    original_format02 = selected_png_setup02["original_format"]
    subfolder_prod_info02 =  selected_png_setup02["subfolder_prod_info"]
    domain02 = selected_png_setup02["domain"]
        
        
    # Input and output paths for each file
    input_paths02 = fn01.list_paths_in_folder(input_folder)
    input_paths02 = [element for element in input_paths02 if prefix_file_name02 in element]
    input_paths02 = [element for element in input_paths02 if element.endswith(original_format02)]
    input_paths02 = [element for element in input_paths02 if gregorian_date in element]



    #output_paths = fn05.list_spected_output_paths_nc2png(input_paths02, input_folder, output_folder, new_tail)
# Output paths
    output_paths = list_output_paths_nc2png(input_paths01, input_folder, output_folder)
    output_paths = [re.sub(f'{re.escape(new_format)}$', f'{new_tail}', x) for x in output_paths]   
    output_paths = [re.sub(f'{subfolder_prod_info01}', f'{subfolder_fusion}', x) for x in output_paths]  

    return input_paths01, input_paths02, output_paths


###################################################################################

# # # # 3) nc2png2mp4


###################################################################################################

# # # # 4) nc2tiff
def list_output_paths_nc2tiff(input_paths, input_folder, output_folder):
    
    output_paths = []
    for x in range(len(input_paths)):
        selected_input_path = input_paths[x]
        prev_ext = ".nc"
        new_ext = ".tiff"


        # Usar una expresión regular para reemplazar la subcadena al final
        new_str = selected_input_path
        new_str = re.sub(f'{re.escape(prev_ext)}$', f'{new_ext}', new_str)
        new_str = re.sub(input_folder, output_folder, new_str)
       
        output_paths.append(new_str)

    return(output_paths)




def generator_input_and_output_paths_nc2tiff_OnlyOneBand(selected_tiff_setup, input_folder, output_folder, gregorian_date):
    new_tail = selected_tiff_setup["new_tail"]
    new_format = selected_tiff_setup["new_format"]
    prefix_file_name = selected_tiff_setup["prefix_file_name"]
    original_format = selected_tiff_setup["original_format"]
    subfolder_prod_info =  selected_tiff_setup["subfolder_prod_info"]
    subfolder_version =  selected_tiff_setup["subfolder_version"]
    
    domain = selected_tiff_setup["domain"]
 
    # Fusion subfolder
    subfolder_fusion = subfolder_prod_info + subfolder_version       
        
        
    # Input paths
    input_paths = fn01.list_paths_in_folder(input_folder)
    input_paths = [element for element in input_paths if subfolder_prod_info in element]
    input_paths = [element for element in input_paths if gregorian_date in element]
    input_paths = [element for element in input_paths if prefix_file_name in element]
    input_paths = [element for element in input_paths if element.endswith(original_format)]

    # Output paths
    output_paths = list_output_paths_nc2tiff(input_paths, input_folder, output_folder)
    output_paths = [re.sub(f'{new_format}$', f'{new_tail}', x) for x in output_paths] 
    output_paths = [re.sub(f'{subfolder_prod_info}', f'{subfolder_fusion}', x) for x in output_paths]  

    return input_paths, output_paths


###################################################################################################

# # # # 5) tiff2png

def list_output_paths_tiff2png(input_paths, input_folder, output_folder):
    
    output_paths = []
    for x in range(len(input_paths)):
        selected_input_path = input_paths[x]
        prev_ext = ".tiff"
        new_ext = ".png"


        # Usar una expresión regular para reemplazar la subcadena al final
        new_str = selected_input_path
        new_str = re.sub(f'{re.escape(prev_ext)}$', f'{new_ext}', new_str)
        new_str = re.sub(input_folder, output_folder, new_str)
        new_str = re.sub("nc2tiff", "tiff2png", new_str)
       
        output_paths.append(new_str)

    return(output_paths)




def generator_input_and_output_paths_tiff2png_OnlyOneBand(selected_png_setup, input_folder, output_folder, gregorian_date):
    new_tail = selected_png_setup["new_tail"]
    new_format = selected_png_setup["new_format"]
    prefix_file_name = selected_png_setup["prefix_file_name"]
    original_format = selected_png_setup["original_format"]
    subfolder_prod_info =  selected_png_setup["subfolder_prod_info"]
    subfolder_version =  selected_png_setup["subfolder_version"]

    domain = selected_png_setup["domain"]
 
    # Fusion subfolder
    subfolder_fusion = subfolder_prod_info + subfolder_version       
        
        
    # Input paths
    input_paths = fn01.list_paths_in_folder(input_folder)
    input_paths = [element for element in input_paths if subfolder_prod_info in element]
    input_paths = [element for element in input_paths if gregorian_date in element]
    input_paths = [element for element in input_paths if prefix_file_name in element]
    input_paths = [element for element in input_paths if element.endswith(original_format)]

    # Output paths
    output_paths = list_output_paths_tiff2png(input_paths, input_folder, output_folder)
    output_paths = [re.sub(f'{new_format}$', f'{new_tail}', x) for x in output_paths] 
    output_paths = [re.sub(f'{subfolder_prod_info}', f'{subfolder_fusion}', x) for x in output_paths]  

    return input_paths, output_paths





def generator_input_and_output_paths_tiff2png_MIX01(selected_png_setup, selected_png_setup01, selected_png_setup02, input_folder, output_folder, gregorian_date):
    new_tail = selected_png_setup["new_tail"]
    prefix_file_name = selected_png_setup["prefix_file_name"]
    original_format = selected_png_setup["original_format"]
    new_format = selected_png_setup["new_format"]
    subfolder_prod_info =  selected_png_setup["subfolder_prod_info"]
    subfolder_version =  selected_png_setup["subfolder_version"]
    
    # Fusion subfolder
    subfolder_fusion = subfolder_prod_info + subfolder_version 
        
    # # # # # Details 01 - MCMIPF    
    prefix_file_name01 = selected_png_setup01["prefix_file_name"]
    original_format01 = selected_png_setup01["original_format"]
    subfolder_prod_info01 =  selected_png_setup01["subfolder_prod_info"]
        
        
    # Input and output paths for each file
    input_paths01 = fn01.list_paths_in_folder(input_folder)
    input_paths01 = [element for element in input_paths01 if prefix_file_name01 in element]
    input_paths01 = [element for element in input_paths01 if element.endswith(original_format01)]
    input_paths01 = [element for element in input_paths01 if gregorian_date in element]


    # # # # # # Details02 - LSTF
    prefix_file_name02 = selected_png_setup02["prefix_file_name"]
    original_format02 = selected_png_setup02["original_format"]
    subfolder_prod_info02 =  selected_png_setup02["subfolder_prod_info"]
    domain02 = selected_png_setup02["domain"]
        
        
    # Input and output paths for each file
    input_paths02 = fn01.list_paths_in_folder(input_folder)
    input_paths02 = [element for element in input_paths02 if prefix_file_name02 in element]
    input_paths02 = [element for element in input_paths02 if element.endswith(original_format02)]
    input_paths02 = [element for element in input_paths02 if gregorian_date in element]



    #output_paths = fn05.list_spected_output_paths_nc2png(input_paths02, input_folder, output_folder, new_tail)
# Output paths
    output_paths = list_output_paths_tiff2png(input_paths01, input_folder, output_folder)
    output_paths = [re.sub(f'{re.escape(new_format)}$', f'{new_tail}', x) for x in output_paths]   
    output_paths = [re.sub(f'{subfolder_prod_info01}', f'{subfolder_fusion}', x) for x in output_paths]  

    return input_paths01, input_paths02, output_paths






###################################################################################################
def build_str_input_folder_OneDay_nc2png(general_input_folder, selected_gregorian_date_SEP, sat_prod = ""):
    selected_julian_date_sep = fn02.gregorianSEP_to_julianSEP(selected_gregorian_date_SEP)
    julian_subfolders = selected_julian_date_sep.replace("-", "/") + "/" 
    all_folders = fn01.list_folders(general_input_folder)
    selected_string = [s for s in all_folders if s.endswith(sat_prod)]
    selected_string = selected_string[0]
    input_folder = str(selected_string) + "/" + str(julian_subfolders)
    return input_folder





###########################################################################################################


# 2) nc to tiff



def build_str_input_folder_OneDay_nc2tiff(general_input_folder, selected_gregorian_date_SEP, sat_prod = ""):
    selected_julian_date_sep = fn02.gregorianSEP_to_julianSEP(selected_gregorian_date_SEP)
    julian_subfolders = selected_julian_date_sep.replace("-", "/") + "/" 
    all_folders = fn01.list_folders(general_input_folder)
    selected_string = [s for s in all_folders if s.endswith(sat_prod)]
    selected_string = selected_string[0]
    input_folder = str(selected_string) + "/" + str(julian_subfolders)
    return input_folder





def path_nc_to_tiff(input_folder, output_folder, selected_nc_path):
    png_path = selected_nc_path.replace(input_folder, output_folder).replace('.nc', '.tiff')
    return(png_path)




def list_spected_output_paths_nc2tiff(input_paths, input_folder, output_folder, new_tail):
    
    input_folders = [os.path.dirname(x) for x in input_paths]
    input_files = [os.path.basename(x)  for x in input_paths]
    input_names = [os.path.splitext(x)[0]  for x in input_files]


    # Spected output path for each file
    spected_output_paths = [path_nc_to_tiff(input_folder = input_folder, 
                                output_folder = output_folder , 
                                selected_nc_path = input_paths[x])for x in range(len(input_files))]
    
    
    spected_output_paths = [ x.replace(".tiff", new_tail) for x in spected_output_paths]
    
    return(spected_output_paths)



#########################################################################################



# 3) tiff to png


def build_str_input_folder_OneDay_tiff2png(general_input_folder, selected_gregorian_date_SEP, sat_prod = ""):
    selected_julian_date_sep = fn02.gregorianSEP_to_julianSEP(selected_gregorian_date_SEP)
    julian_subfolders = selected_julian_date_sep.replace("-", "/") + "/" 
    all_folders = fn01.list_folders(general_input_folder)
    selected_string = [s for s in all_folders if s.endswith(sat_prod)]
    selected_string = selected_string[0]
    input_folder = str(selected_string) + "/" + str(julian_subfolders)
    return input_folder




def path_tiff_to_png(input_folder, output_folder, selected_tiff_path):
    png_path = selected_tiff_path.replace(input_folder, output_folder).replace('.tiff', '.png')
    return(png_path)



def list_spected_output_paths_tiff2png(input_paths, input_folder, output_folder, new_tail):
    
    input_folders = [os.path.dirname(x) for x in input_paths]
    input_files = [os.path.basename(x)  for x in input_paths]
    input_names = [os.path.splitext(x)[0]  for x in input_files]


    # Spected output path for each file
    spected_output_paths = [path_tiff_to_png(input_folder = input_folder, 
                                output_folder = output_folder , 
                                selected_tiff_path = input_paths[x])for x in range(len(input_files))]
    
    spected_output_paths = [ x.replace(".png", new_tail) for x in spected_output_paths]
    
    return(spected_output_paths)

