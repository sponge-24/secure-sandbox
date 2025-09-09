import redis
import json
import docker
import tempfile
import os

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Connect to Docker
client = docker.from_env()

print("Worker started, waiting for jobs...")

while True:
    # Blocking pop: wait for new jobs
    _, job_data = r.brpop("job_queue")
    job = json.loads(job_data)

    job_id = job["id"]
    code = job["code"]
    lang = job.get("lang", "python")

    print(f"Running job {job_id} ({lang})")

    # Create temp dir and write code to file
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "main.py")
        with open(file_path, "w") as f:
            f.write(code)
        print(f"Code written to {file_path}")
        try:
            # Run in Docker (Python only for now)
            output = client.containers.run(
                "python:3.11",                      # sandbox image
                command="timeout 5 python /code/main.py",     # run file inside container
                volumes={tmpdir: {"bind": "/code", "mode": "ro"}},
                network_disabled=True,              # no internet
                mem_limit="256m",                   # memory cap
                nano_cpus=500_000_000,              # 0.5 CPU
                remove=True,                        # auto cleanup
                stderr=True,
                stdout=True
            )
            result = output.decode()
            r.set(f"result:{job_id}", result)
            r.set(f"status:{job_id}", "done")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            r.set(f"result:{job_id}", error_msg)
            r.set(f"status:{job_id}", "done")

    print(f"Job {job_id} finished")
