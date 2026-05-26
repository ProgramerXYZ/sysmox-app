import json
import time
import gc
import main as m

def main():
    SAMPLES_PER_SEC = 30
    INTERVAL = 1.0 / SAMPLES_PER_SEC

    batch_count = 0

    while True:
        batch = []
        second_start = time.perf_counter()

        while time.perf_counter() - second_start < 1.0:
            start = time.perf_counter()

            data = m.all()
            batch.append(data)

            elapsed = time.perf_counter() - start
            sleep_time = INTERVAL - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)

        print(json.dumps(batch), flush=True)
        print("|||", flush=True)

        # destroy old batch explicitly
        del batch

        batch_count += 1

        # periodic cleanup
        if batch_count % 60 == 0:
            gc.collect()

main()