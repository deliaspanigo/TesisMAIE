# Import own libreries
import sys

fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01
import fn05_str_paths_spected as fn05
import fn067_03_goes16_spi067_LSTF_ppi003_convert_tiff2png_v001_WGS84_Celcius as fn067_03_ppi003
import fn076_03_goes16_spi076_MCMIPF_ppi004_convert_tiff2png_v001_WGS84Proj_RGB as fn076_03_ppi004


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
from multiprocessing import Pool


# Libraries - v01 
import custom_color_palette as ccp
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature


# Libraries - v02
import rioxarray as rxr


from matplotlib.image import imread
from itertools import compress
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Funciones
from joblib import Parallel, delayed

from multiprocessing import Pool
import time
import math


# File .nc Original projection on K
def setup_goes16_spi301_MIX01_convert_tiff2png_v01(selected_setup):
    principal_dic = {
        "f00": {
            "product_name": "",
            "original_format": ".tiff",
            "new_format": ".png",
            "new_tail": "_tiff2png2png_spi301_ppi007_v002_dom000_OrigProj.png",
            "prefix_file_name" : "OR_ABI-L2-MCMIPF",
            "subfolder_prod_info": "spi301_MIX001/",
            "subfolder_version": "spi301_ppi007_tiff2png_v002_dom000_OrigProj/",
            "abrev_name": "MIX001"

            
        },
        "f01": {
            "key": "02",
            "folder": "coolwarm/",
            "cmap": "coolwarm",
            "new_tail": "_tiff2png02.png",
            "prefix_file_name" : "OR_ABI-L2-LSTF",
            "subfolder_name": "ABI-L2-LSTF",
            "original_format": ".nc"
        },
    }

    return principal_dic[selected_setup]


def convert_tiff2png_goes16_spi301_MIX01_v01_gen01(selected_input_path01, selected_input_path02,selected_output_path, plot_me = True, save_me = True, overwrite = False):


    #########################################################
    dt_exists = os.path.exists(selected_output_path)
    if dt_exists: 
        #print("\n")
        #print(f"File exists: {selected_output_path}")
        print("File exists!\n")
        return
    elif not dt_exists:
        print("In progress...\n")
    ##########################################################
    
    if plot_me or save_me:
        dt_ok = True
        
    if not dt_ok:
        print("Arguments plot_me and save_me are 'False'.") 
        return
    
    # Scan's start time, converted to datetime object


    # Image01 - MCIPF
## Abrir el archivo con rasterio
    with rasterio.open(selected_input_path01) as src:
        # Leer las tres bandas
        r, g, b = src.read()

        # Reemplazar NaN con un valor predeterminado (por ejemplo, 0)
        r = np.nan_to_num(r, nan=0)
        g = np.nan_to_num(g, nan=0)
        b = np.nan_to_num(b, nan=0)

        # Obtener la información de transformación
        transform = src.transform
        profile = src.profile
        xmin, ymin, xmax, ymax = src.bounds


    # Crear una imagen RGB combinando las tres bandas
    rgb_image = (r, g, b)
    rgb_image = np.transpose([r, g, b], (1, 2, 0))
    
    # Domains
    # domain_map =  [xmin,  xmax, ymin, ymax]
    # domain_map =  [xmin,  xmax, -90, 90]
    domain_map =  [-180, 180, -90, 90]
    domain_img01 = [xmin,  xmax, ymin, ymax]
    
    # Central longitud for domains
    lon_cen_map = 360.0+(domain_map[0]+domain_map[1])/2.0
    lon_cen_img01 = 360.0+(domain_img01[0]+domain_img01[1])/2.0
    
    
    # Image 02 - LSTF
    # Setup png
    key_png_setup = "dom000"
    selected_png_setup = fn067_03_ppi003.dict_setup_NABU(key_png_setup)
    
    selected_product = selected_png_setup["product_name"]
    abrev_name = selected_png_setup["abrev_name"]
    domain = selected_png_setup["domain"]
    unit_var = selected_png_setup["unit_var"]
    min_var = selected_png_setup["min_var"]
    max_var = selected_png_setup["max_var"]
    mini_step = selected_png_setup["mini_step"]
    big_step = selected_png_setup["big_step"]
    
    ##############################################################
    domain_img02 = domain
    lon_cen_img02 = 360.0+(domain_img02[0]+domain_img02[1])/2.0
    ##############################################################
    
    
    # Import .nc file and setup for more details
    ds = rxr.open_rasterio(selected_input_path02, mask_and_scale=True)
    ds[0]  = ds[0].where(ds[0]  != -9999, np.nan)
    CMI = ds[0]
    LonCor = ds["x"]
    LatCor = ds["y"]
    
    
    #  sat = ds.attribute('platform_ID')
    #  sat_info = ds.variable('goes_imager_projection')
    sat = "GOES16"         # Esta bien asi??????? #faltaria que lo tome de los metatados
    sat_info = "epsg4623"  # Esta bien asi???????
    
    
    # # # Setings colours
    # set the colors of the custom palette
    lower_colors = ['maroon','red','darkorange','#ffff00','forestgreen','cyan','royalblue',(148/255,0/255,211/255)]
    lower_colors.reverse()

    lower_palette = [lower_colors, ccp.range(min_var,max_var,mini_step)]


    # pass parameters to the creates_palette module
    # cmap, cmticks, norm, bounds = ccp.creates_palette([lower_palette, upper_palette], extend='both')
    cmap, cmticks, norm, bounds = ccp.creates_palette([lower_palette], extend='both')

    # creating colorbar labels
    ticks = ccp.range(min_var,max_var,big_step)

    
    # # # Plot
    # plt.switch_backend('Agg') # Esto es para que en ejecucion en paralelo no haya problemas.
    
    # creates the figure
    fig = plt.figure('map', figsize=(4,4), dpi=200)
    ax = fig.add_axes([0.1, 0.16, 0.80, 0.75], projection=ccrs.PlateCarree(lon_cen_map))
    # ax.outline_patch.set_linewidth(0.3)


    # set the map limits
    ax.set_extent([domain_map[0]+360.0, domain_map[1]+360.0, domain_map[2], domain_map[3]], crs=ccrs.PlateCarree())
    
    # Add RGB image
    ax.imshow(rgb_image, extent = domain_img01, origin='upper', transform=ccrs.PlateCarree())
    
    # add LSTF image
    img = ax.pcolormesh(LonCor.data, LatCor.data, CMI.data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

    # add the geographic boundaries
    l = NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
    #ax.add_feature(l, edgecolor='gold', linewidth=0.25)
    ax.add_feature(l, edgecolor='black', linewidth=0.25)
    
    # add the colorbar
    cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend='both',
                    cax=fig.add_axes([0.12, 0.05, 0.76, 0.02]))
    cb.ax.tick_params(labelsize=5, labelcolor='black', width=0.5, length=1.5, direction='out', pad=1.0)
    cb.set_label(label='{} [{}]'.format(CMI.standard_name, CMI.units), size=5, color='black', weight='normal')
    cb.outline.set_linewidth(0.5)

    # set the title
    #ax.set_title('{} - C{:02d} [{:.1f} μm]'.format(sat,band, wl), fontsize=7, loc='left')
    ax.set_title('{} - {} [{}]'.format(sat,selected_product, unit_var), fontsize=7, loc='left')
    #ax.set_title(CMI.time_bounds.data[0].strftime('%Y/%m/%d %H:%M UTC'), fontsize=7, loc='right')

    # Sets X axis characteristics
    dx = 15
    xticks = np.arange(domain_map[0], domain_map[1]+dx, dx)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter(dateline_direction_label=True))
    ax.set_xlabel('Longitude', color='black', fontsize=7, labelpad=3.0)


    # Sets X axis characteristics
    dx = 15
    xticks = np.arange(domain_map[0], domain_map[1]+dx, dx)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter(dateline_direction_label=True))
    ax.set_xlabel('Longitude', color='black', fontsize=7, labelpad=3.0)

    # Sets Y axis characteristics
    dy = 15
    yticks = np.arange(domain_map[2], domain_map[3]+dy, dy)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_ylabel('Latitude', color='black', fontsize=7, labelpad=3.0)

    # Sets tick characteristics
    ax.tick_params(left=True, right=True, bottom=True, top=True,
                labelleft=True, labelright=False, labelbottom=True, labeltop=False,
                length=0.0, width=0.05, labelsize=5.0, labelcolor='black')

    # Sets grid characteristics
    ax.gridlines(xlocs=xticks, ylocs=yticks, alpha=0.6, color='gray',
                draw_labels=False, linewidth=0.25, linestyle='--')
  

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


###################################################################################################



############
def convert_tiff2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple(input_folder, output_folder, gregorian_date, plot_me, save_me, overwrite):

    print("Start: convert_tiff2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple()")
    
    key_png_setup = "f00"
    selected_png_setup = setup_goes16_spi301_MIX01_convert_tiff2png_v01(key_png_setup)
    
    key_png_setup01 = "f00"
    selected_png_setup01 = fn076_03_ppi004.setup_goes16_spi076_MCMIPF_convert_tiff2png_v01(key_png_setup01)
 
    key_png_setup02 = "dom000"
    selected_png_setup02 = fn067_03_ppi003.dict_setup_NABU(key_png_setup02)
 
 
    input_paths01, input_paths02, output_paths = fn05.generator_input_and_output_paths_tiff2png_MIX01(selected_png_setup, selected_png_setup01, selected_png_setup02, input_folder, output_folder, gregorian_date)

    total_files = len(input_paths01)

    for x in range(total_files):
        
        selected_input_path01 = input_paths01[x]
        selected_input_path02 = input_paths02[x]
        selected_output_path = output_paths[x]
        
        dt_exists = os.path.exists(selected_output_path)
        if dt_exists: 
            new_detail = "File exists!"
        elif not dt_exists:
            new_detail = "In progress..."
            
        print(f'Convertion... Init plot {x+1} of {total_files} - {new_detail}')

        if not dt_exists:
            convert_tiff2png_goes16_spi301_MIX01_v01_gen01(selected_input_path01, 
                                                     selected_input_path02,
                                                     selected_output_path,
                                                plot_me, save_me, overwrite)
        
            
    print("Close: convert_tiff2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple()")
    
    return





def convert_goes16_spi301_ppi007_gen02_OneDay_HardCoded(gregorian_date = None):
    
    print('Start: convert_goes16_spi301_ppi006_gen02_OneDay_HardCoded()')
        
    # User info - Hardcoded
    input_folder = '03.geot_goes16_wgs84Proj_tiff_files/'
    output_folder  = '04.png/' 
    plot_me = False 
    save_me = True
    overwrite = False
    
    
    # Create folder
    fn01.create_folder_if_not_exists(output_folder)
    
    # Download - gen02
    convert_tiff2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple(input_folder, output_folder, gregorian_date, plot_me, save_me, overwrite)

    print('Close: cconvert_goes16_spi301_ppi006_gen02_OneDay_HardCoded()')
    
    return


