from src.data.cfg import days_of_week


def split_day_of_week(accs):
    accs["weight"] = 1
    accs["Day of Week"] = accs["Start_Time"].dt.day_of_week.apply(
        lambda x: days_of_week[x]
    )
    orders = {"Day of Week": days_of_week}
    return accs, orders


def split_workday(accs):
    accs["weight"] = 1
    accs["Workday"] = accs.Start_Time.dt.day_of_week < 4
    orders = {"Workday": ["Work week", "Weekend"]}
    accs.loc[accs["Workday"], "weight"] *= 2 / 5
    return accs, orders


def split_raining(accs):
    accs["weight"] = 1
    accs["Raining"] = accs["Precipitation"] > 0
    orders = {"Precipitation": ["No", "Yes"]}
    return accs, orders


SPLIT_DICT = {
    "Day of Week": split_day_of_week,
    "Workday": split_workday,
    "Raining": split_raining,
}


def split_by(accs, split):
    return SPLIT_DICT[split](accs)
