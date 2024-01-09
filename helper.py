from datetime import datetime, timedelta
from pytz import timezone

def get_today_timestamp():
    current_datetime = datetime.now(timezone('Asia/Dhaka'))
    midnight_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    midnight_timestamp = midnight_datetime.timestamp() 
    return int(midnight_timestamp)

def get_start_of_week_timestamp():
    today = datetime.now(timezone('Asia/Dhaka'))
    days_since_monday = (today.weekday() - 0) % 7  # 0 is Monday
    start_of_week = today - timedelta(days=days_since_monday)
    start_of_week_midnight = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week_timestamp = start_of_week_midnight.timestamp()
    return int(start_of_week_timestamp)

def get_start_of_month_timestamp():
    today = datetime.now(timezone('Asia/Dhaka'))
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_month_timestamp = start_of_month.timestamp()
    return int(start_of_month_timestamp)