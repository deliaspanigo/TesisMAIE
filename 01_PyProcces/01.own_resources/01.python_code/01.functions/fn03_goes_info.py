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


import sys
from io import StringIO
import GOES
import pandas as pd


def info_goes16_NABU_product_names():
    
    info_product_name = ['ABI-L2-ACMF', 'ABI-L2-MCMIPF',
                         'ABI-L2-FDCC', 'ABI-L2-FDCF', 
                         'ABI-L2-LSTF', 'GLM-L2-LCFA']
    
    info_product_name = sorted(info_product_name)
    return(info_product_name)


def info_goes16_NABU_product_index():
    lst_index = [prod_index_goes(sat_name = "goes16", str_name = x) for x in info_goes16_NABU_product_names()]
    
    output_lst = []
    for sublist in lst_index:
        output_lst.extend(sublist)
    
    return output_lst
    

def info_goes16_NABU_service_details():

    prod_name = info_goes16_NABU_product_names()
    prod_index = info_goes16_NABU_product_index()


    # Convert each number to a string with three digits
    order_index = range(len(prod_name))
    index_mod = [str(number).zfill(3) for number in prod_index]
    names_mod = [name.split("-")[-1] for name in prod_name]
    fn_names = ["fn" + x for x in index_mod]

    output_dict = {}
    for x in range(len(prod_name)):
        my_dict = {"order_index": order_index[x] + 1,
                   "sat_name": "goes16",
                "prod_name": prod_name[x],
                "prod_index": prod_index[x],
                "names_mod": names_mod[x],
                "index_mod": index_mod[x],
                "fn_names": fn_names[x]}
        output_dict[str(x)] = my_dict  # Corrección aquí

    return output_dict


def products_goes16():
    return products_goes_all_list(sat_name = "goes16")


def products_goes_all_list(sat_name = None):
    

    # Redirect standard output to a StringIO object
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Call the function that prints
    GOES.show_products()

    # Get the output as a string
    output_as_string = sys.stdout.getvalue()

    # Restore the original standard output
    sys.stdout = original_stdout


    # Get the output as a list
    output_as_list = output_as_string.splitlines()
    output_as_list = [elemento.replace('\t', '') for elemento in output_as_list]


    list_init = ["Products for goes16:", "Products for goes17:", "Products for goes18:"]
    list_fin = " "
    list_name = ["goes16", "goes17", "goes18"]
    
    index_init = [output_as_list.index(x) for x in list_init]
    index_fin =  [i for i, elemento in enumerate(output_as_list) if elemento == list_fin]
    index_fin.pop(0)
    


    output_list = []
    for x in range(len(index_init)):
        # Realizar la subselección
        subseleccion = output_as_list[(index_init[x] + 1):index_fin[x]]

        output_list.append(subseleccion)
        
    #return output_list

    # # Convertir cada lista interna en un DataFrame y agregarlo a la lista
    # dataframes_lista = []
    # for x in range(len(total_output)):
    #     df = pd.DataFrame(total_output[x])
    #     df.columns = [name_list[x]]
    #     dataframes_lista.append(df)

    #Convertir la lista de DataFrames en un diccionario
    diccionario_list = dict(zip(list_name, output_list))
    
    if sat_name  == None:
       return diccionario_list
    else:
       return diccionario_list[sat_name]
   
   
   
def prod_index_goes(sat_name, str_name):
    all_prod_goes_selected = products_goes_all_list(sat_name)
    index_lst = [i for i, element in enumerate(all_prod_goes_selected) if str_name in element]
    return index_lst 


def prod_name_goes(sat_name, str_name):
    all_prod_goes_selected = products_goes_all_list(sat_name)
    index_lst = prod_index_goes(sat_name, str_name)
    name_lst = [all_prod_goes_selected[x] for x in index_lst]
    return name_lst

