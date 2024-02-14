import sys

fn_folder = '01.own_resources/01.python_code/01.functions/'
# fn_folder = "."
sys.path.append(fn_folder)
import fn01_generic as fn01
import fn07_goes16_mp4_generic as fn07_mp4
import fnA99_01_general_setup as fnA99_01_gs
import fnD_03_gen02_spiALL_OneDay_convert_png as fnD_03_png


import sys
import os 
import re
import time
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
    
    info_setup = fnA99_01_gs.hard_setup_00_general_folders()
    info_png_output = module_up_action.standard_output_OneDay_Hardcoded(gregorian_date)
    
    general_output_folder = info_setup["mp4_oneday"]
    general_input_folder =  info_setup["png"]
    
    input_folder = info_png_output["output_folder"]
    output_folder = input_folder.replace(general_input_folder, general_output_folder)
    
        
    print('Details: {}'.format(info_png_output["spi_and_name_01"]))
    print('input_folder: {}'.format(input_folder))
    print('output_folder: {}'.format(output_folder))
    print('spixxx: {}'.format(spixxx))
    print('plotxxx: {}'.format(plotxxx))
    
    print("\n")
        
    fn01.create_folder_if_not_exists(output_folder)

    
    
    list_spected_input_paths = info_png_output["list_spected_output_paths"]
    
     
    if (len(list_spected_input_paths) == 0):
        print("No hay archivos esperados definidos previamente.")
        return
   
    dt_at_folder = [os.path.exists(x) for x in list_spected_input_paths]
    list_obs_files_at_folder  = [elemento for elemento, condicion in zip(list_spected_input_paths, dt_at_folder) if condicion]

    if (len(list_obs_files_at_folder) == 0):
        print("Los archivos esperados no se encuentran en la carpeta.")
        return
    
    
    output_path = re.sub(re.compile(r"\.png$"), ".mp4", list_obs_files_at_folder[0])
    output_path = output_path.replace(input_folder,output_folder)
    print(output_path)
    
    
    dt_action = not os.path.exists(output_path)
    
    if dt_action:
        fn07_mp4.convert_list_paths_png2mp4_gen01(image_paths = list_spected_input_paths,
                                                    output_path = output_path)
        
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
    #print(archivos_filtrados)
    
    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]

    #print(module_name)
    
    patron = r'plot(\d{3})'    
    #list_spi = [re.search(patron, x) for x in module_name]
    list_plot = [re.search(patron, x).group(0) for x in module_name if re.search(patron, x)]
    
    list_plot = sorted(list_plot)
    
    # print(list_plot)
    
    for plotxxx in list_plot:
    
        sp_gen02_spixxx_plotxxx_OneDay_Hardcoded(gregorian_date, spixxx, plotxxx)
        
    return



def sp_gen02_spiALL_plotALL_OneDay_Hardcoded(gregorian_date):
    archivos_en_carpeta = os.listdir(fn_folder)
            
    patron_ext_py = re.compile(r'^fnB\d{3}_03_')
    patron01= re.compile(r'^.*2png_.*$')
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
    #print(archivos_filtrados)

    module_name = [os.path.splitext(x)[0] for x in archivos_filtrados]

    #print(module_name)


    patron = r'spi(\d{3})'     
    list_spi = [re.search(patron, x).group(0)  for x in module_name]
    list_spi = list(set(sorted(list_spi)))

    #list_plot = [re.search(patron, x).group(0) for x in module_name if re.search(patron, x)]



    # print(list_spi)

    for spixxx in list_spi:

        sp_gen02_spixxx_plotALL_OneDay_Hardcoded(gregorian_date, spixxx)
        
    return


