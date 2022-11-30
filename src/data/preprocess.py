from src.data.cfg import days_of_week


def get_dayofweek(accs):
    accs["Day of Week"] = accs["Start_Time"].dt.day_of_week.apply(
        lambda x: days_of_week[x]
    )
    return accs
