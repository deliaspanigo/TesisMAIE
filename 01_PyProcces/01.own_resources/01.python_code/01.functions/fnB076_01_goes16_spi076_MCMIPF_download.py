
# Own libraries
import fn01_generic as fn01

import fnA99_02_general_functions_for_fnB as fnA99_gf
import fnB076_00_goes16_spi076_MCMIPF_setup as fnB076_00_setup


# # # Libraries
import os
import GOES






def standard_input_OneDay_Hardcoded(gregorian_date = None):

    info_download =  fnB076_00_setup.hard_setup_02_download()
    
    
    input_folder = None
    input_files = None
    input_paths = None
    
    
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_download["spi_and_name_01"],
        "input_folder": input_folder,
        "input_files": input_files,
        "input_paths": input_paths
    }
    
    return pdict
    

def standard_output_OneDay_Hardcoded(gregorian_date = None):
    
    info_download =  fnB076_00_setup.hard_setup_02_download()
    
    # Spected output file names for download files
    output_folder = fnA99_gf.str_download_output_folder(gregorian_date, fnB076_00_setup)
    str_special = info_download["general_prefix_file"] + gregorian_date
    
    list_spected_output_files = [str_special + x + info_download["output_ext_file"] for x in info_download["time_files"]]
    list_spected_output_paths = [output_folder + x for x in list_spected_output_files]
    
    
    # Local files observed
    list_observed_output_files =   fn01.list_files_in_folder(output_folder)
    list_observed_output_paths =   fn01.list_paths_in_folder(output_folder)
    
    
    # dt for apply download file or not
    if len(list_observed_output_files) == 0:
        list_dt_download_files = [True]*len(list_spected_output_files)
    else:
        list_dt_download_files = [not spected_file in list_observed_output_files for spected_file in list_spected_output_files]

    # dt wrong files at folder
    if len(list_observed_output_files) == 0:
        list_dt_wrong_files = []
        list_wrong_files = None
    else:
        list_dt_wrong_files = [not observed_file in list_spected_output_files for observed_file in list_observed_output_files]
        list_wrong_files = [selected_obs_file for selected_obs_file, selected_dt in zip(list_observed_output_files, list_dt_wrong_files) if selected_dt]

    
    pdict = {
        "gregorian_date": gregorian_date, 
        "spi_and_name_01": info_download["spi_and_name_01"],
        "output_folder": output_folder,
        "len_spected_output_files": len(list_spected_output_files),
        "len_observed_output_files": len(list_observed_output_files),
        "len_wrong_output_files": sum(list_dt_wrong_files),
        "list_spected_output_files": list_spected_output_files,
        "list_spected_output_paths": list_spected_output_paths,
        "list_dt_download_files": list_dt_download_files, 
        "list_observed_output_files": list_observed_output_files, 
        "list_observed_output_paths": list_observed_output_paths,
    #    "list_dt_wrong_files": list_dt_wrong_files,
        "list_wrong_files": list_wrong_files
    }
    
    return pdict
           

# Standard Proccesing (sp) - gen01
def sp_gen01(sat_prod = None, gregorian_date = None, output_folder = None, overwrite = False, time_init = "000000", time_fin = "235959"):
    
    datetimeini = str(gregorian_date) + str("-") + str(time_init)
    datetimefin = str(gregorian_date) + str("-") + str(time_fin)
        
    GOES.download(Satellite='goes16',  Product=sat_prod,     
            DateTimeIni = datetimeini, DateTimeFin = datetimefin, 
            channel = ['01','02','03'], 
            rename_fmt = '%Y%m%d%H%M%S', 
            path_out=output_folder,
            retries = 10,
            backoff = 10,
            size_format = 'Decimal',
            show_download_progress = False,
            overwrite_file = overwrite)

    
    return



# Standard Proccesing (sp) - gen02 - OneDay - Hardcoded   
def sp_gen02_OneDay_Hardcoded(gregorian_date = None):

    print('Start: sp_gen02_OneDay_Hardcoded()')
    print("Selected gregorian day: {}".format(gregorian_date))
    
    info_download =  fnB076_00_setup.hard_setup_02_download()
    info_input =  standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  standard_output_OneDay_Hardcoded(gregorian_date)
    
    
    print('Details: {}'.format(info_output["spi_and_name_01"]))
    print('output_folder: {}'.format(info_output["output_folder"]))
    print("\n")
        
    fn01.create_folder_if_not_exists(info_output["output_folder"])

   
    list_spected_output_files = info_output["list_spected_output_files"]
    list_dt_download_files = info_output["list_dt_download_files"]
    list_time_files = info_download["time_files"]
    
    len_files = len(list_spected_output_files)
        
    for x in range(len_files):
        
        text_out = '{} - {} - {} of {}'.format(info_download["sat_name"], 
                                               info_download["abrev_name_01"],
                                               str(x+1), 
                                               str(len_files))
        
        print(text_out)
        
        dt_download_selected_file = list_dt_download_files[x]
        selected_file = list_spected_output_files[x]
        time_init =  list_time_files[x]
        time_fin  =  time_init
        
        
        if dt_download_selected_file: 
            
           
            try:
                sp_gen01(sat_prod = info_download["sat_prod"],
                            gregorian_date = gregorian_date, 
                            output_folder = info_output["output_folder"],
                            overwrite =  info_download["overwrite"],
                            time_init = time_init, 
                            time_fin = time_fin)
        
                print("\n")
            
            except FileNotFoundError as e:
                print(f"File is not avairable online: {e}")
        else:
            print("Internal control File:")
            print("  {} {}".format(selected_file, "already exists."))      
            print("\n")
    print('Close: sp_gen02_OneDay_Hardcoded()')


    return



