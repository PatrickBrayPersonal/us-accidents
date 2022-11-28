from src.data.cfg import days_of_week


def get_dayofweek(accs):
    accs["Day of Week"] = accs["Start_DOW"].apply(lambda x: days_of_week[x])
    return accs
