
# # # Libraries
from pathlib import Path
import fnA99_01_general_setup as fnA99_gs




    
def hard_setup_01_spi():
    pdict = {
        "spi": "076",
        "sat_name": "goes16",
        "abrev_name_01": "MCMIPF",
        "abrev_name_02": "MCMIPF",
        "sensor_name":"ABI",
        "level": "L2"
    }
    pdict["sat_prod"] = "-".join([pdict["sensor_name"], pdict["level"], pdict["abrev_name_01"]])
    pdict["spi_full"] = "spi" + pdict["spi"]
    pdict["spi_and_name_01"] = " - ".join([pdict["spi_full"], pdict["abrev_name_01"]])
    pdict["spi_and_name_02"] = "_".join([pdict["spi_full"], pdict["sat_prod"]])
    return pdict
    
    

def hard_setup_02_download():
    
    general_folders = fnA99_gs.hard_setup_00_general_folders()
    info_spi = hard_setup_01_spi()
    
    
    pdict = {
        "spi_and_name_01": info_spi["spi_and_name_01"],
        "sat_name": info_spi["sat_name"],
        "sat_prod": info_spi["sat_prod"],
        "abrev_name_01": info_spi["abrev_name_01"],
        "abrev_name_02": info_spi["abrev_name_02"],
        "general_input_folder": '',
        "input_ext_file": "",
        "general_output_folder": general_folders["download"],
        "subfolder01": info_spi["spi_and_name_02"],
        "output_ext_file": ".nc",
        "time_files": [str(i).zfill(2) + "0020" for i in range(24)],
        "overwrite": False
    }

    list_special_output_folder = [pdict["general_output_folder"], pdict["subfolder01"]]
    pdict["special_output_folder"] = str(Path(*list_special_output_folder))
    pdict["spected_len_files"] = 24
    pdict["general_prefix_file"] = "OR_ABI-L2-MCMIPF-M6_G16_s"
    return pdict




def hard_setup_03_nc2tiff():
    info_download = hard_setup_02_download()
    info_general_folders = fnA99_gs.hard_setup_00_general_folders()

    pdict = {
        "spi_and_name_01": info_download["spi_and_name_01"],
        "sat_name": info_download["sat_name"],
        "sat_prod": info_download["sat_prod"],
        "abrev_name_01": info_download["abrev_name_01"],
        "abrev_name_02": info_download["abrev_name_02"],
        "general_input_folder": info_download["general_output_folder"],
        "input_ext_file": info_download["output_ext_file"],
        "general_output_folder": info_general_folders["nc2tiff"],
        "output_ext_file": ".tiff",
        "time_files":  info_download["time_files"],
        "overwrite": False,
        "subfolder01":  info_download["subfolder01"]

    }

    list_special_output_folder = [pdict["general_output_folder"], pdict["subfolder01"]]
    pdict["special_output_folder"] = str(Path(*list_special_output_folder))
    pdict["spected_len_files"] = info_download["spected_len_files"]
    pdict["general_prefix_file"] = info_download["general_prefix_file"]
    
    
    return pdict



def hard_setup_04_png():
    info_download = hard_setup_02_download()
    info_nc2tiff = hard_setup_03_nc2tiff()
    info_general_folders = fnA99_gs.hard_setup_00_general_folders()

    pdict = {
        "spi_and_name_01": info_nc2tiff["spi_and_name_01"],
        "sat_name": info_nc2tiff["sat_name"],
        "sat_prod": info_nc2tiff["sat_prod"],
        "abrev_name_01": info_nc2tiff["abrev_name_01"],
        "abrev_name_02": info_nc2tiff["abrev_name_02"],
        "general_input_folder": info_nc2tiff["general_output_folder"],
        "input_ext_file_01": info_download["output_ext_file"],
        "input_ext_file_02": info_nc2tiff["output_ext_file"],
        
        "general_output_folder": info_general_folders["png"],
        "output_ext_file": ".png",
        
        "output_proj_01": "OrigProj",
        "output_proj_02": "WGS84Proj",
        
        "time_files":  info_nc2tiff["time_files"],
        "overwrite": False,
        "subfolder01":  info_nc2tiff["subfolder01"]

    }

    list_special_output_folder = [pdict["general_output_folder"], pdict["subfolder01"]]
    pdict["special_output_folder"] = str(Path(*list_special_output_folder))
    pdict["spected_len_files"] = info_nc2tiff["spected_len_files"]
    pdict["general_prefix_file"] = info_nc2tiff["general_prefix_file"]
    
    
    return pdict


