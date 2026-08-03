import time
import uuid
from datetime import datetime, timezone

random_string = str(uuid.uuid4())

if __name__ == "__main__":
    while True:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        print(f"{timestamp}: {random_string}", flush=True)
        time.sleep(5)