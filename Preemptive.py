import matplotlib.pyplot as plt

def preemptive_scheduler(jobs, max_time):
    schedule = []
    current_time = 0
    while current_time < max_time:
        # Find the highest priority job among available jobs
        highest_priority_job = None
        for job in jobs:
            if job.release_time <= current_time and job.remaining_time > 0:
                if highest_priority_job is None or job.id < highest_priority_job.id:
                    highest_priority_job = job
        if highest_priority_job is not None:
            schedule.append((current_time, highest_priority_job.id))
            highest_priority_job.remaining_time -= 1
            # Check if the job exceeds its deadline
            if current_time > job.deadline:
                print(f"The job which has the release time = {job.release_time} breaks its deadline in {job.deadline}")
                return schedule  # Return schedule even if a deadline is missed    
            current_time += 1
        else:
            # If no job is available, advance time
            schedule.append((current_time, None))
            current_time += 1
    
    return schedule


def draw_timing_diagram2(schedule, max_time):
    plt.figure(figsize=(10, 5))
    
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Colors for each task
    
    for i in range(len(schedule)):
        if schedule[i][1] is not None:
            task_color = colors[schedule[i][1] % len(colors)]  # Assign color based on task priority
            plt.plot([i, i+1], [schedule[i][1], schedule[i][1]], color=task_color, linewidth=3)
    
    plt.xlim(0, max_time)
    plt.ylim(0, 10)  # Adjust ylim based on the maximum priority
    plt.xlabel('Time')
    plt.ylabel('Priority')
    plt.title('Preemptive Task Scheduling Timing Diagram')
    plt.grid(True)
    plt.show()

