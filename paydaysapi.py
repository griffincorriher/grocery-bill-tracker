from datetime import datetime, timedelta
import yaml
import holidays
import pandas as pd

def get_adjusted_payday(date, holiday_list):
    # Move earlier if weekend or holiday
    while date.weekday() >= 5 or date in holiday_list:
        date -= timedelta(days=1)
    return date

def get_semi_monthly_paydays(year):
    print(year)
    us_holidays = holidays.UnitedStates(years=year)
    paydays = []

    for month in range(1, 13):
        # 15th
        fifteenth = datetime(year, month, 15)
        fifteenth = get_adjusted_payday(fifteenth, us_holidays)
        paydays.append(fifteenth)

        # End of month
        last_day = pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(1)
        last_day = get_adjusted_payday(last_day.to_pydatetime(), us_holidays)
        paydays.append(last_day)

    paydays = sorted(set(paydays))
    return [d.strftime("%Y-%m-%d") for d in paydays]

def save_to_yaml(paydates, filename="paydates.yaml"):
    with open(filename, "w") as f:
        yaml.dump({"paydays": paydates}, f)