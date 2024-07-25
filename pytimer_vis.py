import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def load_data(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            date = datetime.strptime(row[0], "%Y-%m-%d|%H:%M:%S")
            task = row[1]
            time_str = row[2]
            data.append((date, task, time_str))
    return data

def convert_time_to_seconds(time_str):
    time_parts = time_str.split()
    time_seconds = 0
    for part in time_parts:
        if 'h' in part:
            time_seconds += int(part[:-1]) * 3600
        elif 'm' in part:
            time_seconds += int(part[:-1]) * 60
        elif 's' in part:
            time_seconds += int(part[:-1])
    return time_seconds

def preprocess_data(data):
    tasks = list(set(task for _, task, _ in data))
    weeks = list(set(date.strftime('%Y-%U') for date, _, _ in data))

    # Initialize a dictionary to store time spent on each task per week
    time_data = {task: {week: 0 for week in weeks} for task in tasks}

    for date, task, time_str in data:
        week = date.strftime('%Y-%U')
        time_seconds = convert_time_to_seconds(time_str)
        time_data[task][week] += time_seconds

    weeks.sort()
    weekly_data = np.array([[time_data[task][week] / 3600 for task in tasks] for week in weeks])
    
    return tasks, weeks, weekly_data

def plot_time_per_task_per_week(tasks, weeks, weekly_data):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    width = 0.15  # Width of each bar
    x = np.arange(len(weeks))
    
    for i, task in enumerate(tasks):
        ax.bar(x + i * width, weekly_data[:, i], width, label=task)
    
    ax.set_xlabel('Week')
    ax.set_ylabel('Hours')
    ax.set_title('Time Spent on Each Task per Week')
    ax.set_xticks(x + width * (len(tasks) - 1) / 2)
    ax.set_xticklabels(weeks, rotation=45)
    ax.set_ylim(0, 10)  # Set y-axis limit to 10 hours
    ax.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def plot_avg_time_per_task(tasks, weekly_data):
    avg_time_per_task = np.mean(weekly_data, axis=0)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(tasks, avg_time_per_task)
    
    ax.set_xlabel('Task')
    ax.set_ylabel('Average Hours per Week')
    ax.set_title('Average Time Spent on Each Task per Week')
    ax.set_ylim(0, 10)  # Set y-axis limit to 10 hours
    
    plt.tight_layout()
    plt.show()

def main():
    file_path = 'pytimer_times.csv'
    data = load_data(file_path)
    tasks, weeks, weekly_data = preprocess_data(data)
    
    plot_time_per_task_per_week(tasks, weeks, weekly_data)
    plot_avg_time_per_task(tasks, weekly_data)

if __name__ == "__main__":
    main()
