#!/usr/bin/env python3
from essntial_functions import (
    validate_intervaltime,
    max_freq_hit_interval_percore,
    min_freq_hit_interval_percore,
    max_freq_hit_interval,
    min_freq_hit_interval,
    show_error_report_popup as err
)
from argparse import ArgumentParser , RawTextHelpFormatter
import main as m
import sys
from description import description as d

# NOTE: CLI argument structure frozen until post-exams refactor


def main():

    parser = ArgumentParser(
        description=d, 
        formatter_class=RawTextHelpFormatter
    )

    # Main command argument
    parser.add_argument(
        "main_command",
        help="Specify the monitoring option:\n"
        "  'cpu_percent' or 'cpu%%': Show CPU usage percentage\n"
        "  'cpucount' or 'cpu#': Show CPU core count\n"
        "  'cpu_time' or 'cpuT': Show CPU time statistics",
    )
    # Global arguments
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
    )

    # CPU monitoring options
    parser.add_argument(
        "-p", "--percore", action="store_true", help="Show statistics per CPU core"
    )
    parser.add_argument(
        "-i",
        "--intervaltime",
        type=float,
        help="Interval time in seconds for monitoring (recommended: 1-10)",
    )
    parser.add_argument(
        "-c", "--phycore", action="store_true", help="Show physical core count"
    )
    parser.add_argument("-t", "--thread", action="store_true", help="Show thread count")

    # CPU time specific options
    parser.add_argument(
        "-u", "--user", action="store_true", help="Show CPU time in user mode"
    )
    parser.add_argument(
        "-s", "--system", action="store_true", help="Show CPU time in system mode"
    )
    parser.add_argument("-I", "--idle", action="store_true", help="Show CPU idle time")

    # CPU freq options
    parser.add_argument(
        "-C", "--current", action="store_true", help="Show CPU current frequency"
    )

    parser.add_argument(
        "-m", "--min", action="store_true", help="Show the minimum CPU frequency"
    )

    parser.add_argument(
        "-M", "--max", action="store_true", help="Show the maximum CPU frequency"
    )

    # Memmory commands 



    args = parser.parse_args()

    intervaltime = int(args.intervaltime) if args.intervaltime is not None else None

    # Validate interval time if provided
    try:
        validate_intervaltime(intervaltime)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle CPU percentage monitoring
    if args.main_command in {"cpupercent", "cpu%"}:
        try:
            if args.percore:
                if intervaltime is not None and intervaltime > 0:
                    print(
                        f"CPU percentage per core for {intervaltime }s: {m.cpuPercent_percore_IF_INTERVAL_time(intervaltime)}%"
                    )
                else:
                    print(f"CPU percentage per core: {m.cpuPercent_percore_DEFAULT()}")
            else:
                if intervaltime is not None and intervaltime > 0:
                    print(
                        f"CPU percentage for {intervaltime }s: {m.cpuPercent_IF_INTERVAL_t(intervaltime)}%"
                    )
                else:
                    print(f"CPU percentage: {m.cpuPercent_DEFAULT()}%")
        except Exception as e:
            print(f"❌ Error retrieving CPU percentage: {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    # Handle CPU count information
    elif args.main_command in {"cpucount", "cpu#"}:
        try:
            if args.phycore:
                print(f"Number of physical CPU cores: {m.cpuPhy_core_count()}")
            if args.thread:
                print(f"Number of CPU threads: {m.cpu_Hyperthread_count()}")
            if not args.phycore and not args.thread:
                print(
                    "Invalid command!\nUse one of these options:\n  '-t', '--thread': Show thread count\n  '-c', '--phycore': Show physical core count"
                )
        except Exception as e:
            print(f"❌ Error retrieving CPU count: {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    # Handle CPU time statistics
    elif args.main_command in {"cpu_time", "cpuT"}:
        try:
            if args.percore:
                if args.user:
                    print(f"Cpu time of the user is {m.cputime_percpu('user')}")
                if args.system:
                    print(f"Cpu time of the system is {m.cputime_percpu('system')}")
                if args.idle:
                    print(f"Cpu time of the idle is  {m.cputime_percpu('idle')}")
            else:
                if args.user:
                    print(f"Cpu time of the user is {m.cputime_default('user')}")
                if args.system:
                    print(f"Cpu time of the system is {m.cputime_default('system')}")
                if args.idle:
                    print(f"Cpu time of the idle is  {m.cputime_default('idle')}")
        except Exception as e:
            print(f"❌ Error retrieving CPU time: {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    # Handle cpuTime percent(%) here 👇
    # will do later

    # Handle cpu frequency

    elif args.main_command in {"cpu_frequency", "cpuF"}:
        try:
            if args.percore:
                if args.current:
                    print(
                        f"The Current cpu frequency is {m.cpu_freq_percore('current')}f"
                    )
                if args.min:

                    if intervaltime is not None and intervaltime > 0:
                        print(
                            f"The minimum frequency for each core in the interval of {intervaltime}s is {min_freq_hit_interval_percore(intervaltime )}"
                        )

                    else:
                        print(
                            f"The minimum cpu frequency for each core capacity is {m.cpu_freq_percore('min')}f"
                        )

                if args.max:
                    if intervaltime is not None and intervaltime > 0:
                        print(
                            f"The maximum frequency for each core in the interval of {intervaltime }s is {max_freq_hit_interval_percore(intervaltime )}"
                        )
                    else:
                        print(
                            f"The maximum cpu frequency capacity is {m.cpu_freq_percore('max')}f"
                        )
            else:
                if args.current:
                    print(f"Your current cpu frequency is {m.cpu_freq('current')}f")
                if args.min:
                    if intervaltime is not None and intervaltime > 0:
                        print(
                            f"The minimum cpu frequency in the interval of {intervaltime }s is {min_freq_hit_interval(intervaltime )}f"
                        )
                    else:
                        print(
                            f"The minimum cpu frequency capacity is {min_freq_hit_interval(intervaltime)}f"
                        )
                if args.max:
                    if intervaltime is not None and intervaltime > 0:
                        print(
                            f"The maximum cpu frequency in the interval of {intervaltime}s is {max_freq_hit_interval(intervaltime)}f"
                        )
                    else:
                        print(
                            f"The maximum cpu frequency capacity is {min_freq_hit_interval(intervaltime)}f"
                        )
        except FileNotFoundError as e:
            print(f"❌ {e}", file=sys.stderr)
            err(e)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error retrieving CPU frequency: {e}", file=sys.stderr)
            err(e)
            sys.exit(1)
    # ----------------------------------------------------------------------------
    #                                MEMORY
    # ----------------------------------------------------------------------------
    elif args.main_command in {"mem#" , "totalmemory", "totalmem" , "mem total"}:
        try:
            print(f"Total memory is : {m.total_physical_memory()}")

        except FileNotFoundError as e:
            print(f"❌ Config.json was not found \n try reconfiguring by try typing 'sysmox reconfig' {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

        except Exception as e:
            print(f"❌ Error retriving the total memmory {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    elif args.main_command in {"mem avail", "avalable memeory" , "mem~", "m~"}:
        try:
            print(f"Avalable memory is : {m.Avalable_memory()}")
        except FileNotFoundError as e:
            print(f"❌ Config.json was not found \ntry reconfiguring by try typing 'sysmox reconfig' {e}", file=sys.stderr)
            err(e)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error retriving the total memmory {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    elif args.main_command in {"mem used", "mem+", "used memory", "used mem", "m+"}:
        try:
            print(f"Active memory is : {m.Used_memory()}")
        except FileNotFoundError as e:
            print(f"❌ Config.json was not found \ntry reconfiguring by try typing 'sysmox reconfig' {e}", file=sys.stderr)
            err(e)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error retriving the Active memory{e}", file=sys.stderr)
            err(e)
            sys.exit(1)
    elif args.main_command in {"mem%", "memory%", "memory percent"}:
        try:
            print(f"Memory usage % is : {m.percent()}")
        except FileNotFoundError as e:
            print(f"❌ Config.json was not found \ntry reconfiguring by try typing 'sysmox reconfig' {e}", file=sys.stderr)
            err(e)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error retriving the memory percentage\n{e}", file=sys.stderr)
            err(e)
            sys.exit(1)
    # ----------------------------------------------------------------------------
    #                                RECONFIG
    # ----------------------------------------------------------------------------

    elif args.main_command in {"reconf", "reconfig"}:
        try:
            m.reconfig()
        except Exception as e:
            print(f"❌ Error during reconfiguration: {e}", file=sys.stderr)
            err(e)
            sys.exit(1)

    else:
        print(f"❌ Unknown command: '{args.main_command}'", file=sys.stderr)
        print(
            "\nValid commands: cpupercent, cpu#, cpucount, cpu_time, cpuT, cpu_frequency, cpuF, reconfig",
            file=sys.stderr,
        )
        sys.exit(1)

                    

if __name__ == "__main__":
    main()
