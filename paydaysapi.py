from datetime import datetime, timedelta
import yaml
import holidays
import pandas as pd

def get_adjusted_payday(date, holiday_list):
    while date.weekday() >= 5 or date in holiday_list:
        date -= timedelta(days=1)
    return date

def get_semi_monthly_paydays(year):
    us_holidays = holidays.UnitedStates(years=[year-1, year])
    paydays = []

    # Include December of previous year
    for month in range(12, 13+12):  # from December (12) to next November (13+11 = 24)
        y = year - 1 if month == 12 else year
        m = 12 if month == 12 else (month % 12 or 12)

        # 15th
        fifteenth = datetime(y, m, 15)
        adj_fifteenth = get_adjusted_payday(fifteenth, us_holidays)
        if adj_fifteenth.year == year - 1 and m == 12:
            paydays.append(adj_fifteenth)
        elif y == year:
            paydays.append(adj_fifteenth)

        # End of month
        last_day = pd.Timestamp(year=y, month=m, day=1) + pd.offsets.MonthEnd(1)
        adj_last_day = get_adjusted_payday(last_day.to_pydatetime(), us_holidays)
        if adj_last_day.year == year - 1 and m == 12:
            paydays.append(adj_last_day)
        elif y == year:
            paydays.append(adj_last_day)

    # Remove duplicates and sort
    paydays = sorted(set(paydays))
    return [d.strftime("%Y-%m-%d") for d in paydays]

def save_to_yaml(paydates, filename="paydates.yaml"):
    with open(filename, "w") as f:
        yaml.dump({"paydays": paydates}, f)