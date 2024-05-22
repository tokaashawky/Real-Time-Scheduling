from collections import deque
import matplotlib.pyplot as plt

def round_robin(tasks, max_time, time_quantum):
    time_quantum = float(time_quantum)
    slots = 1 / time_quantum
    for task in tasks:
        task.generate_jobs()  # Generate additional jobs for each task
    all_jobs = [job for task in tasks for job in task.jobs]
    ready_queue = deque(all_jobs)
    current_time = 0
    schedule = []
    while ready_queue:
        available_jobs = [job for job in ready_queue if job.release_time <= current_time]
        if available_jobs:
            to_remove = []
            for job in available_jobs:
                executed_time = min(slots, job.execution_time)
                job.execution_time -= executed_time

                if job.start_time is None:
                    job.start_time = max(job.release_time, current_time)
                    # Check if the job exceeds its deadline
                    if current_time > job.deadline:
                        print(f"The job which has the release time = {job.release_time} breaks its deadline in {job.deadline}")
                schedule.append((job.id, current_time, current_time + slots))
                if job.execution_time <= 0:
                    job.end_time = current_time + executed_time
                    print(f"job {job.id} completed at time {current_time + executed_time}")
                    ready_queue.remove(job)
                else:
                    # Put the recently used process at the end of the available processes queue
                    ready_queue.remove(job)
                    ready_queue.append(job)
                current_time += slots
            for job in to_remove:
                ready_queue.remove(job)
            print(f"Scheduled jobs: {[job.id for job in available_jobs]} at time {current_time}")
        else:
            current_time += slots
    return schedule

def draw_timing_diagram5(schedule, max_time):
    plt.figure(figsize=(10, 5))

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Colors for each task

    # Dictionary to store the y-coordinate for each priority
    priority_y_coordinate = {}

    for i in range(len(schedule)):
        id, start, end = schedule[i]
        if id is not None:
            if id not in priority_y_coordinate:
                # Assign a fixed y-coordinate for the given priority if not assigned yet
                priority_y_coordinate[id] = len(priority_y_coordinate)  # Incremental y-coordinate for each priority
            y_coordinate = priority_y_coordinate[id]
            task_color = colors[id % len(colors)]  # Assign color based on task priority
            plt.plot([start, end], [y_coordinate, y_coordinate], color=task_color, linewidth=3)

    plt.xlim(0, max_time)
    plt.ylim(-1, len(priority_y_coordinate))  # Adjust ylim based on the number of unique priorities
    plt.xlabel('Time')
    plt.ylabel('Task ID')
    plt.title('Round Robin Timing Diagram')
    plt.yticks(range(len(priority_y_coordinate)), sorted(priority_y_coordinate.keys()))  # Assign y-axis ticks based on priority
    plt.grid(True)
    plt.show()
