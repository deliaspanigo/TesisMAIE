import sys

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01


import os
import re
import importlib


def sp_gen02_spixxx_OneDay_Hardcoded(gregorian_date, spixxx):
    

    archivos_en_carpeta = os.listdir(fn_folder)

  
    patron_ext_py = re.compile(r'^fnB\d{3}')
    patron01= re.compile(r'^.*_setup.*$')
    patron02= re.compile(r'^.*_convert_nc2tiff.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                            if archivo.endswith('.py') 
                            and spixxx in archivo
                            and patron_ext_py.match(archivo) 
                            #and patron01.match(archivo)
                            ]

    archivos_filtrados = sorted(archivos_filtrados)

    file_setup = [archivo for archivo in archivos_filtrados
                            if patron01.match(archivo)][0]

    file_action = [archivo for archivo in archivos_filtrados
                            if patron02.match(archivo)][0]



        
    module_name_setup = os.path.splitext(file_setup)[0]
    module_name_action = os.path.splitext(file_action)[0]

    module_up_setup = importlib.import_module(module_name_setup)
    module_up_action = importlib.import_module(module_name_action)
    
    
        
        
    # Si la función está definida en el módulo, llamala
    if not hasattr(module_up_setup, 'hard_setup_03_nc2tiff'):
        print(f"La función 'standard_output_OneDay_Hardcoded' no está definida en {module_name_action}")
    #else: 
    #    return 

    if not hasattr(module_up_action, 'standard_input_OneDay_Hardcoded'):
        print(f"La función 'standard_input_OneDay_Hardcoded' no está definida en {module_name_action}")
    #else: 
    #    return 
            
    if not hasattr(module_up_action, 'standard_output_OneDay_Hardcoded'):
        print(f"La función 'hard_setup_03_nc2tiff' no está definida en {module_name_setup}")
    #else: 
    #    return 

    if not hasattr(module_up_action, 'sp_gen01'):
        print(f"La función 'sp_gen01' no está definida en {module_name_setup}")
    #else: 
    #    return 
                
    info_setup_nc2tiff = module_up_setup.hard_setup_03_nc2tiff()
    info_input =   module_up_action.standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  module_up_action.standard_output_OneDay_Hardcoded(gregorian_date)

            
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
            module_up_action.sp_gen01(selected_input_path, selected_output_path)
        
        print("\n")
        
    print("Close: sp_gen02_OneDay_Hardcoded()")
        
    del module_up_setup  # Elimina la referencia al modulo
    del module_up_action
    
    return



def sp_gen02_spiALL_OneDay_Hardcoded(gregorian_date):
    
    
    archivos_en_carpeta = os.listdir(fn_folder)
        
    patron_ext_py = re.compile(r'^fnB\d{3}_02_')
    patron01= re.compile(r'^.*_convert_nc2tiff.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                            if archivo.endswith('.py') and patron_ext_py.match(archivo) and patron01.match(archivo)]

    archivos_filtrados = sorted(archivos_filtrados)
    
    
    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]
    patron = r'spi(\d{3})'
    #coincidencia = re.search(patron, cadena)

    list_spi = [re.search(patron, x).group(0) for x in module_name]
    list_spi = sorted(list_spi)
    
    
    for spixxx in list_spi:
    
        sp_gen02_spixxx_OneDay_Hardcoded(gregorian_date, spixxx)
        
    return


