from datetime import datetime
from zoneinfo import ZoneInfo


def get_ist_now():

    # Returns current time explicitly in IST, since server/DB defaults are UTC
    
    return datetime.now(ZoneInfo("Asia/Kolkata"))