import matplotlib.pyplot as plt

def dma_scheduler(jobs, max_time):
    schedule = []
    current_time = 0
    deadline_breaks = ""  # String variable to accumulate the printed text
    # Sort tasks by deadline (earliest first)
    jobs.sort(key=lambda x: x.deadline)
    
    while current_time < max_time:
        # Find the task with the earliest deadline among available tasks
        earliest_deadline_job = None
        for job in jobs:
            if job.release_time <= current_time and job.remaining_time > 0:
                if earliest_deadline_job is None or job.deadline < earliest_deadline_job.deadline:
                    earliest_deadline_job = job
        
        if earliest_deadline_job is not None:
            schedule.append((current_time, earliest_deadline_job.id))
            earliest_deadline_job.remaining_time -= 1
            current_time += 1
            # Check if the job exceeds its deadline
            if current_time > job.deadline:
                deadline_breaks += f"The job which has the release time = {earliest_deadline_job.release_time} breaks its deadline in {earliest_deadline_job.deadline}\n"
                   
            
        else:
            # If no task is available, advance time
            schedule.append((current_time, None))
            current_time += 1
    
    return schedule , deadline_breaks

def draw_timing_diagram6(schedule, max_time):
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
    plt.title('DMA Timing Diagram')
    plt.yticks(range(len(priority_y_coordinate)), sorted(priority_y_coordinate.keys()))  # Assign y-axis ticks based on priority
    plt.grid(True)
    plt.show()

