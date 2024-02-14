
# # # Own functions
import fn01_generic as fn01
import fn02_time as fn02
import fn07_goes16_mp4_generic as fn07


def convert_png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date, fps = 10, overwrite = False):
 
    print("Init: convert_png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded()")
    general_input_folder = "04.png/"
    subfolder_product = "spi076_ABI-L2-MCMIPF/"
    
    fn07.convert_png2mp4_spiALL_gen02_OneDay_Simple(gregorian_date = gregorian_date,
                                                  subfolder_product= subfolder_product, 
                                                  fps = fps, overwrite = overwrite)
            
    print("Close: convert_png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded()")
            
    return





# def convert_nc2png2mp4_goes16_spi076_MCMIPF_gen02_RangeDate_HardCoded(init_gregorian_date, end_gregorian_date, fps = 10, overwrite = False):
    
#     print('Start: convert_nc2png2mp4_goes16_spi076_MCMIPF_gen02_RangeDate_HardCoded()')
    
#     gregorian_list = fn02.generate_gregorian_date_list(start_date = init_gregorian_date, end_date = end_gregorian_date)

#     for x in gregorian_list:
#         convert_nc2png2mp4_goes16_spi076_MCMIPF_gen02_OneDay_HardCoded(gregorian_date = x, fps = fps, overwrite = overwrite)
        
#     print('Close: convert_nc2png2mp4_goes16_spi076_MCMIPF_gen02_RangeDate_HardCoded()')
     
#     return
