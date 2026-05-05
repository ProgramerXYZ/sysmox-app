
# from essntial_functions import (
#     validate_intervaltime,
#     max_freq_hit_interval_percore,
#     min_freq_hit_interval_percore,
#     max_freq_hit_interval,
#     min_freq_hit_interval,
#     show_error_report_popup as err
#)
# from argparse import ArgumentParser , RawTextHelpFormatter 
import time

import main as m
# import sys
from description import description as d

import json as j

# NOTE: CLI argument structure frozen until post-exams refactor


def main():

    # parser = ArgumentParser(
    #     description=d, 
    #     formatter_class=RawTextHelpFormatter
    # )

    # # Main command argument
    # parser.add_argument(
    #     "main_command"
    # )

    # # p=parser()
    data = m.all()


    p = input()
    x=False
    
    if p== "all":
        x = True
    SAMPLES_PER_SEC =  30


    INTERVAL = 1.0 / SAMPLES_PER_SEC
    
    while x:
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
        print (j.dumps(data),flush=True)
        print("|||")
        

if __name__ == "__main__":
    main()