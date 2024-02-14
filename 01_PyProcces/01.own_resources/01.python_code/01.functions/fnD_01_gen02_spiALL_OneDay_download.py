
# # # Own libraries
import sys
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01

# # # Import libraries
import os
import re
import importlib

def sp_gen02_spiALL_OneDay_Hardcoded(gregorian_date = None):
    
    archivos_en_carpeta = os.listdir(fn_folder)
    
    patron_ext_py = re.compile(r'^fnB\d{3}_01_')
    patron01= re.compile(r'^.*_download.*$')

    archivos_filtrados = [archivo for archivo in archivos_en_carpeta
                          if archivo.endswith('.py') and patron_ext_py.match(archivo) and patron01.match(archivo)]
    
    archivos_filtrados = sorted(archivos_filtrados)

    for archivo in archivos_filtrados:
        module_name = os.path.splitext(archivo)[0]
        # import_statement = f"import {module_name} as fnBxxx_01_download"
        module = importlib.import_module(module_name)
        

        # Si la función está definida en el módulo, llamala
        if hasattr(module, 'sp_gen02_OneDay_Hardcoded'):
            module.sp_gen02_OneDay_Hardcoded(gregorian_date)
        else:
            print(f"La función 'sp_gen02_OneDay_Hardcoded' no está definida en {module_name}")

        del module  # Elimina la referencia al modulo
        
    return
