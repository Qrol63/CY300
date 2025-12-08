import pytest
from learning_logs.stats import day_completion, month_completion #(ChatGPT, 2025)

def test_day_completion():
    habits = {"2025-01-08": ["Run", "Study"], "2025-01-09": ["Clean"]}
    completed = {"2025-01-08": ["Run"]}

    result = day_completion("2025-01-08", habits, completed)
    assert result == "Today: 1 out of 2 habits completed."

def test_month_completion():
    habits = {"2025-01-08": ["Run", "Study"], "2025-02-08": ["Clean"]}
    completed = {"2025-01-08": ["Run"]}

    result = month_completion("2025-01", habits, completed)
    assert result == "This Month: 1 out of 2 habits completed."