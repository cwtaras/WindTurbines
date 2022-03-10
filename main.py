from helpers.power_curve import power_curve
from helpers.winddir_relative_avg_for_all_turbine import winddir_relative_avg_for_all_turbine
from helpers.winddir_abs_comparison import winddir_abs_comparison
from helpers.winddir_relative_avg import winddir_relative_avg
from helpers.winddir_relative_avg_hours import winddir_relative_avg_hours
from helpers.hcnt_avg_run import hcnt_avg_run
from helpers.winddir_abs_vs_windspeed import winddir_abs_vs_windspeed
from datetime import datetime

if __name__ == '__main__':
    begin_date = datetime(2021, 1, 1, 00, 00)
    end_date = datetime(2021, 1, 8, 00, 00)
    hcnt = 100

    # 1 week data
    winddir_abs_comparison(begin_date, end_date)
    power_curve(begin_date, end_date, 300)
    winddir_relative_avg_for_all_turbine(begin_date, end_date, 300)
    winddir_relative_avg_hours(begin_date, end_date)
    winddir_relative_avg(begin_date,end_date, 300)
    winddir_abs_vs_windspeed(begin_date, end_date)
    # hcnt_avg_run(begin_date, end_date, hcnt)
