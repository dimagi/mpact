import os

from mpact.services import schedule_messages

TEST_GROUP_ID = '12345'

def run_test_schedule():
    schedule_file = os.path.join(os.path.dirname(__file__), 'data', 'test_schedules.xlsx')
    with open(schedule_file, 'rb') as f:
        return schedule_messages(f)
