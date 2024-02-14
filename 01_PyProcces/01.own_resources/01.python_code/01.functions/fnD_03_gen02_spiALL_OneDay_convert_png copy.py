import sys

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01

import os
import re
import importlib


def sp_gen02_spixxx_plotxxx_OneDay_Hardcoded(gregorian_date, spixxx, plotxxx):
    
    archivos_en_carpeta = os.listdir(fn_folder)
            
    patron_ext_py = re.compile(r'^fnB\d{3}_03_')
    patron01= re.compile(r'^.*2png_.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                            if archivo.endswith('.py') 
                            and patron_ext_py.match(archivo) 
                            and patron01.match(archivo)
                            and spixxx in archivo
                            and plotxxx in archivo]

    archivos_filtrados = sorted(archivos_filtrados)


    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]
    str_module_name = module_name[0]


    module_up_action = importlib.import_module(str_module_name)

    # Si la función está definida en el módulo, llamala
    if not hasattr(module_up_action, 'standard_plot_Hardcoded'):
        print(f"La función 'standard_plot_Hardcoded' no está definida en {str_module_name}")
    #else: 
    #    return 

    # Si la función está definida en el módulo, llamala
    if not hasattr(module_up_action, 'standard_input_OneDay_Hardcoded'):
        print(f"La función 'standard_input_OneDay_Hardcoded' no está definida en {str_module_name}")
    #else: 
    #    return 

    # Si la función está definida en el módulo, llamala
    if not hasattr(module_up_action, 'standard_output_OneDay_Hardcoded'):
        print(f"La función 'standard_output_OneDay_Hardcoded' no está definida en {str_module_name}")
    #else: 
    #    return 
    
    
    print('Start: sp_gen02_OnePlot_OneDay_Hardcoded()')
    print("Selected gregorian day: {}".format(gregorian_date))


    info_standard_plot = module_up_action.standard_plot_Hardcoded(gregorian_date)
    info_input =  module_up_action.standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  module_up_action.standard_output_OneDay_Hardcoded(gregorian_date)


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
            module_up_action.sp_gen01(selected_input_path, selected_output_path, 
                        plot_me = info_standard_plot["plot_me"], 
                        save_me = info_standard_plot["save_me"],
                        overwrite = info_standard_plot["overwrite"])
        
        print("\n")
        
    print("Close: sp_gen02_OnePlot_OneDay_Hardcoded()")
    
    return
   
   
   
def sp_gen02_spixxx_plotALL_OneDay_Hardcoded(gregorian_date, spixxx):
    
    archivos_en_carpeta = os.listdir(fn_folder)
            
    patron_ext_py = re.compile(r'^fnB\d{3}_03_')
    patron01= re.compile(r'^.*2png_.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                            if archivo.endswith('.py') 
                            and patron_ext_py.match(archivo) 
                            and patron01.match(archivo)
                            and spixxx in archivo]

    archivos_filtrados = sorted(archivos_filtrados)
    print(archivos_filtrados)
    
    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]

    print(module_name)
    
    patron = r'plot(\d{3})'    
    #list_spi = [re.search(patron, x) for x in module_name]
    list_plot = [re.search(patron, x).group(0) for x in module_name if re.search(patron, x)]
    
    list_plot = sorted(list_plot)
    
    print(list_plot)
    
    for plotxxx in list_plot:
    
        sp_gen02_spixxx_plotxxx_OneDay_Hardcoded(gregorian_date, spixxx, plotxxx)
        
    return



def sp_gen02_spiALL_plotALL_OneDay_Hardcoded(gregorian_date):
    archivos_en_carpeta = os.listdir(fn_folder)
            
    patron_ext_py = re.compile(r'^fnB\d{3}_03_')
    patron01= re.compile(r'^.*2png.*$')
    patron02 = re.compile(r'^.*_spi(\d{3})_.*$')
    patron03 = re.compile(r'^.*_plot(\d{3})_.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                            if archivo.endswith('.py') 
                            and patron_ext_py.match(archivo) 
                            and patron01.match(archivo)
                            and patron02.match(archivo)
                            # and patron03.match(archivo)
                            ]

    archivos_filtrados = sorted(archivos_filtrados)
    print(archivos_filtrados)

    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]

    print(module_name)


    patron = r'spi(\d{3})'     
    list_spi = [re.search(patron, x).group(0)  for x in module_name]
    list_spi = list(set(sorted(list_spi)))

    #list_plot = [re.search(patron, x).group(0) for x in module_name if re.search(patron, x)]



    print(list_spi)

    for spixxx in list_spi:

        sp_gen02_spixxx_plotALL_OneDay_Hardcoded(gregorian_date, spixxx)
        
    return


