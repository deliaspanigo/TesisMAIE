# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # functions03_goes_download.py
# Funciones en relacion a:
# - gen00: simple download without function
# - gen01: gen00 inside a function
# - gen02: gen01 + control de preexistencia y de conexion a internet
# - gen03: gen02 + stock


# Own libreries
import fn01_generic as fn01
import fn02_time as fn02


# # # Libreries
from itertools import compress
from natsort import natsorted
import os
from s3fs import S3FileSystem


# # # GOES functions -------------------------------------------------------------------


def list_available_files_from_goes(bucket_name, product_name, julian_year, julian_day):
    fs = S3FileSystem(anon=True)

    # Construir la ruta completa con el año y el día juliano especificados
    prefix = f'{bucket_name}/{product_name}/{julian_year}/{julian_day}'

    # Obtener la lista de archivos en la ruta especificada
    files = fs.ls(prefix)
    files = natsorted(files)
    
    

    return files



def list_available_files_from_goes_mod(fs, bucket_name, product_name, julian_year, julian_day, general_sufix):
    #
    # fs = S3FileSystem(anon=True)

    # Construir la ruta completa con el año y el día juliano especificados
    prefix = f'{bucket_name}/{product_name}/{julian_year}/{julian_day}'

    # Obtener la lista de archivos en la ruta especificada
    files = fs.ls(prefix)
    files = natsorted(files)
    
    if len(files) > 0:
        dt_lvl = general_sufix in files[0]
        
        if not dt_lvl:
            ##############################################
            files02 = [fs.ls(x) for x in files]

            from itertools import chain
            files03 = list(chain.from_iterable(files02))

            files03 = natsorted(files03)

            files = files03
            ##############################################
            
            
    return files


def download_goes_gen01(selected_goes_info, download_folder):

    try:
        file_name = os.path.basename(selected_goes_info)
        file_path_local = download_folder + file_name
                
        fs = S3FileSystem(anon=True)
        download_file = fs.ls(selected_goes_info, refresh=True)
              
        if len(download_file) == 0:
            print("Wrong goes_info details or file is not avairable in AWS.") 
            
        fs.get(download_file, download_folder)

        print(f"Successful download: {download_file} -> {download_folder}")
        return True

    except Exception as e:
        # Maneja excepciones específicas relacionadas con la pérdida de conexión a Internet aquí
        if "ConnectionError" in str(e) or "TimeoutError" in str(e):
            print("Internet connection lost during download.")
            if os.path.exists(file_path_local):
                print("File downloaded incompletely.")
                print("Deleting file...")
                fn01.delete_file(file_path_local)
                print("Deleted file.")
                
            
        else:
            print(f"Error during download: {str(e)}")
            print(f"Review goes_info: {selected_goes_info}")
            if os.path.exists(file_path_local):
                print("File downloaded incompletely.")
                print("Deleting file...")
                fn01.delete_file(file_path_local)
                print("Deleted file.")
            
        return False




def download_goes_gen02(selected_new_path_local, selected_av_path_aws, selected_av_size_aws):
    

    
    print(f'-Starting download_goes_gen02()')
    
    goes_info = os.path.dirname(selected_av_path_aws)
    selected_av_folder_local = os.path.dirname(selected_new_path_local) + "/"
    new_file = os.path.basename(selected_av_path_aws)
    new_file_extention = os.path.splitext(new_file)[1]
    
    print(f'-GOES info: {goes_info}') 
    print(f'-File name: {new_file}') 
    print(f'-AWS path: {selected_av_path_aws}')
    print(f'-Local download folder: {selected_av_folder_local}')
    print(f'-Local path: {selected_new_path_local}')
    
    
    # Control 01 - File extention ".nc"
    dt_nc_file = new_file_extention == ".nc"
    print(f"-Control 01: File extention is '.nc': {dt_nc_file}")

    if not dt_nc_file:
        print("     -File extention is '{new_file_extention}'.")
        print("     -File extention must be '.nc'.")
        print("     -File will be not downloaded.")
        print("\n")
        return
    
    # Control 01 - Preexistencia del archivo
    dt_preexistence = not os.path.exists(selected_new_path_local)
    print(f"-Control 02: No previous file existence: {dt_preexistence}")

    if not dt_preexistence:
        print("     -File exist at folder.")
        print("     -File will be not downloaded.")
        print(f'-Ending download_goes_gen02()')  
        print("\n")
        return




    # Control 02 - Check internet
    with fn01.suppress_output():
        dt_conection = fn01.check_internet_connection()
    print(f"-Control 03: Internet Conection: {dt_conection}")
    
    if not dt_conection:
        print(f"    -Conexion problem!.")
        print(f"    -Canceled download.")
        print(f'-Ending download_goes_gen02()')  
        print("\n")
        return
                    
    # Download 
    print("-    Starting download_goes_gen01()...")
    print("-    Downloading...")
    with fn01.suppress_output():
        download_goes_gen01(selected_av_path_aws, selected_av_folder_local)
    print("-    File downloaded.")
    print("-    Finished download_goes_gen01()...")


    # Control 03 - Archivo en carpeta    
    dt_postexistence = os.path.exists(selected_new_path_local)
    print(f"-Control 04: File at local download folder: {dt_postexistence}")

    if not dt_postexistence:
        print("-    File had been download, but is not at local folder!.")
        print("-    Download error or wrong local download folder.")
        print(f'-Ending download_goes_gen02()')  
        return 


    # Control 03 - Tamanio del archivo        
    obs_file_size = fn01.calculate_file_size_in_bytes(selected_new_path_local)
    dt_size = selected_av_size_aws == obs_file_size
    
    print(f"-Control 05: Correct file size: {dt_size}")
    print(f"    -File Size - AWS:   {selected_av_size_aws} bytes")
    print(f"    -File Size - Local: {obs_file_size} bytes")
        
    if not dt_size:
        print(" -Incompleted file download.")
        print(" -Deleting file...")
        fn01.delete_file(selected_new_path_local)
        print(" -Deleted file.")
        print(f'-Ending download_goes_gen02()')  
        return 

    print(f'-Download and controls done.')       
    print(f'-Ending download_goes_gen02()')  
    print("\n")  
    return



def download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix):
        
    print(f"Starting download_goes_gen03()")
    
    
    # # # Section 01 - Dates details
    print(f"Section01 - General Information:")
    julian_date_SEP    = fn02.gregorianSEP_to_julianSEP(gregorian_date = gregorian_date_SEP, date_separator='-')
    julian_year =  fn01.clip_first_segment(selected_string  =  julian_date_SEP, sep = "-")
    julian_day =   fn01.clip_last_segment(selected_string   =  julian_date_SEP, sep = "-")
    julian_date_COMP = julian_year + julian_day
    new_folder = fn02.gregorianSEP_to_newfolder(gregorian_date_SEP) 
    
    
    # Print Section 01
    print(f"Julian Date: {julian_date_SEP}")
    print(f"Gregorian Date: {gregorian_date_SEP}")
    print(f"Full Date: {new_folder}")
    print(f"Root folder: {root_folder}")
    # print(f"Special prefix for files: {special_prefix}")
    print(f"General sufix for files: {general_sufix}")
    print("\n")
    
    #######################################################################################################
    
    # Control 01 - Check internet
    with fn01.suppress_output():
        dt_conection = fn01.check_internet_connection()
    print(f"-Control01 gen03() - Internet Conection: {dt_conection}")
    
    if not dt_conection:
        print(f"    -Conexion problem!.")
        print(f"    -Canceled download.")
        print(f"-Ending download_goes_gen03()")
        print("\n")
        return
        

    
    ######################################################################################################
    
    
    
    # # # Section 02 - # Avairable files AWS
    print(f"-Searching GOES-16 files at AWS.")
    fs = S3FileSystem(anon=True)
    av_paths_aws = list_available_files_from_goes_mod(fs, bucket_name, product_name, julian_year, julian_day, general_sufix)
    av_folders_aws = [os.path.dirname(x) for x in av_paths_aws]
    av_files_aws = [os.path.basename(x)  for x in av_paths_aws]
    av_sizes_aws = [fs.info(x)["size"]    for x in av_paths_aws]


    # Avairable folders localy
    av_folders_local = [root_folder + x + "/" for x in av_folders_aws] 
    av_unique_folders_local = list(set(av_folders_local))


    # Observed paths and files at local folder
    obs_paths_local = fn01.get_unique_file_paths_from_list(av_unique_folders_local)
    obs_files_local = [os.path.basename(selected_str_file) for selected_str_file in obs_paths_local]


    # Detection file to be downloaded
    # Detection for each av_files_aws in list av_files_local
    dt_files_at_folder = [x in obs_files_local  for x in av_files_aws]


    # Detection for av_files_aws must be donloaded
    dt_files_download = [not x for x in dt_files_at_folder]


    # OK - files to will be downloaded
    ok_av_paths_aws = list(compress(av_paths_aws, dt_files_download))
    ok_av_folders_aws = list(compress(av_folders_aws, dt_files_download))
    ok_av_files_aws = list(compress(av_files_aws, dt_files_download))
    ok_av_sizes_aws = list(compress(av_sizes_aws, dt_files_download))
    
    # OK - local folders for earh AWS file
    ok_av_folders_local = list(compress(av_folders_local, dt_files_download))

    # New path in folder (future path to save download locally)
    ok_new_paths_local = [ok_av_folders_local[x] + ok_av_files_aws[x] for x in range(len(ok_av_files_aws))]

    # Counts
    count_at_aws = len(av_paths_aws)
    count_at_local = sum(dt_files_at_folder)
    count_to_download = len(ok_av_paths_aws)


    count_max =  max(count_at_aws, count_at_local, count_to_download)
    count_digits = len(str(count_max))
    formato = f"{{:{count_digits}d}}"  # Le agrega espacios a la izquierda
    formato2 = f"{{:0{count_digits}d}}"  # Le agrega ceros a la izquierda
    
    # Download action detection
    dt_action = count_to_download > 0 
       
    print(f"-Control02 gen03() - Files avairable to download: {dt_action}")        
    print(f"    -Total AWS files avairable:             {formato.format(count_at_aws)}")
    print(f"    -Total files at own server:             {formato.format(count_at_local)}")
    print(f"    -Total files to be downloaded from AWS: {formato.format(count_to_download)}")
    print("\n")
   
    if not dt_action:
        print("There are no new avairable files to download from AWS.")    
        return
        
        
    for pos_cycle in range(count_to_download):    
    
        print(f"-GOES download stock {formato2.format(pos_cycle+1)} of {formato2.format(count_to_download)}")
        
        # Selected AWS
        selected_av_path_aws = ok_av_paths_aws[pos_cycle]
        selected_av_file_aws = ok_av_files_aws[pos_cycle]
        selected_av_size_aws = ok_av_sizes_aws[pos_cycle]

        # Selected local
        selected_new_path_local = ok_new_paths_local[pos_cycle]
        
       
        # Download 
        download_goes_gen02(selected_new_path_local, selected_av_path_aws, selected_av_size_aws)
    
    print(f"Ending download_goes_gen03()")
    return




