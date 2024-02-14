
# # # Own functions
import fn01_generic as fn01
import fn02_time as fn02
import fn05_str_paths_spected as fn05

# Libraries
import os
import rioxarray as rxr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import imread
from itertools import compress


# Funciones



def png_setup_LCFA_nc2png(selected_setup):
    principal_dic = {
        "png01": {
            "key": "01",
            "cmap": "Reds",
            "new_tail": "_nc2png01.png",
            "prefix_file_name" : "OR_GLM-L2-LCFA",
            "subfolder_name": "GLM-L2-LCFA",
            "original_format": ".nc"
        },
        "png02": {
            "key": "02",
            "folder": "coolwarm/",
            "cmap": "coolwarm",
            "new_tail": "_nc2png02.png",
            "prefix_file_name" : "OR_GLM-L2-LCFA",
            "subfolder_name": "GLM-L2-LCFA",
            "original_format": ".nc"
        },
    }

    return principal_dic[selected_setup]






def convert_LCFA_nc2png_gen01(selected_input_path, selected_output_path, selected_cmap, 
                              save_png = True, plot_me = False, tell_me = False):
    # Open .nc file and .tiff
    nc_file = rxr.open_rasterio(selected_input_path, mask_and_scale=True)
    
    the_raster = nc_file['LST'][0]
    
    # make plot
    fig, ax = plt.subplots()
    
    # show image
    shw = ax.imshow(the_raster, cmap = selected_cmap)
    # shw = ax.imshow(the_raster, cmap = "RdBu")
    

    # make bar
    bar = plt.colorbar(shw)

    # show plot with labels
    ax.set_title(selected_input_path)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    bar.set_label('Kelvin')
    
    if plot_me:
        plt.show()
    
    if save_png:
        fn01.create_folder_for_file(selected_output_path, tell_me = tell_me)
        fig.savefig(selected_output_path, dpi=200)   # save the figure to file
        if tell_me: 
            print("Plot saved!")
        
    plt.close(fig)
    nc_file.close()
    the_raster.close()
    return


def convert_LCFA_nc2png_gen02(input_folder, output_folder, 
                              selected_cmap = "Reds", new_tail = "",
                              save_png = True, plot_me = False, tell_me = True):

    # # # Process
    # 1) Create output folder
    fn01.create_folder_if_not_exists(output_folder)


    # Input and output paths for each file
    input_paths = fn01.list_paths_in_folder(input_folder)
    input_paths = [element for element in input_paths if element.endswith(".nc")]

    output_paths = fn05.list_spected_output_paths_nc2png(input_paths, input_folder, output_folder, 
                                                         new_tail)

    # Convertion for only one files
    for x in range(len(input_paths)):
        selected_input_path = input_paths[x]
        selected_output_path = output_paths[x]
        
        # # # ACA PUEDO AGREGAR CONTROLES
        dt_output_file = os.path.exists(selected_output_path)
            
        if not dt_output_file:    
            convert_LSTF_nc2png_gen01(selected_input_path = selected_input_path,
                                                    selected_output_path = selected_output_path, 
                                                    selected_cmap = selected_cmap,
                                                    save_png = save_png, plot_me = plot_me, tell_me = tell_me)
            
        elif dt_output_file:
            print("File exists!")
            
    return        




def convert_LCFA_nc2png_gen03_OneDay(general_input_folder, general_output_folder, selected_gregorian_date_SEP, tell_me = True):
        
        
    all_key = ["png01", "png02"]
    
    for x in range(len(all_key)):
        ################################################################
        key_png_setup = all_key[x]
        selected_png_setup = png_setup_LSTF_nc2png(key_png_setup)
        ###############################################################

        sat_prod =     selected_png_setup["subfolder_name"]
        new_tail = selected_png_setup["new_tail"]
        selected_cmap = selected_png_setup["cmap"]

        general_output_folder_mod = general_output_folder.replace("png", key_png_setup)


        input_folder = fn05.build_str_input_folder_OneDay_nc2png(general_input_folder = general_input_folder,
                                                                selected_gregorian_date_SEP = selected_gregorian_date_SEP,
                                                                sat_prod = sat_prod )
        
        output_folder = input_folder.replace(general_input_folder, 
                                            general_output_folder_mod)




        convert_LSTF_nc2png_gen02(input_folder, output_folder, 
                                    selected_cmap = selected_cmap, new_tail = new_tail,
                                    save_png = True, plot_me = False, tell_me = tell_me)
        
    return



