import sys

# Import own libreries
fn_folder = '01.own_resources/01.python_code/01.functions/'
sys.path.append(fn_folder)
import fn01_generic as fn01



def sp_gen02_OnePlot_OneDay_Hardcoded(gregorian_date, fnBxxx_03_plotxxx):

    print('Start: sp_gen02_OnePlot_OneDay_Hardcoded()')
    print("Selected gregorian day: {}".format(gregorian_date))
    

    info_standard_plot = fnBxxx_03_plotxxx.standard_plot_Hardcoded(gregorian_date)
    info_input =  fnBxxx_03_plotxxx.standard_input_OneDay_Hardcoded(gregorian_date)
    info_output =  fnBxxx_03_plotxxx.standard_output_OneDay_Hardcoded(gregorian_date)

    
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
        return
    
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
            fnBxxx_03_plotxxx.sp_gen01(selected_input_path, selected_output_path, 
                     plot_me = info_standard_plot["plot_me"], 
                     save_me = info_standard_plot["save_me"],
                     overwrite = info_standard_plot["overwrite"])
        
        print("\n")
        
    print("Close: sp_gen02_OnePlot_OneDay_Hardcoded()")
    
    return



def sp_gen02_AllPlot_OneDay_Hardcoded(gregorian_date):
    return