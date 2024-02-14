# # # Own libraries
import fn01_generic as fn01
import fn02_time as fn02
import fnA99_02_general_functions_for_fnB as fnA99_gf
import fnB076_00_goes16_spi076_MCMIPF_setup as fnB076_00_setup
import fnB076_02_goes16_spi076_MCMIPF_convert_nc2tiff as fnB076_02_nc2tiff







# Libraries - v02
import os
#from datetime import datetime
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
#import xarray
import re 


# Libraries - v02
import os
from datetime import datetime
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from cartopy.feature import NaturalEarthFeature

# Funciones
import rasterio




def standard_plot_Hardcoded(gregorian_date):
        
    # # # Pack on dictionary
    pdict = {}
    
    pdict["gregorian_date"] = gregorian_date
    pdict["plot"] = "plot005"
    pdict["ppi"] =  "ppi002"
    pdict["label"] = "tiff2png_FullDisk_WP_v002"
    pdict["input_ext_file"] =  ".tiff"
    pdict["output_ext_file"] =  ".png"
    pdict["output_proj"] = "OrigProj"
    
    fusion_label = [pdict["plot"], pdict["ppi"], pdict["label"]]
    pdict["full_label"] = "_".join(fusion_label)
    
    pdict["plot_me"] = False
    pdict["save_me"] = True
    pdict["overwrite"] = False
    
    return pdict


  


def standard_input_OneDay_Hardcoded(gregorian_date = None):

 # # # Source information
    info_nc2tiff_input =  fnB076_02_nc2tiff.standard_input_OneDay_Hardcoded(gregorian_date)
    info_nc2tiff_output =  fnB076_02_nc2tiff.standard_output_OneDay_Hardcoded(gregorian_date)
   
    # # # Input folder is output downloaded files
    input_folder = info_nc2tiff_output["output_folder"]
    list_spected_input_files = info_nc2tiff_output["list_spected_output_files"]
    list_spected_input_paths = info_nc2tiff_output["list_spected_output_paths"]
    
    # # # Pack on dictionary
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_nc2tiff_output["spi_and_name_01"],
        "input_folder": input_folder,
        "list_spected_input_files": list_spected_input_files,
        "list_spected_input_paths": list_spected_input_paths
    }
    
    return pdict
    





def standard_output_OneDay_Hardcoded(gregorian_date = None):
    
    # # # Source information
    info_setup = fnB076_00_setup.hard_setup_04_png()
    info_input =  standard_input_OneDay_Hardcoded(gregorian_date)
    info_standard_plot = standard_plot_Hardcoded(gregorian_date)
   
    
    # # # Spected output file names for download files
    input_folder = info_input["input_folder"]
    output_subfolder01 = fnA99_gf.str_nc2png_output_folder(gregorian_date, fnB076_00_setup)
    output_subfodler02 = info_standard_plot["full_label"]
    output_folder = output_subfolder01 + output_subfodler02 + "/"
    
    # # # Initial info
    list_spected_input_files = info_input["list_spected_input_files"]
    list_spected_input_paths = info_input["list_spected_input_paths"]
    ext_input_file =  info_setup["input_ext_file_02"]
    ext_output_file = info_setup["output_ext_file"]
    
    # # # Spected output files
    # The file extension must chang.
    regex01 = '\\{}$'.format(ext_input_file)
    list_spected_output_files = [re.sub(regex01, ext_output_file, selected_file) for selected_file in list_spected_input_files]

    
    # # # Spected output paths
    # A change is applied to the name of the files and the initial folder.
    list_spected_output_paths = [list_spected_input_paths[x].replace(list_spected_input_files[x], list_spected_output_files[x]) for x in range(len(list_spected_input_paths))]
    list_spected_output_paths = [selected_path.replace(input_folder, output_folder) for selected_path in list_spected_output_paths]
       
    
    # # # Local files observed
    list_observed_output_files =   fn01.list_files_in_folder(output_folder)
    list_observed_output_paths =   fn01.list_paths_in_folder(output_folder)
    
    
    # # # Action detection for apply download file or not
    if len(list_observed_output_files) == 0:
        list_dt_action_files = [True]*len(list_spected_output_files)
    else:
        list_dt_action_files = [not spected_file in list_observed_output_files for spected_file in list_spected_output_files]

    # # # Detection for wrong files at folder
    if len(list_observed_output_files) == 0:
        list_dt_wrong_files = []
        list_wrong_files = None
    else:
        list_dt_wrong_files = [not observed_file in list_spected_output_files for observed_file in list_observed_output_files]
        list_wrong_files = [selected_obs_file for selected_obs_file, selected_dt in zip(list_observed_output_files, list_dt_action_files) if selected_dt]


    # # # Pack on dictionary
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_setup["spi_and_name_01"],
        "output_folder": output_folder,
        "len_spected_output_files": len(list_spected_output_files),
        "len_observed_output_files": len(list_observed_output_files),
        "len_wrong_output_files": sum(list_dt_wrong_files),
        "list_spected_output_files": list_spected_output_files,
        "list_spected_output_paths": list_spected_output_paths,
        "list_dt_action_files": list_dt_action_files, 
        "list_observed_output_files": list_observed_output_files, 
        "list_observed_output_paths": list_observed_output_paths,
    #    "list_dt_wrong_files": list_dt_wrong_files,
        "list_wrong_files": list_wrong_files
    }
    
    return pdict
           




def sp_gen01(selected_input_path, selected_output_path, plot_me = True, save_me = True, overwrite = False):
    
   # # # Prints!
    print("Start: sp_gen01()")
    
    # # # Not run if file exists!
    dt_exists = os.path.exists(selected_output_path)
    if dt_exists: 
        print("File exists!")
        return
    elif not dt_exists:
        print("In progress...")
    
    
    # # # Logical running
    if plot_me or save_me:
        dt_ok = True
        
    if not dt_ok:
        print("Arguments plot_me and save_me are 'False'.") 
        return
    

    # # # Source information
    info_setup = fnB076_00_setup.hard_setup_04_png()

    # # # More details
    selected_product = info_setup["sat_prod"]
    abrev_name = info_setup["abrev_name_02"]
    sat = "G16"   
    
    # # # Local time (ARG)
    selected_file_name = os.path.basename(selected_input_path)
    utc_date = fn02.str_fulltime_from_filename(selected_file_name, str01 = "G16_s", str02 = "_")
    local_date = fn02.gregoriandate_utc2local_string(fecha_string = utc_date, correccion= 3)



    ## Abrir el archivo con rasterio
    with rasterio.open(selected_input_path) as src:
        # Leer las tres bandas
        r, g, b = src.read()

        # Obtener la información de transformación
        transform = src.transform
        profile = src.profile
        xmin, ymin, xmax, ymax = src.bounds


    # Crear una imagen RGB combinando las tres bandas
    rgb_image = (r, g, b)
    rgb_image = np.transpose([r, g, b], (1, 2, 0))
    
    # Domains
    domain_map =  [xmin,  xmax, ymin, ymax]
    domain_img = [xmin,  xmax, ymin, ymax]
    
    # Central longitud for domains
    lon_cen_map = 360.0+(domain_map[0]+domain_map[1])/2.0
    lon_cen_img = 360.0+(domain_img[0]+domain_img[1])/2.0
     
    # creates the figure
    fig = plt.figure('map', figsize=(4,4), dpi=200)
    ax = fig.add_axes([0.1, 0.16, 0.80, 0.75], projection=ccrs.PlateCarree(lon_cen_map))
    
    # Fig extentions    
    ax.set_extent([domain_map[0]+360.0, domain_map[1]+360.0, domain_map[2], domain_map[3]], crs=ccrs.PlateCarree())

    # Add RGB image
    ax.imshow(rgb_image, extent = domain_img, origin='upper', transform=ccrs.PlateCarree())
   
    # add the geographic boundaries
    l = NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
    ax.add_feature(l, edgecolor='black', linewidth=0.25)
    
    # Cost lines
    ax.coastlines(resolution='10m', color='gold', linewidth=1)
    
    
    # # # Left title
    title_left = '{} - {}'.format(sat, selected_product)
    ax.set_title(title_left, fontsize=7, loc='left')

    # # # Right title
    title_right = '{}\n{}'.format(local_date , utc_date)
    ax.set_title(title_right, fontsize=7, loc='right')

    #output
    if plot_me:
        plt.show()

    if save_me:
        if not os.path.exists(selected_output_path) or overwrite:
            fn01.create_folder_for_file(selected_output_path)
            fig.savefig(selected_output_path, dpi=200) 
    
    # Clean...    
    plt.clf()
    
    # Close...
    plt.close()
    # Close ds    
    # ds.close()
    
    return




def sp_gen02(gregorian_date):
    
    
    
    print('Start: sp_gen02()')
    print("Selected gregorian day: {}".format(gregorian_date))


    info_standard_plot = standard_plot_Hardcoded(gregorian_date)
    info_input =  standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  standard_output_OneDay_Hardcoded(gregorian_date)


    print('Details: {}'.format(info_output["spi_and_name_01"]))
    print('input_folder: {}'.format(info_input["input_folder"]))
    print('output_folder: {}'.format(info_output["output_folder"]))
    print("\n")
        
    fn01.create_folder_if_not_exists(info_output["output_folder"])

    list_spected_input_paths = info_input["list_spected_input_paths"]
    list_spected_output_paths = info_output["list_spected_output_paths"]
    list_dt_action_files = info_output["list_dt_action_files"]



    len_files = len(list_spected_input_paths) 
    if len_files == 0:
        print("There are not files to procces.")
        #return

    # For each input file...
    for x in range(len_files):
        
        selected_input_path = list_spected_input_paths[x]
        selected_output_path = list_spected_output_paths[x]
        selected_dt_action = list_dt_action_files[x]
        
        if not selected_dt_action: 
            new_detail = "File exists!"
        elif selected_dt_action:
            new_detail = ""
            
        print(f'Convertion to png...  {x+1} of {len_files} - {new_detail}')

        if selected_dt_action or info_standard_plot["overwrite"]:
                sp_gen01(selected_input_path, selected_output_path, 
                        plot_me = info_standard_plot["plot_me"], 
                        save_me = info_standard_plot["save_me"],
                        overwrite = info_standard_plot["overwrite"])
        
        print("\n")
        
    print("Close: sp_gen02()")
    
    return
   
   