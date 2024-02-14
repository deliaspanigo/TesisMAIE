# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # functions01_generic.py
# Functions in relation to:
# - Folder manipulation
# - String detection and trimming


# # # Libreries
from contextlib import contextmanager
from matplotlib.image import imread
import matplotlib.pyplot as plt
import natsort
import os
import requests
import shutil
import sys

# Funciones

##############################

def init_sep():
    init_sep = "####################################"*2

    return init_sep


def final_sep():
    final_sep = init_sep()
    return final_sep


def plot_path_png(selected_path):
    # Leer el archivo PNG
    imagen = imread(selected_path)

    # Mostrar la imagen en un gráfico
    plt.imshow(imagen)
    plt.axis('off')  # Desactivar los ejes
    plt.show()
    return 




################################################################
def get_unique_file_paths_from_list(folders):
    """
    Get unique file paths from a list of folders.

    Args:
        folders (list): A list of folder paths to explore.

    Returns:
        list: A list of unique file paths found in the specified folders.
    """
    # Initialize a list to store all file paths
    file_paths = []

    # Iterate through the folders and get file paths
    for folder in folders:
        for root_dir, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root_dir, file)
                file_paths.append(file_path)

    # Convert the list into a set to remove duplicates, then back to a list
    unique_file_paths = list(set(file_paths))

    return unique_file_paths

#############################################################
def find_newest_file_position_in_folder(folder_path):
    try:
        # Get a list of files in the folder
        files = os.listdir(folder_path)

        # Initialize variables for the newest file and its position
        newest_file = None
        newest_file_position = None

        # Iterate through the list of files
        for i, file in enumerate(files):
            file_path = os.path.join(folder_path, file)

            # Check if the file exists and is a file (not a directory)
            if os.path.isfile(file_path):
                modification_time = os.path.getmtime(file_path)

                # Check if this file is newer than the previously recorded one
                if newest_file is None or modification_time > newest_file:
                    newest_file = modification_time
                    newest_file_position = i

        # Return the position of the newest file (0-based index)
        if newest_file_position is not None:
            return newest_file_position
        else:
            return None
    except OSError as e:
        print(f"Error while searching for files in the folder: {str(e)}")
        return None


def find_newest_file_position_in_list(file_paths):
    try:
        # Initialize variables for the newest file and its position
        newest_file = None
        newest_file_path = None

        # Iterate through the list of file paths
        for file_path in file_paths:
            # Check if the file exists and is a file (not a directory)
            if os.path.isfile(file_path):
                modification_time = os.path.getmtime(file_path)

                # Check if this file is newer than the previously recorded one
                if newest_file is None or modification_time > newest_file:
                    newest_file = modification_time
                    newest_file_path = file_path

        # Return the path of the newest file
        if newest_file_path is not None:
            return newest_file_path
        else:
            return None
    except OSError as e:
        print(f"Error while processing files: {str(e)}")
        return None

###########################################################################################
def delete_folder(folder_path):
    try:
        # Use the shutil.rmtree() function to delete the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been successfully deleted.")
        #return True

    except Exception as e:
        print(f"Error while deleting the folder: {str(e)}")
        #return False

    return

###############################################################################
@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as null_file:
        original_stdout = sys.stdout
        sys.stdout = null_file
        yield
        sys.stdout = original_stdout
################################################################################


def delete_file(file_path):
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error while deleting the file: {str(e)}")
        
        
# # # Create Folders and files ---------------------------------------------------------------


def ST01_create_folder_structure(dir_root):
    
    new_folders = ["data", "img", "png"]
    
    for x in new_folders:
        new_folder = dir_root + x
        create_folder_if_not_exists(new_folder)
    
    return

########################################################################################################

# str ----> Action
def create_folder_if_not_exists(folder_path, tell_me = False):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        if tell_me: print(f'Se ha creado la carpeta: {folder_path}')
    else:
        if tell_me: print(f'La carpeta ya existe: {folder_path}')
    
    return



def create_folder_for_file(file_path, tell_me = False):
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        if tell_me: 
            print(f"Carpeta '{folder_path}' creada exitosamente.")
    return


# str ----> Action
def recreate_folder_if_exists(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print(f'Se ha eliminado el contenido de la carpeta existente y se ha creado nuevamente: {folder_path}')
    else:
        print(f'La carpeta no existe: {folder_path}')

    return


# str ----> Action
def clear_folder_if_exists(folder_path):

    try:
        # Verificar si la carpeta existe
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Iterar sobre los elementos en la carpeta
            for elemento in os.listdir(folder_path):
                elemento_ruta = os.path.join(folder_path, elemento)

                # Verificar si es un archivo o una carpeta
                if os.path.isfile(elemento_ruta):
                    # Si es un archivo, eliminarlo
                    os.remove(elemento_ruta)
                elif os.path.isdir(elemento_ruta):
                    # Si es una carpeta, eliminarla de manera recursiva
                    for root, dirs, files in os.walk(elemento_ruta, topdown=False):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for dir in dirs:
                            os.rmdir(os.path.join(root, dir))

            print(f"Content from '{folder_path}' had been deteled correcly.")
        else:
            print(f"Folder '{folder_path}' doesn't exist or in not a folder.")
    except Exception as e:
        print(f"Error trying to delet subfolders and files in: {str(e)}")



    return



def clear_folder_recursive(folder):
    """Delete all files in a folder recursively."""
    for content in os.listdir(folder):
        content_path = os.path.join(folder, content)
        if os.path.isfile(content_path):
            # Delete the file if it's a file
            os.remove(content_path)
        elif os.path.isdir(content_path):
            # Recursively delete files in subfolders
            clear_folder_recursive(content_path)
            
            

def list_paths_in_folder(selected_folder_path):
    files = []
    for root, dirs, filenames in os.walk(selected_folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    
    files = natsort.natsorted(files)
    return files


# str ---> list
def list_files_in_folder(selected_folder_path):
    files = []
    for root, dirs, filenames in os.walk(selected_folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    
    files = natsort.natsorted(files)
    files = [os.path.basename(x)  for x in files]
    return files


# Function to list all folders and subfolders
def list_folders(path):
    folders = []
    for current_path, subfolders, files in os.walk(path):
        folders.extend([os.path.join(current_path, folder) for folder in subfolders])
    return folders


def get_last_modified_file(folder_path):
    files = os.listdir(folder_path)
    if not files:
        return None  # Carpeta vacía

    # Ordenar los archivos por fecha de modificación en orden descendente
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    
    last_modified_file = sorted_files[0]
    return last_modified_file





# # # Actions for string------------------------------------------------------------

def clip_last_segment(selected_string, sep = "/"):
    last_segment = selected_string.split(sep)[-1]
    return last_segment



def clip_first_segment(selected_string, sep = "/"):
    first_segment = selected_string.split(sep)[0]
    return first_segment



def clip_specific_segment(selected_string, sep = "/", position = 0):
    selected_segment = selected_string.split(sep)[position]
    return selected_segment



    numbers = [str(i).zfill(2) for i in range(24)]
    return numbers


# str ----> str
def clip_filename(selected_path):
    file_name = os.path.basename(selected_path)
    # file_names = natsorted(file_names) # Bien ordenados
    return file_name



# list[str] -----> list[str]
def filter_lstr_by_extension(file_names_list, extension = ""):
    filtered_files = [file_name for file_name in file_names_list if file_name.endswith(extension)]
    return filtered_files



# list[str] -----> list[str]
def filter_lstr_by_prefix(file_names, prefix):
    filtered_files = [file_name for file_name in file_names if file_name.startswith(prefix)]
    return filtered_files


def detection_prefix_sufix_in_list(prefix, sufix, str_list):
    for selected_string in str_list:
        if prefix in selected_string and selected_string.endswith(sufix):
            return True  # Se encontró al menos un string con el prefijo y sufijo
    return False  # No se encontró ningún string con el prefijo y sufijo en la lista


##################################################################################




def calculate_file_size_in_bytes(ruta_archivo):
    try:
        # Verificar si el archivo existe
        if os.path.isfile(ruta_archivo):
            # Obtener el tamaño del archivo en bytes
            peso_bytes = os.path.getsize(ruta_archivo)
            return peso_bytes
        else:
            print(f"El archivo '{ruta_archivo}' no existe.")
            return None
    except Exception as e:
        print(f"Error al medir el peso del archivo: {str(e)}")
        return None
    
    
    
def calculate_file_size_in_megabytes(file_path):
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Get the file size in bytes
            file_size_bytes = os.path.getsize(file_path)
            
            # Convert the size to megabytes
            file_size_megabytes = file_size_bytes / (1024 * 1024)
            
            return file_size_megabytes
        else:
            print(f"The file '{file_path}' does not exist.")
            return None
    except Exception as e:
        print(f"Error calculating file size: {str(e)}")
        return None
    

def calculate_file_size_in_kilobytes(file_path):
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Get the file size in bytes
            file_size_bytes = os.path.getsize(file_path)
            
            # Convert the size to kilobytes
            file_size_kilobytes = file_size_bytes / 1024
            
            return file_size_kilobytes
        else:
            print(f"The file '{file_path}' does not exist.")
            return None
    except Exception as e:
        print(f"Error calculating file size: {str(e)}")
        return None
    
    
def check_file_size(file_path, size_limit_kb):
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Get the size of the file in bytes
            file_size_bytes = os.path.getsize(file_path)
            
            # Convert the size to kilobytes (KB)
            file_size_kb = file_size_bytes / 1024
            
            # Compare the file size with the limit
            if file_size_kb >= size_limit_kb:
                return True  # The file size is equal or greater than the limit
            else:
                return False  # The file size is less than the limit
        else:
            return False  # The file does not exist
    except Exception as e:
        return False  # An error occurred
    
    
# # # Check Internet Conection
def check_internet_connection():
    test_url = "https://www.google.com"  # You can use any reliable website
    timeout_seconds = 5  # Set a timeout for the request

    try:
        # Try to make an HTTP GET request to the test website
        response = requests.get(test_url, timeout=timeout_seconds)

        # Check if the response has a successful status code (200)
        if response.status_code == 200:
            print("Internet connection established.")
            return True
        else:
            print("Request to the website was not successful. Status code:", response.status_code)
            return False

    except requests.ConnectionError:
        print("Could not establish an Internet connection.")
        return False

    