import sys

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01

import os
import re
import importlib


def sp_gen02_spixxx_plotxxx_OneDay_Hardcoded(gregorian_date, spixxx, plotxxx):
    
    print("Start: sp_gen02_spixxx_plotxxx_OneDay_Hardcoded()")


    files_in_folder = os.listdir(fn_folder)
            
    patron_ext_py = re.compile(r'^fnB\d{3}_03_')
    patron01= re.compile(r'^.*2png_.*$')

    filtered_files = [selected_file for selected_file in files_in_folder
                            if selected_file.endswith('.py') 
                            and patron_ext_py.match(selected_file) 
                            and patron01.match(selected_file)
                            and spixxx in selected_file
                            and plotxxx in selected_file]

    filtered_files = sorted(filtered_files)


    module_name = [os.path.splitext(x)[0] for x in filtered_files]
    str_module_name = module_name[0]


    module_up_action = importlib.import_module(str_module_name)

    # Si la función está definida en el módulo, llamala
    if not hasattr(module_up_action, 'sp_gen02'):
        print(f"La función 'sp_gen02' no está definida en {str_module_name}")
        return
    else: 
        module_up_action.sp_gen02(gregorian_date)


    print("Close: sp_gen02_spixxx_plotxxx_OneDay_Hardcoded()")

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


