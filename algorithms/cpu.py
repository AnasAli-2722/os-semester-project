import pandas as pd

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

class CPUScheduler:
    def fcfs(self, processes):
        processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        timeline = [] 

        for p in processes:
            if current_time < p.arrival_time:
                current_time = p.arrival_time
            
            p.start_time = current_time
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.start_time - p.arrival_time
            
            timeline.append(dict(Task=f"P{p.pid}", Start=p.start_time, Finish=p.completion_time, Resource=f"Process {p.pid}"))
            current_time = p.completion_time
            
        return processes, timeline

    def sjf_non_preemptive(self, processes):
        processes.sort(key=lambda x: x.arrival_time)
        completed = []
        timeline = []
        current_time = 0
        remaining = processes[:]
        
        while remaining:
            available = [p for p in remaining if p.arrival_time <= current_time]
            
            if not available:
                earliest = min(remaining, key=lambda x: x.arrival_time)
                current_time = earliest.arrival_time
                continue
            
            shortest = min(available, key=lambda x: x.burst_time)
            
            shortest.start_time = current_time
            shortest.completion_time = current_time + shortest.burst_time
            shortest.turnaround_time = shortest.completion_time - shortest.arrival_time
            shortest.waiting_time = shortest.start_time - shortest.arrival_time
            
            timeline.append(dict(Task=f"P{shortest.pid}", Start=shortest.start_time, Finish=shortest.completion_time, Resource=f"Process {shortest.pid}"))
            
            current_time = shortest.completion_time
            completed.append(shortest)
            remaining.remove(shortest)
            
        return completed, timeline

    def round_robin(self, processes, quantum):
        processes.sort(key=lambda x: x.arrival_time)
        queue = []
        timeline = []
        current_time = 0
        completed = []
        
        
        active_pool = [p for p in processes] 
        if active_pool:
             queue.append(active_pool.pop(0))
             current_time = queue[0].arrival_time

        while queue or active_pool:
            if not queue:
                next_p = active_pool.pop(0)
                current_time = next_p.arrival_time
                queue.append(next_p)

            p = queue.pop(0)
            
            if p.start_time == -1:
                p.start_time = current_time
            
            exec_time = min(p.remaining_time, quantum)
            timeline.append(dict(Task=f"P{p.pid}", Start=current_time, Finish=current_time + exec_time, Resource=f"Process {p.pid}"))
            
            p.remaining_time -= exec_time
            current_time += exec_time
            
            while active_pool and active_pool[0].arrival_time <= current_time:
                queue.append(active_pool.pop(0))
                
            if p.remaining_time > 0:
                queue.append(p)
            else:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed.append(p)
                
        return completed, timeline