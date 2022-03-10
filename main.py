from constants import DATA_PATH, SOURCE_FORMAT
from helpers.power_curve import power_curve
from helpers.winddir_relative_arg_for_all_tribune import winddir_relative_arg_for_all_tribune
from helpers.winddir_abs_comparison import winddir_abs_comparison
from helpers.winddir_relative_arg import winddir_relative_arg
from helpers.winddir_relative_arg_hours import winddir_relative_arg_hours
from datetime import datetime

if __name__ == '__main__':
    begin_date = datetime(2020, 1, 1, 00, 00)
    end_date = datetime(2020, 1, 31, 00, 00)
    # winddir_abs_comparison(begin_date, end_date)
    # df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp', usecols=['PCTimeStamp',
    # 'Amb_WindDir_Relative_Avg'])
    # print(df)
    # df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, usecols= ['PCTimeStamp', 'Amb_WindDir_Relative_Avg'])
    # print(df)
    # power_curve(begin_date, end_date)
    # winddir_relative_arg_for_all_tribune(begin_date, end_date)
    winddir_relative_arg_hours(begin_date, end_date)
