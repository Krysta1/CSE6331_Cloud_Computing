import time


def calculate_timezone(lon):
    currentLon = float(lon)
    consult = currentLon / 15
    remainder = currentLon % 15
    if remainder <= 7.5:
        timeZone = consult
    else:
        if currentLon > 0:
            timeZone = consult + 1
        else:
            timeZone = consult - 1
    return int(timeZone)


def transfer_time(utc_time, timezone):
    new_time = utc_time[:-5].replace("T", ' ')
    # print(new_time)
    timeArray = time.strptime(new_time, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    
    # print(timestamp)
    local_timestamp = time.localtime(timestamp + timezone * 3600)
    dt = time.strftime("%H:%M", local_timestamp)
    return dt


print(transfer_time("2019-06-08T05:55:36.205Z", 8))
