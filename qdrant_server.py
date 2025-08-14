# run_qdrant_docker.py
import subprocess
from pathlib import Path

# Settings
CONTAINER_NAME = "qdrant-local-test2"
HOST_PORT = 6333
DATA_DIR = Path.home() / "qdrant-local-test"
IMAGE = "qdrant/qdrant"

def container_exists(name: str) -> bool:
    """Check if a Docker container exists (running or stopped)."""
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", f"name=^{name}$", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return name in result.stdout.splitlines()

def container_running(name: str) -> bool:
    """Check if a Docker container is currently running."""
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name=^{name}$", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return name in result.stdout.splitlines()

def run_qdrant():
    """Start Qdrant container (create if needed)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if container_exists(CONTAINER_NAME):
        if container_running(CONTAINER_NAME):
            print(f"Container '{CONTAINER_NAME}' is already running.")
        else:
            print(f"Starting existing container '{CONTAINER_NAME}'...")
            subprocess.run(["docker", "start", CONTAINER_NAME], check=True)
            print(f"Container '{CONTAINER_NAME}' started.")
    else:
        print(f"Creating and starting new container '{CONTAINER_NAME}'...")
        cmd = [
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", f"{HOST_PORT}:6333",
            "-v", f"{str(DATA_DIR)}:/qdrant/storage",
            IMAGE
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Qdrant started. Container ID:\n{result.stdout.strip()}")
        else:
            print(f"Error starting Qdrant:\n{result.stderr.strip()}")

def stop_qdrant():
    """Stop Qdrant container if it's running."""
    if container_running(CONTAINER_NAME):
        print(f"Stopping container '{CONTAINER_NAME}'...")
        subprocess.run(["docker", "stop", CONTAINER_NAME], check=True)
        print(f"Container '{CONTAINER_NAME}' stopped.")
    else:
        print(f"Container '{CONTAINER_NAME}' is not running.")

if __name__ == "__main__":
    # Example usage
    run_qdrant()
    # stop_qdrant()  # Uncomment if you want to stop it
