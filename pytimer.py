import csv
import time
from datetime import datetime

def start_task(task_name):
    start_time = time.time()
    return task_name, start_time

def end_task(task_name, start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    log_time(task_name, elapsed_time)

def log_time(task_name, elapsed_time):
    date_str = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_spent = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    with open('/Users/zzigak/timer/pytimer_times.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, task_name, time_spent])

def main(task_name):
    print(f"Starting task: {task_name}")
    task_name, start_time = start_task(task_name)
    input("Press Enter to stop the task...")
    end_task(task_name, start_time)
    print(f"Task '{task_name}' logged.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: pytimer.py taskName")
    else:
        main(sys.argv[1])
