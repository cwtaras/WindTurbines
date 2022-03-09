from helpers.helper_functions import column_number_finder
from helpers.power_curve import power_curve
from helpers.winddir_relative_arg_for_all_tribune import winddir_relative_arg_for_all_tribune
from helpers.winddir_abs_comparison import winddir_abs_comparison
from helpers.winddir_relative_arg import winddir_relative_arg
from helpers.winddir_relative_arg_hours import winddir_relative_arg_hours
from datetime import datetime

if __name__ == '__main__':
    # Grd_Prod_Pwr_Avg - 47
    # Amb_WindSpeed_Avg - 12
    # Amb_WindDir_Abs_Avg - 34
    column_number_finder(' Amb_WindDir_Abs_Avg')
    begin_date = datetime(2021, 1, 1, 00, 00)
    end_date = datetime(2021, 1, 8, 12, 00)
    power_curve(begin_date, end_date)
