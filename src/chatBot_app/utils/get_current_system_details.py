from datetime import datetime, timezone

def get_system_time_info()-> dict:
    utc_now =  datetime.now(timezone.utc)
    local_tz = datetime.now().astimezone().tzinfo
    day_of_week = datetime.now().strftime("%A")

    return {
        "current_utc_datetime": utc_now,
        "local_timezone": str(local_tz),
        "day_of_week": day_of_week,
    }