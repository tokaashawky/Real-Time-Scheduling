import matplotlib.pyplot as plt

def FIFO_scheduler(jobs, max_time):
    
    schedule = []
    current_time = 0
    deadline_breaks = ""  # String variable to accumulate the printed text
    # Sort tasks by release time (earliest first)
    jobs.sort(key=lambda x: x.release_time)
    
    while current_time < max_time:
        # Find the earliest released job among available jobs
        earliest_released_job = None
        for job in jobs:
            if job.release_time <= current_time and job.remaining_time > 0:
                if earliest_released_job is None or job.release_time < earliest_released_job.release_time:
                    earliest_released_job = job
        
        if earliest_released_job is not None:
            # Execute the job until completion
            for _ in range(int (earliest_released_job.execution_time)):
                schedule.append((current_time, earliest_released_job.id))
                current_time += 1
                earliest_released_job.remaining_time -= 1
                
                # Check if the job exceeds its deadline
                if current_time > earliest_released_job.deadline:
                    deadline_breaks += f"The job which has the release time = {earliest_released_job.release_time} breaks its deadline in {earliest_released_job.deadline}\n"
                
        else:
            # If no job is available, advance time
            schedule.append((current_time, None))
            current_time += 1
    
    return schedule , deadline_breaks


def draw_timing_diagram3(schedule, max_time):
    plt.figure(figsize=(10, 5))
    
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Colors for each task
    
    # Dictionary to store the y-coordinate for each priority
    priority_y_coordinate = {}
    
    for i in range(len(schedule)):
        time, id = schedule[i]
        if id is not None:
            if id not in priority_y_coordinate:
                # Assign a fixed y-coordinate for the given priority if not assigned yet
                priority_y_coordinate[id] = len(priority_y_coordinate)  # Incremental y-coordinate for each priority
            y_coordinate = priority_y_coordinate[id]
            task_color = colors[id % len(colors)]  # Assign color based on task priority
            plt.plot([time, time + 1], [y_coordinate, y_coordinate], color=task_color, linewidth=3)
    
    plt.xlim(0, max_time)
    plt.ylim(-1, len(priority_y_coordinate))  # Adjust ylim based on the number of unique priorities
    plt.xlabel('Time')
    plt.ylabel('Task ID')
    plt.title('FIFO Timing Diagram')
    plt.yticks(range(len(priority_y_coordinate)), sorted(priority_y_coordinate.keys()))  # Assign y-axis ticks based on priority
    plt.grid(True)
    plt.show()