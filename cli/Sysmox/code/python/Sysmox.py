
# from essntial_functions import (
#     validate_intervaltime,
#     max_freq_hit_interval_percore,
#     min_freq_hit_interval_percore,
#     max_freq_hit_interval,
#     min_freq_hit_interval,
#     show_error_report_popup as err
#)
from argparse import ArgumentParser , RawTextHelpFormatter
import main as m
# import sys
from description import description as d

# NOTE: CLI argument structure frozen until post-exams refactor


def main():

    parser = ArgumentParser(
        description=d, 
        formatter_class=RawTextHelpFormatter
    )

    # Main command argument
    parser.add_argument(
        "main_command"
    )
    print(m.all())
if __name__ == "__main__":
    main()