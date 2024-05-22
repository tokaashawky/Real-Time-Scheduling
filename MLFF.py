import matplotlib.pyplot as plt
class Tasks:
    def __init__(self, taskName, releaseTime, period, executionTime, deadLine, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        self.period = period # period of a task is the same as its deadline
        self.executionTime = executionTime
        self.remainingExecution = 0
        self.deadLine = deadLine
        self.deadlineBroken = False
        self.executionTimes = [] #list that contains times of execution
        self.negativeSlackTimes = [] #when slack time of a task is a negative number
        self.brokenDeadlines = [] #when deadline broken 
        
        # time for "new job" of the task is ====>" ready to execute".
        """This list comprehension generates a list of time intervals
        starting from self.releaseTime and ending at maxTime, with a step size of self.period"""
        self.readyTimes = [time for time in self.rangeFloat(self.releaseTime, maxTime+1, self.period)]
        self.readyTimes.append(self.readyTimes[-1] + period)
        #list that contain all deadline of the task during execution
        """iterates over each time in self.readyTimes and calculates the deadline for each task.
        It adds self.deadline to each time in self.readyTimes"""
        self.deadlines = [time + self.deadLine for time in self.readyTimes]
    
    def calcSlackTime(self, t):
        """if task has finished execution means there is no need to calculate its slack time and return none,
        if there is sill remaining execution timewe calculate the slack time of the task then return it"""
        if self.remainingExecution!=0:
            slackTime = (self.deadLine - t)-self.remainingExecution
            if slackTime<0:
                self.negativeSlackTimes.append((t, slackTime)) #broken deadlines
            return slackTime #if remainingExecution!=0
        return None #if remainingExecution=0

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadLine = deadline
                break

    def rangeFloat(self,start, end, step):
        rangelist = [start]
        if step !=0:
            while True:
                start += step
                if start > end:
                    break
                rangelist.append(round(start, 2))
        return rangelist  

class jobs:
    def __init__(self, tasks, maxtime):
        self.tasks = tasks
        self.maxtime = maxtime
        self.tasksSlackTimes =[] #slackTime of each task during the ___whole___ execution
        self.currentTime = 0 #curent time in execution
        self.executeList = []
        
        
        while self.currentTime < maxtime:
            #executing task with the minimum slack time
            minSlackTask = self.getMinSlackTime()
            self.execute(minSlackTask)
    
    def getMinSlackTime(self):
        tasksSlackTime = []
        # Iterate over tasks and their ready times
        for task in self.tasks:
            # Check if task has any ready times
            if task.readyTimes:
                ready_time = task.readyTimes[0]
                if ready_time <= self.currentTime:
                    self.executeList.append(task)
                    task.readyTimes.pop(0)
                    task.remainingExecution = task.executionTime
                task.updateDeadline(self.currentTime)
                tasksSlackTime.append(task.calcSlackTime(self.currentTime))
            else:
                # Skip task if it has no ready times
                continue
    
        tasksSlackTime2 = [slack_time for slack_time in tasksSlackTime if slack_time is not None]
        if not tasksSlackTime2:
            # Handle case when no tasks have remaining execution
            # Update current execution time to the nearest job ready time
            tasksNextReadyTime = [task.readyTimes[0] for task in self.tasks if task.readyTimes]
            if tasksNextReadyTime:
                self.currentTime = min(tasksNextReadyTime)
            else:
                self.currentTime += 1
            self.updateTasksRemainingExecution()
            return self.getMinSlackTime()
    
        minSlackIndex = tasksSlackTime.index(min(tasksSlackTime2))
        self.tasksSlackTimes.append((tasksSlackTime, self.currentTime))
        return self.tasks[minSlackIndex]

     
    def updateTasksRemainingExecution(self):
        for task in self.tasks:
            # Check if task has any ready times
            if task.readyTimes:
                # Check if the task is ready to be executed based on its first ready time
                if task.readyTimes[0] <= self.currentTime:
                    """ If the task has no remaining execution time or its deadline has been broken,
                     reset its remaining execution time and add it to the list of tasks to be executed"""
                    if task.remainingExecution == 0 or task.deadlineBroken:
                        self.executeList.append(task)
                        task.remainingExecution = task.executionTime
                        task.readyTimes.pop(0)  # Remove the first ready time as it has been used
                    task.updateDeadline(self.currentTime)
 
    def execute(self, task):
        startTime = self.currentTime
        endTime = self.getTimeToStop(task)
        task.remainingExecution -= (endTime - startTime)
        # Record the execution time interval
        if endTime > self.maxtime:
            task.executionTimes.append([startTime, self.maxtime])
        else:
            task.executionTimes.append([startTime, endTime])
        # If the task has finished executing, remove it from the execution list
        if task.remainingExecution == 0:
            self.executeList.remove(task)
        # Check if the task has passed its deadline
        self.checkDeadline(endTime)
        # Update the current time to the end time of the task
        self.currentTime = endTime
        # Update the remaining execution time of tasks
        self.updateTasksRemainingExecution()

    def getTimeToStop(self, task):
        tasksNextReadyTime = [t.readyTimes[0] for t in self.tasks]
        # Find the nearest job to be ready from the current execution time
        nearestReadyTime = min(tasksNextReadyTime)
        # If the task's execution finishes before the nearest job is ready, return its end time
        if self.currentTime + task.remainingExecution < nearestReadyTime:
            return self.currentTime + task.remainingExecution
        else:
            # Otherwise, stop the execution at the nearest job's ready time to calculate slack time
            return nearestReadyTime
    
    def checkDeadline(self, t):
        # Check if any task has passed its deadline
        for task in self.tasks:
            if task.remainingExecution != 0 and task.deadLine <= t:
                # If the deadline has been broken, record it and set the flag
                if task.deadLine not in task.brokenDeadlines:
                    task.brokenDeadlines.append(task.deadLine)
                    task.deadlineBroken = True
                    # Check which job breaks the deadline
                    for job in task.executionTimes:
                        if job[1] >= task.deadLine:  # If the job's end time is after the deadline
                            print(f"The job from {task.taskName} which has the release time = {task.releaseTime} breaks its deadline in {task.deadLine}")
                            break  # Break the loop since we found the job that breaks the deadline
            else:
                task.deadlineBroken = False
                
    def getResults(self):
        # Initialize dictionaries to store task information
        exedict = {}
        negativeSlackdict = {}
        brokenDeadlinesdict = {}
        # Initialize list to store overall results
        results = []
        # Populate dictionaries with task information
        for task in self.tasks:
            exedict[f"{task.taskName}"]=task.executionTimes
            negativeSlackdict[f"{task.taskName}"] = f"{task.negativeSlackTimes} "
            brokenDeadlinesdict[f"{task.taskName}"] = task.brokenDeadlines
        # Append dictionaries and other information to the results list    
        results.append(exedict)
        results.append(self.tasksSlackTimes)
        results.append(brokenDeadlinesdict)
        results.append(negativeSlackdict)
        return results  

def draw_timing_diagram8(task_execution_info, max_time):
    plt.figure(figsize=(10, 6))
    # Define a colormap
    cmap = plt.get_cmap('tab10')
    num_colors = len(task_execution_info)
    colors = [cmap(i) for i in range(num_colors)]
    color_dict = {task_name: color for task_name, color in zip(task_execution_info.keys(), colors)}
    # Plotting the execution schedule of tasks
    for task_name, execution_times in task_execution_info.items():
        color = color_dict[task_name]  # Get the color for the task
        for start, end in execution_times:
            plt.plot([start, end], [task_name, task_name], linewidth=5, label=f"{task_name} execution", color=color)
    plt.xlabel("Time")
    plt.ylabel("Task")
    plt.title("Task Execution Timing Diagram")
    plt.yticks(list(task_execution_info.keys()))
    plt.xlim(0, max_time)
    plt.ylim(0, len(task_execution_info) + 1)
    plt.grid(True)
    # Creating custom legend
    handles = [plt.Line2D([0], [0], color=color_dict[task_name], lw=2, label=task_name) for task_name in task_execution_info.keys()]
    plt.legend(handles=handles, loc='upper left')
    plt.show()
    
