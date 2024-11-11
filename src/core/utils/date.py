from datetime import datetime, date

AGE_FORMAT = '%Y-%m-%d'

def str_to_date(date_string: str) -> date:
    return datetime.strptime(date_string, AGE_FORMAT).date()