import time

import requests
import pytest

from models import TaskStatusEnum, Base, engine

BASE_URL = "http://localhost:8000"


def start_task():
    response = requests.post(f"{BASE_URL}/start-task/")
    if response.status_code == 200:
        return response.json()["job_id"]
    else:
        pytest.fail(f"Failed to start task: {response.text}")


def check_status(job_id):
    response = requests.get(f"{BASE_URL}/status/{job_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        pytest.fail(f"Failed to get status: {response.text}")


def test_task_lifecycle():
    # Step 1: Submit a task
    job_id = start_task()
    assert job_id is not None, "Job ID should not be None"

    # Step 2: Check if the job is started 2 seconds after submitting the task
    time.sleep(2)
    status = check_status(job_id)
    assert (
        status["status"] == TaskStatusEnum.STARTED
    ), f"Expected status 'started', got {status}"

    # Step 3: Check if the job is completed 11 seconds after submitting the task
    time.sleep(9)  # We already waited 2 seconds, so we wait an additional 9 seconds
    status = check_status(job_id)
    assert (
        status["status"] == TaskStatusEnum.COMPLETED
    ), f"Expected status 'completed', got {status}"
    assert status["result"] == "Prompt results are here"


# More info on how to do setup / teardown on a more granular database level
# https://stackoverflow.com/a/67348153
@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Setup
    Base.metadata.create_all(bind=engine)

    yield  # this is where the testing happens

    # Teardown
    Base.metadata.drop_all(bind=engine)
