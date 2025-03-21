from datetime import datetime
from datetime import timedelta


def get_date_after_n_days(date: datetime, days: int = 30) -> datetime:
    return date + timedelta(days=days)
