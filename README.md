# Project Title: Task Tracker

Authors: Cadet Dunn, Cadet Rolands
Date: December 9, 2024

## Overview

This website application allows user to do the following things:

- Create tasks or habits
- View completed habits in a calendar format
- Create specific habits and tasks for specific days of the week.

## Files

- accounts: files regarding registration screen and logging in.
- learning_logs: files regarding the homepage and applications for adding tasks/habits. 
- ll_project: Django configurations
- venv: file regarding virtual environment, does not have main website code inside.

## Running the Program

To run the program:

1. Open the command prompt.
2. Start a virtual environment using the following commands and enter the folder:
    - python -m venv llenv
    - cd CY300
3. Run the program with the following command: python manage.py runserver
4. Copy and paste the website link from the command prompt into the web browser to access the site
No additional arguments are required.

## Dependencies

The program requires Python 3.7 or higher and Django. Ensure the following libraries are
installed:

- `csv` (built-in)
- `sys` (built-in)
- 'django'
- 'datetime'
- 'calendar'
- 'import pytest'

## Input

The website takes in your account information along with inputting a task that populates into the calendar.

## Output

The task shows up on specific days of the week on a calendar and allows you to check off the task on the calendar.

## Contact

If you encounter issues running the program, please contact Cadet Rolands at
quinn.rolands@westpoint.edu.