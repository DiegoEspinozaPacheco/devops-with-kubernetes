import time
import uuid
from datetime import datetime, timezone

random_string = str(uuid.uuid4())
FILE_PATH = "/usr/src/app/files/log.txt"

if __name__ == "__main__":
    while True:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        with open(FILE_PATH, "a") as f:
            f.write(f"{timestamp}: {random_string}\n")
        time.sleep(5)