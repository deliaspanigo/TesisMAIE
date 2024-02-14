# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # functions02_time.py
# Functions in relation to:
# - Gregorian dates
# - Julian dates
# - Interconversion between Gregorian and Julian dates
# - Determination of the name of the month


# # # Own functions
# from functions01_generic import *
import fn01_generic as fn01

# # # Libreries
import calendar
import datetime
import re

# from datetime import datetime, timedelta, timezone

# # Gregorian Date ----------------------------------------------------------------------

def str_fulltime_from_filename(selected_file_name, str01 = "G16_s", str02 = "_"):
    # Definir el patrón de la expresión regular
    
    patron_regex = r'G16_s(\d+)'

    # Aplicar la expresión regular para extraer la parte deseada
    coincidencias = re.search(patron_regex, selected_file_name)
    selected_time = coincidencias.group(1)


    date_obj = datetime.datetime.strptime(selected_time, "%Y%m%d%H%M%S")
    date_formated = date_obj.strftime("%Y/%m/%d %H:%M")
    date_final = str(date_formated) + " UTC"

    return date_final


def generate_gregorian_date_list(start_date, end_date):
    """
    Generates a list of dates from start_date to end_date, inclusive.

    Parameters:
    - start_date (str): Start date in 'YYYYMMDD' format.
    - end_date (str): End date in 'YYYYMMDD' format.

    Returns:
    - List of dates as strings in 'YYYYMMDD' format.
    """
    
    start_date = str(start_date)
    end_date = str(end_date)
    
    # Convert input strings to datetime objects
    start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')

    # Calculate the difference between dates
    delta = end_date_obj - start_date_obj

    # Generate the list of dates as strings
    date_list = [(start_date_obj + datetime.timedelta(days=i)).strftime('%Y%m%d') for i in range(delta.days + 1)]

    return date_list



def get_current_date_gregorianCOMP():
    # Obtener la fecha actual
    current_date = datetime.date.today()

    # Formatear la fecha como "year-month-day"
    formatted_date = current_date.strftime("%Y%m%d")

    return formatted_date

def get_current_date_gregorianSEP():
    # Obtener la fecha actual
    current_date = datetime.date.today()

    # Formatear la fecha como "year-month-day"
    formatted_date = current_date.strftime("%Y-%m-%d")

    return formatted_date



def get_previous_date_gregorianSEP():
    
    # Restar un día a la fecha actual
    current_date = datetime.date.today()
    previous_date = current_date - datetime.timedelta(days=1)

    # Formatear la fecha como "year-month-day"
    formatted_date = previous_date.strftime("%Y-%m-%d")

    return formatted_date


def gregorianCOMP_to_julianCOMP(gregorian_date_str):
    
    # Convertir la cadena de fecha a enteros
    gregorian_year = int(str(gregorian_date_str)[0:4])
    gregorian_month = int(str(gregorian_date_str)[4:6])
    gregorian_day = int(str(gregorian_date_str)[6:8])
    
    gregorian_date = datetime.date(int(gregorian_year), int(gregorian_month), int(gregorian_day))

    ordinal = gregorian_date.toordinal()
    julian_day = ordinal - datetime.date(gregorian_date.year, 1, 1).toordinal() + 1
    julian_day = str(julian_day).zfill(3)

    julian_year = str(gregorian_year)
    
    julian_date = julian_year + julian_day 
    return julian_date



def gregorianCOMP_to_fulldate(gregorian_date_str):
    julian_date = gregorianCOMP_to_julianCOMP(gregorian_date_str)
    
    new_name = str("GD") + str(gregorian_date_str) + str("_") + str("JD") + str(julian_date)
    return new_name


def gregorianCOMP_to_newsubfolder(gregorian_date_str):
    gregorian_year = str(gregorian_date_str)[0:4]
    full_date = gregorianCOMP_to_fulldate(gregorian_date_str)
    new_folder = gregorian_year + "/" + full_date + "/" 
    return new_folder



def gregorianPART_to_julianPART(gregorian_year, gregorian_month, gregorian_day):
    
    gregorian_date = datetime.date(int(gregorian_year), int(gregorian_month), int(gregorian_day))

    ordinal = gregorian_date.toordinal()
    julian_day = ordinal - datetime.date(gregorian_date.year, 1, 1).toordinal() + 1
    julian_day = str(julian_day).zfill(3)

    julian_year = str(gregorian_year)
    
    return julian_year, julian_day



def gregorianSEP_to_julianSEP(gregorian_date, date_separator='-'):
    gregorian_year, gregorian_month, gregorian_day  = map(int, gregorian_date.split(date_separator))
    
    julian_year, julian_day = gregorianPART_to_julianPART(gregorian_year, gregorian_month, gregorian_day)
    julian_date = str(julian_year) + date_separator + str(julian_day)
    return julian_date    



# # Julian Date ------------------------------------------------------------------------
    
def julianPART_to_gregorianPART(julian_year, julian_day):
    if isinstance(julian_year, str):
        julian_year = int(julian_year)
    if isinstance(julian_day, str):
        julian_day = int(julian_day)

    base_date = datetime.date(julian_year, 1, 1)
    target_date = base_date + datetime.timedelta(days=julian_day - 1)
    
    gregorian_year = target_date.year
    gregorian_month = target_date.month
    gregorian_day = target_date.day
    
    gregorian_year = str(gregorian_year).zfill(4)
    gregorian_month = str(gregorian_month).zfill(2)
    gregorian_day = str(gregorian_day).zfill(2)
    
    return gregorian_year, gregorian_month, gregorian_day 



def julianSTR_to_gregorianSTR(julian_date, date_separator="-"):
    julian_year, julian_day= julian_date.split(date_separator)

    gregorian_year, gregorian_month, gregorian_day = julianPART_to_gregorianPART(julian_year, julian_day)
    
    gregorian_date = gregorian_year + date_separator + gregorian_month + date_separator + gregorian_day
    return gregorian_date




def gregorianCOMP_to_gregorianSEP(gregorian_comp, date_separator = "-"):
    gregorian_year = gregorian_comp[0:4]
    gregorian_month = gregorian_comp[4:6]
    gregorian_day = gregorian_comp[6:8]
    
    gregorian_date = gregorian_year + date_separator + gregorian_month + date_separator + gregorian_day
    return gregorian_date



###########


def get_month_name(month_number):
    if isinstance(month_number, str):
        month_number = int(month_number)
    
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return "Invalid month number"    
    
    
def gregorianSEP_to_full_month_name(gregorian_date):
    gregorian_month = fn01.clip_specific_segment(gregorian_date, sep = "-", position = 1)
    month_name = get_month_name(gregorian_month)
    output = gregorian_month + "_" + month_name
    return output


def gregorianSEP_to_fulldate(gregorian_date):            
    # gregorian_date = get_current_date_gregorian()
    # gregorian_year = clip_specific_segment(gregorian_date, sep = "-", position = 0)
    gregorian_month = fn01.clip_specific_segment(gregorian_date, sep = "-", position = 1)
    gregorian_day = fn01.clip_specific_segment(gregorian_date, sep = "-", position = 2)
    armado_gregoriano = "GD" + gregorian_date
    
    julian_date    = gregorianSEP_to_julianSEP(gregorian_date = gregorian_date, date_separator='-')
    julian_year =  fn01.clip_first_segment(selected_string  =  julian_date, sep = "-")
    julian_day =   fn01.clip_last_segment(selected_string   =  julian_date, sep = "-")
    armado_juliano = "JD" + julian_date
    
    month_name = get_month_name(gregorian_month)
    special_month = gregorian_month + "_" + month_name 
    
    
    armado_junto = armado_gregoriano + "_" + armado_juliano
    return armado_junto 


def gregorianSEP_to_newfolder(gregorian_date):
    gregorian_year = fn01.clip_specific_segment(gregorian_date, sep = "-", position = 0)
    month_full_name = gregorianSEP_to_full_month_name(gregorian_date)    
    full_date = gregorianSEP_to_fulldate(gregorian_date)
    new_folder = gregorian_year + "/" +  month_full_name + "/" + full_date + "/"
    return new_folder



def gregoriandate_utc2local_string(fecha_string, correccion=0):
    # Convertir el string a un objeto datetime
    fecha_utc = datetime.datetime.strptime(fecha_string, '%Y/%m/%d %H:%M %Z')

    # Crear un objeto timezone con la corrección
    correccion_utc = datetime.timezone(datetime.timedelta(hours=correccion))
    fecha_local = fecha_utc.replace(tzinfo=correccion_utc).astimezone(datetime.timezone.utc)

    # Cambiar "UTC" por "Local" en el string
    fecha_local_str = fecha_local.strftime('%Y/%m/%d %H:%M ARG')

    return fecha_local_str
