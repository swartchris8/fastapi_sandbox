import requests
import time


# Function to start a new task
def start_task():
    response = requests.post("http://localhost:8000/start-task/")
    if response.status_code == 200:
        return response.json()["job_id"]
    else:
        print(f"Failed to start task: {response.text}")
        return None


# Function to check task status
def check_status(job_id):
    response = requests.get(f"http://localhost:8000/status/{job_id}/")
    if response.status_code == 200:
        return response.json()["status"]
    else:
        print(f"Failed to get status: {response.text}")
        return None


# Start a new task
job_id = start_task()
if job_id:
    print(f"Started new task with job_id: {job_id}")

    # Wait for 2 seconds
    time.sleep(2)

    # Check if the job has started
    status = check_status(job_id)
    print(f"Status after 2 seconds: {status}")

    # Wait for an additional 9 seconds (making it 11 seconds total)
    time.sleep(9)

    # Check if the job is completed
    status = check_status(job_id)
    print(f"Status after 11 seconds: {status}")
