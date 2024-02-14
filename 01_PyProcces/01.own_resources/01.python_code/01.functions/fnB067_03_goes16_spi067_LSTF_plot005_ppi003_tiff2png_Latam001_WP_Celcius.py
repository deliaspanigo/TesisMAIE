
# # # Own libraries
import fn01_generic as fn01
import fn02_time as fn02
import fnA99_02_general_functions_for_fnB as fnA99_gf
import fnB067_00_goes16_spi067_LSTF_setup as fnB067_00_setup
import fnB067_02_goes16_spi067_LSTF_convert_nc2tiff as fnB067_02_nc2tiff

# # # Import libraries
import cartopy.crs as ccrs
import custom_color_palette as ccp
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import rioxarray as rxr



# # # From... Import libraries
from cartopy.feature import NaturalEarthFeature
from cartopy.feature import ShapelyFeature
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter



# # # Data upload
# Argentinuian provinces - vectorial - shapefile
ruta_shapefile_prov_ARG = "01.own_resources/02.vectorial/prov_argentina_malv/prov_argentina_malv.shp"
datos_shapefile_prov_ARG = gpd.read_file(ruta_shapefile_prov_ARG)


def standard_plot_Hardcoded(gregorian_date):
    
    # # # Pack on dictionary    
    pdict = {}
    
    pdict["gregorian_date"] = gregorian_date
    pdict["plot"] = "plot005"
    pdict["ppi"] =  "ppi003"
    pdict["label"] = "tiff2png_Latam001_WP_Celcius"
    pdict["input_ext_file"] =  ".tiff"
    pdict["output_ext_file"] =  ".png"
    pdict["output_proj"] = "WGS84"
    
    fusion_label = [pdict["plot"], pdict["ppi"], pdict["label"]]
    pdict["full_label"] = "_".join(fusion_label)
    
    pdict["plot_me"] = False
    pdict["save_me"] = True
    pdict["overwrite"] = False
    
    return pdict


   

def standard_input_OneDay_Hardcoded(gregorian_date = None):

    # # # Source information
    info_nc2tiff_input =  fnB067_02_nc2tiff.standard_input_OneDay_Hardcoded(gregorian_date)
    info_nc2tiff_output =  fnB067_02_nc2tiff.standard_output_OneDay_Hardcoded(gregorian_date)
    
    # # # Input folder is a previus output folder
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
    info_setup = fnB067_00_setup.hard_setup_04_png()
    info_input =  standard_input_OneDay_Hardcoded(gregorian_date)
    info_standard_plot = standard_plot_Hardcoded(gregorian_date)
   
    
    # # # Input folder and output folder
    input_folder = info_input["input_folder"]
    output_subfolder01 = fnA99_gf.str_tiff2png_output_folder(gregorian_date, fnB067_00_setup)
    output_subfodler02 = info_standard_plot["full_label"]
    output_folder = output_subfolder01 + output_subfodler02 + "/"
    
    # # # Initial info
    list_spected_input_files = info_input["list_spected_input_files"]
    list_spected_input_paths = info_input["list_spected_input_paths"]
    ext_input_file =  ".tiff" #info_setup["input_ext_file_01"]
    ext_output_file = ".png"  #info_setup["output_ext_file"]
    
    # # # Spected output files
    # The file extension is changed.
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
           


# LSTF - download
def sp_gen01(selected_input_path, selected_output_path, plot_me = True, save_me = False, overwrite = False):
    
    # # # Prints!
    print("Start: sp_gen01()")
    
    # # # Not run if file exists! -----------------------------------------------
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
    
    
    # # # # # Source information ----------------------------------------------------
    info_setup = fnB067_00_setup.hard_setup_04_png()
    
    # # # Internal parameters
    selected_product = info_setup["sat_prod"]
    abrev_name2 = info_setup["abrev_name_02"]
    domain_map = [ -90.0, -30.0, -60.0, 15.0]
    domain_img = [-165.0, 15.0, -90.0, 90.0]
    unit_var =  "C"
    min_var =  -60
    max_var =   60
    mini_step =  1.0
    big_step =  10


    # # # # # More information to plot ----------------------------------
    # # # Plot argentian limits?    
    dt_province_limits_arg = False
    
    # # # More details
    sat = "GOES16"         
    sat_info = "epsg4623"
    
    
    # # # Local time (ARG)
    selected_file_name = os.path.basename(selected_input_path)
    utc_date = fn02.str_fulltime_from_filename(selected_file_name, str01 = "G16_s", str02 = "_")
    local_date = fn02.gregoriandate_utc2local_string(fecha_string = utc_date, correccion= 3)

    # # # Import .tiff selected_input_path ---------------------------------
    ds = rxr.open_rasterio(selected_input_path, mask_and_scale=True)
    ds[0]  = ds[0].where(ds[0]  != -9999, np.nan)
    CMI = ds[0]
    LonCor = ds["x"]
    LatCor = ds["y"]
    
    
    # # # Settings colours and palette ----------------------------------------
    # set the colors of the custom palette
    lower_colors = ['maroon','red','darkorange','#ffff00','forestgreen','cyan','royalblue',(148/255,0/255,211/255)]
    lower_colors.reverse()
    lower_palette = [lower_colors, ccp.range(min_var,max_var,mini_step)]


    # # # Palette creation
    cmap, cmticks, norm, bounds = ccp.creates_palette([lower_palette], extend='both')

    # # # Creating colorbar labels
    ticks = ccp.range(min_var,max_var,big_step)

    # # # Central longitud from map domain
    lon_cen_map = 360.0+(domain_map[0]+domain_map[1])/2.0



    # # # # Plot Code ------------------------------------
    # # # Setting for parallel proccesing
    #plt.switch_backend('Agg') 


    # # # Plot setup
    fig = plt.figure('Map', figsize=(4,4), dpi=200)
    ax = fig.add_axes([0.1, 0.16, 0.80, 0.75], 
                      projection=ccrs.PlateCarree(lon_cen_map))

    # # # Data plotting
    img = ax.pcolormesh(LonCor.data, LatCor.data, CMI.data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())


    # # # Plotting international boundaries
    l = NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
    ax.add_feature(l, edgecolor='black', linewidth=0.25)

    
    # # # Adding argentinians provinces boundaries
    if dt_province_limits_arg:
        shape_feature = ShapelyFeature(datos_shapefile_prov_ARG['geometry'], 
                                       ccrs.PlateCarree(), edgecolor='black', linewidth=0.3)
        ax.add_feature(shape_feature, facecolor='none')
        
        
    
    # # # Adding colorbar
    cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend='both',
                    cax=fig.add_axes([0.12, 0.07, 0.76, 0.02]))
    
    
    # # # Colorbar parameters
    cb.ax.tick_params(labelsize=5, labelcolor='black', width=0.5, length=1.5, direction='out', pad=1.0)
    cb.set_label(label='{} [{}]'.format("Temperatura de superficie", CMI.units), size=5, color='black', weight='normal')    
    cb.outline.set_linewidth(0.5)

      
    # # # Left title
    title_left = '{} - {} [{}]'.format(sat,selected_product, unit_var)
    ax.set_title(title_left, fontsize=7, loc='left')

    # # # Right title
    title_right = '{}\n{}'.format(local_date , utc_date)
    ax.set_title(title_right, fontsize=7, loc='right')



    # # # Setting X axis characteristics
    dx = 15
    xticks = np.arange(domain_map[0], domain_map[1]+dx, dx)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter(dateline_direction_label=True))
    ax.set_xlabel('Longitud', color='black', fontsize=7, labelpad=3.0)



    # # # Setting Y axis characteristics
    dy = 15
    yticks = np.arange(domain_map[2], domain_map[3]+dy, dy)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_ylabel('Latitud', color='black', fontsize=7, labelpad=3.0)



    # Sets tick characteristics
    ax.tick_params(left=True, right=True, bottom=True, top=True,
                labelleft=True, labelright=False, labelbottom=True, labeltop=False,
                length=0.0, width=0.05, labelsize=5.0, labelcolor='black')


    # # # Setting tick characteristics for both axis
    ax.gridlines(xlocs=xticks, ylocs=yticks, alpha=0.6, color='gray',
                draw_labels=False, linewidth=0.25, linestyle='--')


    # # # Setting map limits!
    ax.set_extent([domain_map[0]+360.0, domain_map[1]+360.0, domain_map[2], domain_map[3]], crs=ccrs.PlateCarree())


    # # # Plot me!
    if plot_me:
        plt.show()

    # # # Save me!
    if save_me:
        if not os.path.exists(selected_output_path) or overwrite:
            fn01.create_folder_for_file(selected_output_path)
            fig.savefig(selected_output_path, dpi=200) 
    
    
    # # # Cleanning all...    
    plt.clf()
    
    # # # Clossing all...
    plt.close()

    # # # Final print!   
    print("Close: sp_gen01()")
    
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
   
   