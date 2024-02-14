
# Own libraries
import fn01_generic as fn01
import fnA99_02_general_functions_for_fnB as fnA99_gf
import fnB067_00_goes16_spi067_LSTF_setup as fnB067_00_setup
import fnB067_01_goes16_spi067_LSTF_download as fnB067_01_download

# # # Libraries
import os
import re
import rioxarray as rxr





def standard_input_OneDay_Hardcoded(gregorian_date = None):

    info_download_input =  fnB067_01_download.standard_input_OneDay_Hardcoded(gregorian_date)
    info_download_output =  fnB067_01_download.standard_output_OneDay_Hardcoded(gregorian_date)
    
    
    input_folder = info_download_output["output_folder"]
    list_spected_input_files = info_download_output["list_spected_output_files"]
    list_spected_input_paths = info_download_output["list_spected_output_paths"]
    
    
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_download_output["spi_and_name_01"],
        "input_folder": input_folder,
        "list_spected_input_files": list_spected_input_files,
        "list_spected_input_paths": list_spected_input_paths
    }
    
    return pdict
    

def standard_output_OneDay_Hardcoded(gregorian_date = None):
    
    info_setup_nc2tiff = fnB067_00_setup.hard_setup_03_nc2tiff()
    info_input_nc2tiff =  standard_input_OneDay_Hardcoded(gregorian_date)
    
    info_output_download =  fnB067_01_download.standard_input_OneDay_Hardcoded(gregorian_date)
    
    # # # Spected output file names for download files
    input_folder = info_input_nc2tiff["input_folder"]
    output_folder = fnA99_gf.str_nc2tiff_output_folder(gregorian_date, fnB067_00_setup)
    
    # # # Initial info
    list_spected_input_files = info_input_nc2tiff["list_spected_input_files"]
    list_spected_input_paths = info_input_nc2tiff["list_spected_input_paths"]
    ext_input_file =  info_setup_nc2tiff["input_ext_file"]
    ext_output_file = info_setup_nc2tiff["output_ext_file"]
    
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
    
    
    # dt for apply download file or not
    if len(list_observed_output_files) == 0:
        list_dt_action_files = [True]*len(list_spected_output_files)
    else:
        list_dt_action_files = [not spected_file in list_observed_output_files for spected_file in list_spected_output_files]

    # dt wrong files at folder
    if len(list_observed_output_files) == 0:
        list_dt_wrong_files = []
        list_wrong_files = None
    else:
        list_dt_wrong_files = [not observed_file in list_spected_output_files for observed_file in list_observed_output_files]
        list_wrong_files = [selected_obs_file for selected_obs_file, selected_dt in zip(list_observed_output_files, list_dt_action_files) if selected_dt]

    
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_setup_nc2tiff["spi_and_name_01"],
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
def sp_gen01(input_path, output_path):

    print("Start: convert_nc2tiff_gen01()")
    
    # Se establece el la referencia espacial y se define en el archivo
    selected_epsg = "EPSG:4326"
    spatial_ref = 'PROJCS["unnamed",GEOGCS["unknown",DATUM["unnamed",SPHEROID["Spheroid",6378137,298.2572221]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Geostationary_Satellite"],PARAMETER["central_meridian",-75],PARAMETER["satellite_height",35786023],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],EXTENSION["PROJ4","+proj=geos +lon_0=-75 +h=35786023 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs +sweep=x"]]'

 
    
    # Open .nc file
    new_tiff = rxr.open_rasterio(input_path, mask_and_scale=True)

    
    # General changes
    new_tiff = new_tiff.rio.set_crs(spatial_ref)         # CRS
    new_tiff = new_tiff.rio.reproject(selected_epsg) # EPSG
    new_tiff = new_tiff.astype(float)  # Float 64 para todas las bandas
    new_tiff = new_tiff.rio.write_crs(selected_epsg, inplace=True)  # 
    

    
    # Selected band changes
    new_tiff['LST'][0] = new_tiff['LST'][0] - 273.15   # Pasamos de Kelvin a Celcius
    new_tiff['LST'][0] = new_tiff['LST'][0].fillna(-9999)

    new_tiff['LST'].attrs["units"] = "C"
    
    # if domain is not None:
    #     # # Clip por bbox
    #     new_tiff['LST'] = new_tiff['LST'].rio.clip_box(
    #         minx=domain[0],
    #         miny=domain[2],
    #         maxx=domain[1],
    #         maxy=domain[3],
    #         crs=selected_epsg,
    #     )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    new_tiff.LST.rio.to_raster(output_path)

    
    
    
    # nc_mod
    # nc_original.close()
    new_tiff.close()
    
    print("Close: convert_nc2tiff_gen01()")
    return





def sp_gen02_OneDay_Hardcoded(gregorian_date):

    print('Start: gen02_OneDay_Hardcoded()')
    print("Selected gregorian day: {}".format(gregorian_date))
    
    info_setup_nc2tiff = fnB067_00_setup.hard_setup_03_nc2tiff()
    info_input =  standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  standard_output_OneDay_Hardcoded(gregorian_date)

    
    print('Details: {}'.format(info_output["spi_and_name_01"]))
    print('output_folder: {}'.format(info_output["output_folder"]))
    print("\n")
        
    fn01.create_folder_if_not_exists(info_output["output_folder"])
    
    list_spected_input_paths = info_input["list_spected_input_paths"]
    list_spected_output_paths = info_output["list_spected_output_paths"]
    list_dt_action_files = info_output["list_dt_action_files"]
    list_time_files = info_setup_nc2tiff["time_files"]
    
    
    len_files = len(list_spected_input_paths) 
   
    # For each input file...
    for x in range(len_files):
        
        selected_input_path = list_spected_input_paths[x]
        selected_output_path = list_spected_output_paths[x]
        selected_dt_action = list_dt_action_files[x]
        
        if not selected_dt_action: 
            new_detail = "File exists!"
        elif selected_dt_action:
            new_detail = "In progress..."
            
        print(f'Convertion... nc2tiff {x+1} of {len_files} - {new_detail}')

        if selected_dt_action or info_setup_nc2tiff["overwrite"]:
            sp_gen01(selected_input_path, selected_output_path)
        
        print("\n")
        
    print("Close: sp_gen02_OneDay_Hardcoded()")
    
    return


