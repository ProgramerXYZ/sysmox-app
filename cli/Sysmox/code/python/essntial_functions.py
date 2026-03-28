import sys
import json, os
import subprocess
import psutil
import time
import tkinter as tk
import webbrowser
import urllib.parse


# error handleling
def show_error_report_popup(error_message):
    """
    Shows a popup with Report and Close buttons.
    Report opens GitHub with the error pre-filled.
    """

    GITHUB_ISSUE_URL = "https://github.com/ProgramerXYZ/Sysmox-releses/issues/new"

    # Encode error for URL
    body_text = f"### Error Report\n\n```\n{error_message}\n```"
    encoded_body = urllib.parse.quote(body_text)

    report_url = f"{GITHUB_ISSUE_URL}?body={encoded_body}"

    root = tk.Tk()
    root.title("Sysmon Error")
    root.geometry("520x260")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text="Sysmon encountered an error.\n\nPlease report this issue so it can be fixed.",
        wraplength=480,
        justify="left",
    )
    label.pack(pady=10)

    text_box = tk.Text(root, height=6, width=60)
    text_box.insert("1.0", error_message)
    text_box.config(state="disabled")
    text_box.pack(padx=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=15)

    def report():
        webbrowser.open(report_url)
        root.destroy()

    def close():
        root.destroy()

    report_btn = tk.Button(button_frame, text="Report", width=12, command=report)
    close_btn = tk.Button(button_frame, text="Close", width=12, command=close)

    report_btn.pack(side="left", padx=10)
    close_btn.pack(side="right", padx=10)

    root.mainloop()


# file handeling
from pathlib import Path
import sys


def get_runtime_dir():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent


CPP_BIN_DIR = get_runtime_dir() / "cpp_bin"


def get_cpp_executable(name):
    exe_name = f"{name}.exe" if sys.platform.startswith("win") else name
    exe_path = CPP_BIN_DIR / exe_name

    if not exe_path.exists():
        error_msg = (
            f"C++ helper executable not found:\n{exe_path}\n\n"
            "Please report this issue on the Sysmon GitHub repository."
        )
        show_error_report_popup(error_msg)
        raise FileNotFoundError(error_msg)

    return str(exe_path)


"""much more optimized code will use later """
# import subprocess

# class CPPFormatter:
#     def __init__(self, exe_path):
#         self.process = subprocess.Popen(
#             [exe_path],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             text=True
#         )

#     def send(self, value):
#         # send value and flush input
#         self.process.stdin.write(str(value) + "\n")
#         self.process.stdin.flush()
#         # read one line of output
#         return self.process.stdout.readline().strip()

#     def close(self):
#         self.process.stdin.close()
#         self.process.terminate()
#         self.process.wait()

# # Usage
# bytes_formatter = CPPFormatter("./format_size.exe")
# time_formatter = CPPFormatter("./format_time.exe")
# duration_formatter = CPPFormatter("./duration_format.exe")

# # Call repeatedly without restarting
# result1 = bytes_formatter.send(68893)
# result2 = time_formatter.send(3666)
# result3 = duration_formatter.send(4520)


# # Close all when done
# bytes_formatter.close()
# time_formatter.close()
# duration_formatter.close()
# Run the C++ executable
def byte_value_convert_cpp(bytes_value):
    process = subprocess.Popen(
        [get_cpp_executable("format_size")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    # Send the number and capture output
    out, _ = process.communicate(str(bytes_value))
    return out.strip()


# Run the C++ executable for time formatting
def time_value_convert_cpp(seconds_value):
    process = subprocess.Popen(
        [get_cpp_executable("format_time")],  # your compiled C++ time formatter
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    out, _ = process.communicate(str(seconds_value))
    return out.strip()


def duration_format_cpp(seconds_value):
    process = subprocess.Popen(
        [get_cpp_executable("duration_format")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    out, _ = process.communicate(str(seconds_value))
    return out.strip()


def Mhz_to_Ghz_convertion(Hertz_val):
    process = subprocess.Popen(
        [get_cpp_executable("format_to_ghz")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    out, _ = process.communicate(str(Hertz_val))
    return out.strip()


def validate_intervaltime(interval):

    if interval is not None and interval <= 0:
        print("Invalid interval time. Must be greater than zero.")
        sys.exit(1)  # clean exit with error code


def check_json_integrity(json_path):
    try:
        with open(json_path, "r") as file:
            json.load(file)  # Try reading the JSON
        return True  # No issues
    except json.JSONDecodeError:
        print("⚠️ The JSON file appears to be corrupted. Deleting it...")
        os.remove(json_path)
        print("Please try running 'sysmon reconfig' again to regenerate it.")
        return False
    except FileNotFoundError:
        # Missing is fine; we don't touch this case
        print(
            "The config.json file is missing plz try to reconfigure sysmon you can reconfigure it by running 'sysmon reconfig'command"
        )
        return False


def max_freq_hit_interval_percore(interval):
    # get number of cores
    core_count = len(psutil.cpu_freq(percpu=True))
    highest = [0.0] * core_count  # store GHz floats

    start = time.time()

    while time.time() - start < interval:
        freqs = psutil.cpu_freq(percpu=True)
        for i, f in enumerate(freqs):
            ghz = f.current / 1000.0  # psutil gives MHz, convert to GHz
            if ghz > highest[i]:
                highest[i] = ghz

    # ---- SEND RESULTS TO C++ ----
    # Create a single string: "3.20 3.10 2.95 3.00"
    send_string = " ".join(f"{v:.4f}" for v in highest)

    process = subprocess.Popen(
        [get_cpp_executable("format_freq_percore")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    out, _ = process.communicate(send_string)
    return out.strip()


def min_freq_hit_interval_percore(interval):
    # get number of cores
    core_count = len(psutil.cpu_freq(percpu=True))
    lowest = [9999.0] * core_count  # start with a very high number (GHz)

    start = time.time()

    while time.time() - start < interval:
        freqs = psutil.cpu_freq(percpu=True)

        for i, f in enumerate(freqs):
            ghz = f.current / 1000.0  # current MHz → GHz
            if ghz < lowest[i]:
                lowest[i] = ghz

    # ---- SEND RESULTS TO C++ ----
    # Create a single string: "1.20 1.35 1.10 1.15"
    send_string = " ".join(f"{v:.4f}" for v in lowest)

    process = subprocess.Popen(
        [get_cpp_executable("format_freq_percore")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    out, _ = process.communicate(send_string)
    return out.strip()


def max_freq_hit_interval(interval):
    highest = 0.0  # GHz

    start = time.time()

    while time.time() - start < interval:
        f = psutil.cpu_freq(percpu=False)
        ghz = f.current / 1000.0  # MHz → GHz
        if ghz > highest:
            highest = ghz

    # send single value to C++
    send_string = f"{highest:.4f}"

    process = subprocess.Popen(
        [get_cpp_executable("format_freq")],  # single-value formatter
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    out, _ = process.communicate(send_string)
    return out.strip()


def min_freq_hit_interval(interval):
    lowest = 9999.0  # GHz (intentionally very high)

    start = time.time()

    while time.time() - start < interval:
        f = psutil.cpu_freq(percpu=False)
        ghz = f.current / 1000.0  # MHz → GHz
        if ghz < lowest:
            lowest = ghz

    # send single value to C++
    send_string = f"{lowest:.4f}"

    process = subprocess.Popen(
        [get_cpp_executable("format_freq")],  # single-value formatter
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    out, _ = process.communicate(send_string)
    return out.strip()
