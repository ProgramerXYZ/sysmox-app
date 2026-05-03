import psutil as p
import essntial_functions as e
import json
import setup as s
import time 

# Global vars
def load_json_safe(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        
        return None
    except FileNotFoundError:
        
        return None


def _load_or_create_config():
    data = load_json_safe("config.json")
    if data is None:
        # live fallback
        return {
            "total_physical_memory": p.virtual_memory().total,
            "total_core_count": p.cpu_count(logical=False),
            "total cpu Hyperthred count": p.cpu_count(logical=True),
        }
    return data
def total_physical_memory():
    data = _load_or_create_config()
    return e.byte_value_convert_cpp(data["total_physical_memory"])


def cpuPhy_core_count_():
    data = _load_or_create_config()
    return data["total_core_count"]


def cpu_Hyperthread_count():
    data = _load_or_create_config()
    return data["total cpu Hyperthred count"]


def cpuPercent_IF_INTERVAL_t(intervalTime):
    return p.cpu_percent(interval=intervalTime)


def cpuPercent_DEFAULT():
    return p.cpu_percent(interval=None)


def cpuPercent_percore_IF_INTERVAL_time(intervalTime):
    return p.cpu_percent(interval=intervalTime, percpu=True)


def cpuPercent_percore_DEFAULT():
    return p.cpu_percent(interval=None, percpu=True)


def cpuPhy_core_count():
    return cpuPhy_core_count_()


def cpu_Hyperthred_count():
    return cpu_Hyperthread_count()


# Cpu time Defaults 👇:
def cputime_default(cpu_time_type):
    t = p.cpu_times(percpu=False)

    if cpu_time_type == "user":
        return t.user
    elif cpu_time_type == "system":
        return t.system
    elif cpu_time_type == "idle":
        return t.idle
    else:
        raise ValueError("Unknown CPU time type")


def cputime_percpu(cpu_time_type):
    cpu_times_list = p.cpu_times(percpu=True)
    values = []

    for cpu_times in cpu_times_list:
        if cpu_time_type == "user":
            values.append(cpu_times.user)
        elif cpu_time_type == "system":
            values.append(cpu_times.system)
        elif cpu_time_type == "idle":
            values.append(cpu_times.idle)
        else:
            raise ValueError("Unknown CPU time type")

    return values


def cpu_freq(freq_type):
    f = p.cpu_freq(percpu=False)

    if freq_type == "current":
        return f.current
    elif freq_type == "min":
        return f.min if f.min is not None else f.current
    elif freq_type == "max":
        return f.max if f.max is not None else f.current
    else:
        raise ValueError("Unknown CPU frequency type")

# the cpu frequency data is not very reliable so 

def safe_freq(val, fallback):
    return val if val is not None and val > 0 else fallback

def cpu_freq_percore(cpu_freq_type): 
    frequencies_per_core = p.cpu_freq(percpu=True)
    result = []

    for f in frequencies_per_core:
        current = f.current
        min_v = safe_freq(f.min, current)
        max_v = safe_freq(f.max, current)

        if cpu_freq_type == "current":
            result.append(current)

        elif cpu_freq_type == "min":
            result.append(min_v)

        elif cpu_freq_type == "max":
            result.append(max_v)

        elif cpu_freq_type == "all":
            result.append({
                "current": current,
                "min": min_v,
                "max": max_v
            })

        else:
            raise ValueError("Unknown CPU frequency type")

    return result

def cpu_all(interval=0.05):
    return {
        "cores": {
            "physical": cpuPhy_core_count(),
            "logical": cpu_Hyperthred_count()
        },

        "percent": {
            "overall": cpuPercent_IF_INTERVAL_t(interval) if interval is not None else cpuPercent_DEFAULT(),
            "per_core": cpuPercent_percore_IF_INTERVAL_time(interval) if interval is not None else cpuPercent_percore_DEFAULT()
        },

        "times": {
            "overall": {
                "user": cputime_default("user"),
                "system": cputime_default("system"),
                "idle": cputime_default("idle")
            },
            "per_core": {
                "user": cputime_percpu("user"),
                "system": cputime_percpu("system"),
                "idle": cputime_percpu("idle")
            }
        },

        "frequency": {
            "overall": {
                "current": cpu_freq("current"),
                "min": cpu_freq("min"),
                "max": cpu_freq("max")
            },
            "per_core": cpu_freq_percore("all")
        }
    }



#  def get_cpu_info(cpu_info):
#     if cpu_info=="cpu.percentage":
#         return p.cpu_percent(interval=1)
#     elif cpu_info=="cpu.percentage-percore":
#         return p.cpu_percent(interval=1, percpu=True)
#     elif cpu_info == "cpu phycores -a":
#         return p.cpu_count(logical=False)
#     elif cpu_info == "cpu core -a":
#         return p.cpu_count(logical=True)
#     elif cpu_info == "cpu.times":
#         return p.cpu_times(percpu=False)
#     elif cpu_info == "cpu.freq":
#         return p.cpu_freq(percpu=True)
#     elif cpu_info == "cpu.stats":
#         return p.cpu_stats()
#     else:
#         return "Invalid CPU info request"

# ALL MEMORY REALTED STUFF IS HERE 👇
def mem():
    return p.virtual_memory()

def total_physical_memory():
    data = _load_or_create_config()
    return data["total_physical_memory"]

def memory_available():
    return mem().available

def memory_used():
    m = mem()
    return m.total - m.available

def memory_percent():
    return mem().percent

def all_mem():
    m = mem()
    return {
        "total": m.total,
        "available": m.available,
        "used": m.total - m.available,
        "percent": m.percent,
    }



def reconfig():
    s.create_config()

INTERVAL = 0.032  # 50 ms
_last_sample_time = time.time()

def all():
    global _last_sample_time

    now = time.time()

    # if we're early → wait
    if now < _last_sample_time:
        time.sleep(_last_sample_time - now)
        _last_sample_time += INTERVAL

    else:
        # if we're late → reset schedule (avoid drift explosion)
        _last_sample_time = now + INTERVAL

    all_data={
        "collection_time": time.time_ns() // 1_000_000,
        "cpu": cpu_all(),
        "memory": all_mem(),
    }
    
    return all_data


