# # # Own functions
import fn01_generic as fn01
import fn02_time as fn02
import fn03_goes_download_gen as fn03



# List of products to will be downloaded
# - ABI-L2-ACMF
# - ABI-L2-FDCC
# - ABI-L2-FDCF
# - ABI-L2-LSTF
# - GLM-L2-LCFA




def ST04_download_goes_ALL_OneDay(root_folder, gregorian_date_SEP):
    
    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP)

    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP)
        
    return


def ST04_download_goes_ALL_YESTERDAY(root_folder):
    
    print(" *** INICIO DESCARGA YESTERDAY!!!  *** ")
    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()
    
    print("\n")
    print("\n")
    print(" *** INICIO ACMF!!!  *** ")
    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP)

    print("\n")
    print("\n")
    print(" *** INICIO FDCC!!!  *** ")
    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP)

    print("\n")
    print("\n")
    print(" *** INICIO FDCF!!!  *** ")
    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP)
    
    print("\n")
    print("\n")
    print(" *** INICIO LSTF!!!  *** ")
    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP)
    
    print("\n")
    print("\n")
    print(" *** INICIO LCFA!!!  *** ")
    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP)
        
    print(" *** FIN DESCARGA YESTERDAY!!!  *** ")    
    
    return


def ST04_download_goes_ALL_TODAY(root_folder):
    
    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()
    
    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP)

    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP)
    
    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP)
        
    return


def ST04_download_goes_ALL_YandT(root_folder):
    
    # Folder and GregoriaDate
    #root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP_yesterday =  fn02.get_previous_date_gregorianSEP()
    gregorian_date_SEP_today =  fn02.get_current_date_gregorianSEP()
    
    # Yesterday
    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_yesterday)

    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_yesterday)

    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_yesterday)
    
    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_yesterday)
    
    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_yesterday)
        


    # Today
    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_today)

    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_today)

    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_today)
    
    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_today)
    
    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP = gregorian_date_SEP_today)
        
        
    return

#######################################################################################################



def ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP):

    # Harcodeo 
    bucket_name = 'noaa-goes16'
    product_name = 'ABI-L2-ACMF'
    general_prefix = "OR_ABI-L2-ACMF-M6_G16_s"
    general_sufix = ".nc"

    fn03.download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix)

    return


def ST04_download_goes_ACMF_yesterday(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()


    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP)

    return


def ST04_download_goes_ACMF_today(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()


    ST04_download_goes_ACMF_OneDay(root_folder, gregorian_date_SEP)
   
    return

#######################################################################################################



def ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP):

    # Harcodeo 
    bucket_name = 'noaa-goes16'
    product_name = 'ABI-L2-FDCC'
    general_prefix = "OR_ABI-L2-FDCC-M6_G16_s"
    general_sufix = ".nc"

    # Download
    fn03.download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix)

    return


def ST04_download_goes_FDCC_yesterday(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()


    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP)

    return


def ST04_download_goes_FDCC_today(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()

    ST04_download_goes_FDCC_OneDay(root_folder, gregorian_date_SEP)

    return

#######################################################################################################


def ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP):

    # Harcodeo 
    bucket_name = 'noaa-goes16'
    product_name = 'ABI-L2-FDCF'
    general_prefix = "OR_ABI-L2-FDCF-M6_G16_s"
    general_sufix = ".nc"

    # Download
    fn03.download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix)

    return




def ST04_download_goes_FDCF_yesterday(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()


    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP)

    return


def ST04_download_goes_FDCF_today(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()


    ST04_download_goes_FDCF_OneDay(root_folder, gregorian_date_SEP)

    return

#######################################################################################################

def ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP):

    # Harcodeo 
    bucket_name = 'noaa-goes16'
    product_name = 'ABI-L2-LSTF'
    general_prefix = "OR_ABI-L2-LSTF-M6_G16_s"
    general_sufix = ".nc"

    # Download
    fn03.download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix)

    return


def ST04_download_goes_LSTF_yesterday(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()


    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP)

    return


def ST04_download_goes_LSTF_today(root_folder):

 # Folder and GregoriaDate
    #root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()


    ST04_download_goes_LSTF_OneDay(root_folder, gregorian_date_SEP)

    return



#######################################################################################################


def ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP):

    # Harcodeo 
    bucket_name = 'noaa-goes16'
    product_name = 'GLM-L2-LCFA'
    general_prefix = "OR_GLM-L2-LCFA_G16_s"
    general_sufix = ".nc"

    # Download
    fn03.download_goes_gen03(root_folder, bucket_name, product_name, gregorian_date_SEP, general_sufix)

    return


def ST04_download_goes_LCFA_yesterday(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_previous_date_gregorianSEP()


    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP)
    return


def ST04_download_goes_LCFA_today(root_folder):

    # Folder and GregoriaDate
    # root_folder = '../../02.input/01.raster/'
    gregorian_date_SEP =  fn02.get_current_date_gregorianSEP()


    ST04_download_goes_LCFA_OneDay(root_folder, gregorian_date_SEP)

    return


#######################################################################################################

                            
                            