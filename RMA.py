import matplotlib.pyplot as plt

class Task:
    def __init__(self, release_time, period, execution_time, deadline, id):
        self.jobs = [Job(release_time, period, execution_time, deadline, id)]
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.deadline = deadline
        self.id = id
        
    def generate_jobs(self):
        for i in range(1, 6):  # Generate five additional jobs
            release_time = self.jobs[0].release_time + i * self.jobs[0].period
            period = self.period * (i + 1)
            execution_time = self.jobs[-1].execution_time
            deadline = self.jobs[-1].deadline + period
            id = self.jobs[-1].id
            job = Job(release_time, period, execution_time, deadline, id)
            self.jobs.append(job)
            print(f"Job {i}: Release Time: {release_time}, Period: {period}, Execution Time: {execution_time}, Deadline: {deadline}")


class Job:
    def __init__(self, release_time, period, execution_time, deadline, id):
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.deadline = deadline
        self.id = id    

def rma_scheduler(jobs, max_time):
    schedule = []
    current_time = 0
    deadline_breaks = ""  # String variable to accumulate the printed text
    
    # Sort tasks by deadline (earliest first)
    jobs.sort(key=lambda x: x.period)
    
    while current_time < max_time:
        # Find the task with the earliest deadline among available tasks
        earliest_period_job = None
        for job in jobs:
            if job.release_time <= current_time and job.remaining_time > 0:
                if earliest_period_job is None or job.period < earliest_period_job.period:
                    earliest_period_job = job
        
        if earliest_period_job is not None:
            schedule.append((current_time, earliest_period_job.id))
            earliest_period_job.remaining_time -= 1
            current_time += 1
            
            # Check if the job exceeds its deadline
            if current_time > earliest_period_job.deadline:
                deadline_breaks += f"The job which has the release time = {earliest_period_job.release_time} breaks its deadline in {earliest_period_job.deadline}\n"
                
        else:
            # If no task is available, advance time
            schedule.append((current_time, None))
            current_time += 1
    
    return schedule , deadline_breaks

def draw_timing_diagram7(schedule, max_time):
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
    plt.title('RMA Timing Diagram')
    plt.yticks(range(len(priority_y_coordinate)), sorted(priority_y_coordinate.keys()))  # Assign y-axis ticks based on priority
    plt.grid(True)
    plt.show()





    




