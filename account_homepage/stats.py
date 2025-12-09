from datetime import date as date_cls #(ChatGPT, 2025)
from calendar import monthrange #(ChatGPT, 2025)
from .models import Topic, TaskCompletion #(ChatGPT, 2025)

def day_completion(date:str, habits:dict, completed:dict) -> str:
    completed_count = 0
    total = 0
    for item in habits:
        if date in item:
            total += len(habits[item])
    
    for item in completed:
        if date in item:
            completed_count += len(completed[item])
    
    return (f"Today: {completed_count} out of {total} habits completed.")

def month_completion(mon:str, habits:dict, completed:dict) -> str:
    completed_count = 0
    total = 0
    for item in habits:
        if mon in item:
            total += len(habits[item])
    
    for item in completed:
        if mon in item:
            completed_count += len(completed[item])
    
    return (f"This Month: {completed_count} out of {total} habits completed.")