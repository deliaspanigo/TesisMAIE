# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # functions03_goes_download.py
# Funciones en relacion a:
# - gen00: simple download without function
# - gen01: gen00 inside as a function
# - gen02: gen01 + subfolder creation


# Import own libreries
import sys

fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01


import os
import imageio
import re 


def convert_list_paths_png2mp4_gen01(image_paths, output_path, fps=10):
    
    fn01.create_folder_for_file(output_path)
    
    images = []

    for filepath in image_paths:
        images.append(imageio.imread(filepath))

    # Escribir el video
    imageio.mimsave(output_path, images, fps=fps)
    
    return

    
def convert_png2gif(image_paths, output_path, fps=10):
    images = []

    for filepath in image_paths:
        images.append(imageio.imread(filepath))

    fn01.create_folder_for_file(output_path)

    # Escribir el GIF
    imageio.mimsave(output_path, images, duration=1/fps)
    
    return

###########################################################################



def convert_png2mp4_spiALL_gen02_OneDay_Simple(gregorian_date, subfolder_product = "", fps = 10, overwrite = False):
    
    print("Init: convert_png2mp4_spiALL_gen02_OneDay_Simple()")
    general_input_folder = "04.png/"
    
    input_folders = fn01.list_folders(general_input_folder)
    input_folders = [element for element in input_folders if gregorian_date in element]
    input_folders = [element for element in input_folders if subfolder_product in element]
    input_folders.sort()
    input_folders = [x + "/" for x in input_folders]
    
    output_folders = [re.sub(f'{general_input_folder}', f'{"05.mp4_OneDay/"}', x) for x in input_folders] 

    total_input_folders = len(input_folders)
    
    for x in range(total_input_folders):
        selected_input_folder = input_folders[x]
        selected_output_folder = output_folders[x]
        
        print(f'File {x+1} of {total_input_folders}')
        print(f'  selected_input_folder:  {selected_input_folder}')
        print(f'  selected_output_folder: {selected_output_folder}')

        
        input_paths = fn01.list_paths_in_folder(selected_input_folder)
        input_paths.sort()
        
        
        input_files_png = fn01.list_files_in_folder(selected_input_folder)
        input_file_png = input_files_png[0]
        
        new_structure = "_png2mp4_" + "fps" + str(fps) + "_"
        output_file_mp4 = re.sub(f'{"_nc2png_"}', f'{new_structure}', input_file_png)
        output_file_mp4 = re.sub(f'{".png"}$', f'{".mp4"}', output_file_mp4)
        
        output_path = selected_output_folder + output_file_mp4
        
        print(f'  output_path: {output_path}')
                
        dt_not_exists_mp4 = not os.path.exists(output_path)
        
        if dt_not_exists_mp4 or overwrite:
            
            fn01.create_folder_for_file(output_path)
            print(f'  Converting...')
            convert_list_paths_png2mp4_gen01(image_paths = input_paths, 
                                             output_path = output_path,
                                             fps=fps)
            
            print(f'  Done!')
        else:
            print("  File exists!")   
            
    print("Close: convert_png2mp4_spiALL_gen02_OneDay_Simple()")
            
    return


