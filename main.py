from helpers.basic_figures import *
from datetime import datetime
from helpers.first_sanity_checks import *

if __name__ == '__main__':
    begin_date = datetime(2020, 12, 1, 00, 00)
    end_date = datetime(2020, 12, 8, 23, 50)
    hcnt = 100

    # 1 week data
    # winddir_abs_comparison(begin_date, end_date)
    # power_curve(begin_date, end_date, 300)
    # winddir_relative_avg_for_all_turbine(begin_date, end_date, 300)
    # winddir_relative_avg_hours(begin_date, end_date)
    # winddir_relative_avg(begin_date,end_date, 300)
    # winddir_abs_vs_windspeed(begin_date, end_date)
    # hcnt_avg_run(begin_date, end_date, hcnt)
    # turbine_yaw_avg_comprasion(begin_date, end_date)
    # all_turbines_yaw_misaligment(begin_date, end_date)
    # speed_to_relative_avg(begin_date, end_date, hcnt)
    # turbine_yaw_avg_comprasion(begin_date, end_date)
    # all_turbines_yaw_misaligment(begin_date, end_date)
    #yaw_misaligment_min_max(begin_date, end_date)
    #power_curve_sanity_check(begin_date,end_date, hcnt)
    rpm_yaw_misalignment(begin_date,end_date)
    