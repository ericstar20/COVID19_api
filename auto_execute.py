
import datetime
import threading
from covid_api import covid_api_sql

# Initial start time
marktime=" 23:00:00"

# Set excute code
def func():
    # put the code you want to auto execute below
    covid_api_sql()
    timer = threading.Timer(86400, func)
    timer.start()

# Define the prefun condition
def preFun():
    now_time = datetime.datetime.now()
    marktimes = datetime.datetime.strptime(str(now_time.date()) + marktime, "%Y-%m-%d %H:%M:%S")
    if (now_time <= marktimes):
        next_time = marktimes
        print("Today" + marktime + ' will excute the code!')
    else:
        # tomorrow execute
        next_time = now_time + datetime.timedelta(days=+1)
        print("Tomorrow" + marktime + 'will excute the code!')
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day

    next_time = datetime.datetime.strptime(str(next_year) +
                                           "-" + str(next_month) +
                                           "-" + str(next_day) + marktime,
                                           "%Y-%m-%d %H:%M:%S")
    timer_start_time = (next_time - now_time).total_seconds()
    return timer_start_time

def main():
    timer_start_time=preFun()
    timer = threading.Timer(timer_start_time, func)
    timer.start()
    print('After close the code, the auto program will re-execute at',timer_start_time)
    pass

if __name__ == '__main__':
    main()
