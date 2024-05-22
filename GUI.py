import tkinter as tk
from tkinter import ttk
from collections import deque
import matplotlib.pyplot as plt

from NonPreemptive import non_preemptive_scheduler, draw_timing_diagram1
from Preemptive import preemptive_scheduler, draw_timing_diagram2
from FIFO import FIFO_scheduler, draw_timing_diagram3
from EDF import earliest_deadline_first, draw_timing_diagram4
from RR import round_robin, draw_timing_diagram5
from DMA import dma_scheduler, draw_timing_diagram6
from RMA import rma_scheduler, draw_timing_diagram7
from MLFF import Tasks, jobs, draw_timing_diagram8
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
    def get_available_jobs(self, current_time):
        return [job for job in self.jobs if job.release_time <= current_time]
class Job:
    def __init__(self, release_time, period, execution_time, deadline, id):
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.deadline = deadline
        self.id = id    
        self.start_time = None  # Introduce start_time attribute
      
task_entries = []
def add_task_fields():    
    task_entries.clear()
    num_tasks = int(num_tasks_entry.get())
    for i in range(num_tasks):
        task_frame = ttk.LabelFrame(root, text=f"Task {i+1}")
        task_frame.grid(row=5, column=i, padx=5, pady=5, sticky="nsew")  # Place each task frame in the same row but different columns
        task_params = {}
        if algorithm_choice.get() == 'Preemptive' or algorithm_choice.get() == 'Non_Preemptive':
            labels = ['Release Time', 'Period', 'Execution Time', 'Deadline', 'priority']   
        else:
            labels = ['ID','Release Time', 'Period', 'Execution Time', 'Deadline']  
        
        for j, label_text in enumerate(labels):
            ttk.Label(task_frame, text=label_text).grid(row=j, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(task_frame)
            entry.grid(row=j, column=1, padx=5, pady=5, sticky="ew")
            task_params[label_text.lower().replace(' ', '_')] = entry
        task_entries.append(task_params)  # Store the dictionary of entries
        
        
def clear_results_labels():
    deadline_breaks_label.config(text="")
    
def calculate_schedule():
    clear_results_labels()
    tasks = []
    rtasks = []
    num_tasks = int(num_tasks_entry.get())
    max_time = int(max_time_entry.get())
    selected_algorithm = algorithm_choice.get()
    
    for i in range(num_tasks):
        release_time = int(task_entries[i]['release_time'].get())
        period = int(task_entries[i]['period'].get())
        execution_time = float(task_entries[i]['execution_time'].get())
        deadline = int(task_entries[i]['deadline'].get())
        if selected_algorithm == 'Preemptive' or selected_algorithm == 'Non_Preemptive':
            id = int(task_entries[i]['priority'].get())
        else:
            id = int(task_entries[i]['id'].get()) 
            
        if algorithm_choice.get() != 'MLF':               
            rtasks.append(Task(release_time, period, execution_time, deadline, id))
            initial_job = Job(release_time, period, execution_time, deadline, id)
            tasks.append(initial_job)
            for j in range(1, 6):
                release_time = initial_job.release_time + j * initial_job.period
                period = initial_job.period * (j + 1)
                deadline = initial_job.deadline - initial_job.release_time + release_time
                job = Job(release_time, period, execution_time, deadline, id)
                tasks.append(job)
        else:
            rtasks.append(Tasks( id,release_time, period, execution_time, deadline,max_time))
              
    deadline_breaks = ""
    if selected_algorithm == 'FIFO':
        schedule, deadline_breaks = FIFO_scheduler(tasks, max_time)
        print(schedule)
        draw_timing_diagram3(schedule, max_time)
    elif selected_algorithm == 'EDF':
        schedule, deadline_breaks = earliest_deadline_first(tasks, max_time)
        print(schedule)
        draw_timing_diagram4(schedule, max_time)
    elif selected_algorithm == 'DMA':
        schedule, deadline_breaks = dma_scheduler(tasks, max_time)
        print(schedule)
        draw_timing_diagram6(schedule, max_time)
    elif selected_algorithm == 'RMA':
        schedule, deadline_breaks = rma_scheduler(tasks, max_time)
        print(schedule)
        draw_timing_diagram7(schedule, max_time)
    elif selected_algorithm == 'Preemptive':
        schedule = preemptive_scheduler(tasks, max_time)
        print(schedule)
        draw_timing_diagram2(schedule, max_time)
    elif selected_algorithm == 'Non_Preemptive':
        schedule = non_preemptive_scheduler(tasks, max_time)
        print(schedule)
        draw_timing_diagram1(schedule, max_time)
    elif selected_algorithm == 'RR':
        time_quantum = float(time_quantum_entry.get())
        schedule = round_robin(rtasks, max_time, time_quantum)
        print(schedule)
        draw_timing_diagram5(schedule, max_time) 
    elif selected_algorithm == 'MLF':
       mlf = jobs(rtasks, max_time)
       results = mlf.getResults() 
       print(results[0])
       draw_timing_diagram8(results[0], max_time) 
        
    deadline_breaks_label.config(text="Note: " + str(deadline_breaks))

root = tk.Tk()
root.title("Task Scheduler")

# Algorithm Selection
algorithm_label = ttk.Label(root, text="Select Scheduling Algorithm: ")
algorithm_label.grid(row=0, column=0, padx=5, pady=5)
algorithm_choice = ttk.Combobox(root, values=['FIFO', 'EDF', 'DMA', 'RMA', 'Preemptive', 'Non_Preemptive', 'RR','MLF'])
algorithm_choice.grid(row=0, column=1, padx=5, pady=5)

# Requests Entry for number of tasks
num_tasks_label = ttk.Label(root, text="Enter number of tasks: ")
num_tasks_label.grid(row=1, column=0, padx=5, pady=5)
num_tasks_entry = ttk.Entry(root)
num_tasks_entry.grid(row=1, column=1, padx=5, pady=5)

# Entry for max_time
max_time_label = ttk.Label(root, text="Enter max time: ")
max_time_label.grid(row=2, column=0, padx=5, pady=5)
max_time_entry = ttk.Entry(root)
max_time_entry.grid(row=2, column=1, padx=5, pady=5)

# Entry for quantum (conditionally displayed)
time_quantum_label = ttk.Label(root, text="Time Quantum:")
time_quantum_label.grid(row=3, column=0, padx=5, pady=5)
time_quantum_entry = ttk.Entry(root)
time_quantum_entry.grid(row=3, column=1, padx=5, pady=5)
time_quantum_label.grid_remove()
time_quantum_entry.grid_remove()

def update_time_quantum_visibility(event):
    if algorithm_choice.get() == 'RR':
        time_quantum_label.grid()
        time_quantum_entry.grid()
    else:
        time_quantum_label.grid_remove()
        time_quantum_entry.grid_remove()

algorithm_choice.bind("<<ComboboxSelected>>", update_time_quantum_visibility)

# Add Task Fields Button
add_task_button = ttk.Button(root, text="Add Task Fields", command=add_task_fields)
add_task_button.grid(row=4, column=1, padx=5, pady=5)

# Run Button
run_button = ttk.Button(root, text="CALCULATE", command=calculate_schedule)
run_button.grid(row=6, column=1, padx=5, pady=5)

# deadline_breaks Label
deadline_breaks_label = ttk.Label(root, text="")
deadline_breaks_label.grid(row=7, columnspan=2, padx=5, pady=5)

root.mainloop()
