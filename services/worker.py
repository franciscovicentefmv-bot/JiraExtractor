from threading import Thread
from uuid import uuid4

JOBS = {}


def run_job(fn, *args, **kwargs):
    job_id = str(uuid4())

    JOBS[job_id] = {
        "status": "running",
        "progress": 0,
        "result": None
    }

    def wrapper():
        try:
            result = fn(job_id, *args, **kwargs)
            JOBS[job_id]["status"] = "done"
            JOBS[job_id]["result"] = result
        except Exception as e:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["result"] = str(e)

    Thread(target=wrapper, daemon=True).start()

    return job_id


def update_progress(job_id, value):
    if job_id in JOBS:
        JOBS[job_id]["progress"] = value


def get_job(job_id):
    return JOBS.get(job_id)
