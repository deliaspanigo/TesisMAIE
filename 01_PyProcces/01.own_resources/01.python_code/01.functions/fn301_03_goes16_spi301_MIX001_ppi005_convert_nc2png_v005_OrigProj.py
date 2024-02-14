# Librerias
import sys


# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01
import fn02_time as fn02
import fn05_str_paths_spected as fn05
import fn06_goes_new_download_gen as fn06
import fn067_03_goes16_spi067_LSTF_ppi002_convert_nc2png_v002_OrigProj_Celcius as fn067_03_ppi002
import fn076_03_goes16_spi076_MCMIPF_ppi001_convert_nc2png_v001_OrigProj_RGB as fn076_03_ppi001

# More libraries
import os
import GOES
import custom_color_palette as ccp
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature

# Libraries - v02
import os
from datetime import datetime
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import metpy  # noqa: F401
import numpy as np
import xarray

import re
from multiprocessing import Pool

# File .nc Original projection on K



def setup_goes16_spi301_MIX01_convert_nc2png_v05(selected_setup):
    principal_dic = {
        "f00": {
            "product_name": "",
            "original_format": ".nc",
            "new_format": ".png",
            "new_tail": "_nc2png_spi301_ppi005_v005_dom000_OrigProj.png",
            "prefix_file_name" : "OR_ABI-L2-MCMIPF",
            "subfolder_prod_info": "spi301_MIX001/",
            "subfolder_version": "spi301_ppi005_nc2png_v005_dom000_OrigProj/",
            "abrev_name": "MIX001"

            
        },
        "f01": {
            "key": "02",
            "folder": "coolwarm/",
            "cmap": "coolwarm",
            "new_tail": "_nc2png02.png",
            "prefix_file_name" : "OR_ABI-L2-LSTF",
            "subfolder_name": "ABI-L2-LSTF",
            "original_format": ".nc"
        },
    }

    return principal_dic[selected_setup]




def convert_nc2png_goes16_spi301_MIX01_v05_gen01(selected_input_path01, selected_input_path02, selected_output_path, plot_me = True, save_me = True, overwrite = False):
    
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
    
    if plot_me or save_me:
        dt_ok = True
        
    if not dt_ok:
        print("Arguments plot_me and save_me are 'False'.") 
        #return
    
    # Parte 01: MCMIPF
    with xarray.open_dataset(selected_input_path01) as F:
        # Resto del código...

        # Scan's start time, converted to datetime object
        scan_start = datetime.strptime(F.time_coverage_start, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Scan's end time, converted to datetime object
        scan_end = datetime.strptime(F.time_coverage_end, '%Y-%m-%dT%H:%M:%S.%fZ')

        # File creation time, convert to datetime object
        file_created = datetime.strptime(F.date_created, '%Y-%m-%dT%H:%M:%S.%fZ')

        # The 't' variable is the scan's midpoint time
        midpoint = str(F['t'].data)[:-8]
        
        scan_mid = datetime.strptime(midpoint, '%Y-%m-%dT%H:%M:%S.%f')
        dat = F.metpy.parse_cf('CMI_C02')

        geos = dat.metpy.cartopy_crs
        
        # We'll use the `CMI_C02` variable as a 'hook' to get the CF metadata.
        dat = F.metpy.parse_cf('CMI_C02')
        x = dat.x
        y = dat.y
    
        # Load the RGB arrays
        R = np.clip(F['CMI_C02'][:].data, 0, 1)
        G = np.clip(F['CMI_C03'][:].data, 0, 1)
        B = np.clip(F['CMI_C01'][:].data, 0, 1)
        
        # Apply the gamma correction
        gamma = 2.2
        R = np.power(R, 1/gamma)
        G = np.power(G, 1/gamma)
        B = np.power(B, 1/gamma)

        # Calculate the "True" Green
        G_true = 0.48358168 * R + 0.45706946 * B + 0.06038137 * G
        G_true = np.clip(G_true, 0, 1)

        # The final RGB array :)
        RGB = np.dstack([R, G_true, B])

   
    # Part 02: LST
    key_png_setup02 = "dom000"
    selected_png_setup02 = fn067_03_ppi002.dict_setup_NABU(key_png_setup02)
    selected_product02 = selected_png_setup02["product_name"]
    abrev_name02 = selected_png_setup02["abrev_name"]
    domain02 = selected_png_setup02["domain"]
    unit_var02 = selected_png_setup02["unit_var"]
    min_var02 = selected_png_setup02["min_var"]
    max_var02 = selected_png_setup02["max_var"]
    mini_step02 = selected_png_setup02["mini_step"]
    big_step02 = selected_png_setup02["big_step"]
    
    
    # Import .nc file and setup for more details
    ds = GOES.open_dataset(selected_input_path02)
    CMI, LonCor, LatCor = ds.image(abrev_name02, lonlat='corner')
    
    ####################################
    CMI.data = CMI.data - 273.15
    # CMI.standard_name 
    CMI.units = unit_var02
    ####################################
    
    sat = ds.attribute('platform_ID')
    sat_info = ds.variable('goes_imager_projection')
    lon_sat = sat_info.longitude_of_projection_origin
    hsat = sat_info.perspective_point_height
    
    
    # Setings colours
    ##########################################################
    # import custom_color_palette as ccp
    # import matplotlib.pyplot as plt

    
    # set the colors of the custom palette
    lower_colors = ['maroon','red','darkorange','#ffff00','forestgreen','cyan','royalblue',(148/255,0/255,211/255)]
    lower_colors.reverse()

    lower_palette = [lower_colors, ccp.range(min_var02,max_var02,mini_step02)]


    # pass parameters to the creates_palette module
    # cmap, cmticks, norm, bounds = ccp.creates_palette([lower_palette, upper_palette], extend='both')
    cmap, cmticks, norm, bounds = ccp.creates_palette([lower_palette], extend='both')

    # creating colorbar labels
    ticks = ccp.range(min_var02,max_var02,big_step02)
    
    # Part 03: Plot
    # ###########################
    # import numpy as np
    # import cartopy.crs as ccrs
    # from cartopy.feature import NaturalEarthFeature
    # creates the figure
    plt.switch_backend('Agg') # Esto es para que en ejecucion en paralelo no haya problemas.
    fig = plt.figure('Geo', figsize=(4,4), dpi=200)
    fig.patch.set_facecolor('black')
    
    ax = fig.add_axes([0.1, 0.16, 0.80, 0.75],
                    projection=ccrs.Geostationary(central_longitude=lon_sat, satellite_height=hsat))
    #ax.outline_patch.set_linewidth(0.3)

    #ax = fig.add_subplot(1, 1, 1, projection=geos)

    ax.imshow(RGB, origin='upper',
            extent=(x.min(), x.max(), y.min(), y.max()),
            transform=geos)
    
    ax.coastlines(resolution='50m', color='gold', linewidth=1)
    ax.add_feature(ccrs.cartopy.feature.BORDERS, linewidth=1)
    
    # add the geographic boundaries
    l = NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
    # ax.add_feature(l, edgecolor='gold', linewidth=0.25)
    ax.add_feature(l, edgecolor='black', linewidth=0.25)

    # plot the data
    img = ax.pcolormesh(LonCor.data, LatCor.data, CMI.data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

    # add the colorbar
    # # # cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend='both',
    # # #                 cax=fig.add_axes([0.12, 0.1, 0.76, 0.02]))
    # # # cb.ax.tick_params(labelsize=5, labelcolor='white', width=0.5, length=1.5, direction='out', pad=1.0)
    # # # cb.set_label(label='{} [{}]'.format(CMI.standard_name, CMI.units), size=5, color='white', weight='normal')
    # # # cb.outline.set_linewidth(0.5)

    # set the title
    # ax.set_title('{} - C{:02d} [{:.1f} μm]'.format(sat,band, wl), fontsize=7, loc='left')
    # # # ax.set_title('{} - {} [{}]'.format(sat,selected_product02, unit_var02), fontsize=7, loc='left', color = 'white')
    # # # ax.set_title(CMI.time_bounds.data[0].strftime('%Y/%m/%d %H:%M UTC'), fontsize=7, loc='right', color = 'white')
    
    
    # Sets X axis characteristics
    dx = 15
    xticks = np.arange(domain02[0], domain02[1]+dx, dx)

    # Sets Y axis characteristics
    dy = 15
    yticks = np.arange(domain02[2], domain02[3]+dy, dy)

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
    
    return




############
def convert_nc2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple(input_folder, output_folder, gregorian_date, plot_me, save_me, overwrite):

    print("Start: convert_nc2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple()")
    
    key_png_setup = "f00"
    selected_png_setup = setup_goes16_spi301_MIX01_convert_nc2png_v05(key_png_setup)
    
    key_png_setup01 = "f00"
    selected_png_setup01 = fn076_03_ppi001.setup_goes16_spi076_MCMIPF_convert_nc2png_v01(key_png_setup01)
 
    key_png_setup02 = "dom000"
    selected_png_setup02 = fn067_03_ppi002.dict_setup_NABU(key_png_setup02)

 
    input_paths01, input_paths02, output_paths = fn05.generator_input_and_output_paths_nc2png_MIX01(selected_png_setup, selected_png_setup01, selected_png_setup02, input_folder, output_folder, gregorian_date)

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
            convert_nc2png_goes16_spi301_MIX01_v05_gen01(selected_input_path01, 
                                                     selected_input_path02,
                                                     selected_output_path,
                                                plot_me, save_me, overwrite)
        
            
    print("Close: convert_nc2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple()")
    
    return



##############################################################################################




def convert_goes16_spi301_ppi005_gen02_OneDay_HardCoded(gregorian_date = None):
    
    print('Start: convert_goes16_spi301_ppi005_gen02_OneDay_HardCoded()')
        
    # User info - Hardcoded
    input_folder = '02.download_goes16_OrigProj_nc_files/'
    output_folder  = '04.png/' 
    plot_me = False 
    save_me = True
    overwrite = False
    
    
    # Create folder
    fn01.create_folder_if_not_exists(output_folder)
    
    # Download - gen02
    convert_nc2png_goes16_spi301_MIX01_v05_gen02_OneDay_Simple(input_folder, output_folder, gregorian_date, plot_me, save_me, overwrite)

    print('Close: convert_goes16_spi301_ppi005_gen02_OneDay_HardCoded()')
    
    return



