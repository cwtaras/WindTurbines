from .power_curve import power_curve
from .winddir_relative_avg import winddir_relative_avg
from .winddir_relative_avg_for_all_turbine import winddir_relative_avg_for_all_turbine


def hcnt_avg_run(begin_date, end_date, hcnt):
    power_curve(begin_date, end_date, hcnt)
    winddir_relative_avg(begin_date, end_date, hcnt)
    winddir_relative_avg_for_all_turbine(begin_date, end_date, hcnt)
