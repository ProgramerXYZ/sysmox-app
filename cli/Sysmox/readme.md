# Sysmox

Sysmox is a lightweight, terminal-based system monitoring tool focused on providing clear and reliable **CPU-related information** through simple, human-readable commands.

It is designed to be fast, minimal, and transparent—doing one thing well instead of trying to do everything at once.

> **Current Release:** v0.2.0-beta

---

## ✨ What is Sysmox?

Sysmox is a command-line utility that allows you to inspect CPU information such as frequency, core-level data, and basic processor characteristics directly from the terminal.

It is intended for:

- Developers
- Power users
- Students learning system internals
- Anyone who prefers CLI tools over heavy GUIs

Sysmox currently focuses **only on CPU monitoring**. Other system components may be added in future versions, but are not part of this release.

---

## 🚀 Features

- Simple and predictable command structure
- CPU frequency reporting (current / min / max)
- Per-core CPU data (when supported by the system)
- Lightweight and fast execution
- Designed with cross-platform support in mind; currently available on Windows due to platform-specific binary dependencies
- No background services
- No telemetry or data collection

---

## 🧾 Available Commands

Sysmox uses a **command + flags** structure. The first argument specifies the main CPU-related command, and optional flags modify its behavior. Some commands support interval-based monitoring and per-core output.

---

### General

```text
sysmox --help
```

Displays usage information and all available commands and flags.

```text
sysmox --version
```

Displays the installed Sysmox version.

---

### CPU Usage Percentage

```text
sysmox cpupercent
sysmox cpu%
```

Displays overall CPU usage percentage.

Options:

- `-pc, --percore` → Show CPU usage per core
- `-i, --intervaltime <seconds>` → Measure usage over a time interval
- `-a, --all` → Show all available CPU percentage data

Examples:

```text
sysmox cpupercent -i 2
sysmox cpu% --percore
```

---

### CPU Core & Thread Count

```text
sysmox cpucount
sysmox cpu#
```

Displays CPU core and thread information.

Options:

- `-c, --phycore` → Show physical core count
- `-t, --thread` → Show logical thread count

---

### CPU Time Statistics

```text
sysmox cpu_time
sysmox cpuT
```

Displays CPU time statistics.

Options:

- `-u, --user` → User mode CPU time
- `-s, --system` → System mode CPU time
- `-I, --idle` → Idle CPU time
- `-pc, --percore` → Per-core CPU time statistics

---

### CPU Frequency

```text
sysmox cpu_frequency
sysmox cpuF
```

Displays CPU frequency information.

Options:

- `-C, --current` → Current CPU frequency
- `-m, --min` → Minimum CPU frequency
- `-M, --max` → Maximum CPU frequency
- `-pc, --percore` → Per-core frequency information
- `-i, --intervaltime <seconds>` → Frequency over a monitoring interval

---

### Reconfiguration

```text
sysmox reconfig
sysmox reconf
```

Re-runs Sysmox configuration or environment setup.

---

### CPU Commands

```text
sysmox cpu
```

Displays general CPU information.

```text
sysmox cpu --current
```

Shows the current CPU frequency.

```text
sysmox cpu --min
```

Shows the minimum CPU frequency (if available on the system).

```text
sysmox cpu --max
```

Shows the maximum CPU frequency (if available on the system).

```text
sysmox cpu --percore
```

Displays per-core CPU frequency information. Output depends on hardware and OS support.

---

## 🪟 Windows SmartScreen Notice

Sysmox is currently distributed as an **unsigned beta executable**.

When running the installer, Windows may display a "Windows protected your PC" warning.

To proceed:

1. Click **More info**
2. Click **Run anyway**

This is expected behavior for early-stage software and does not indicate malicious activity.

---

## 🧪 Release Status

- Version: **v0.1.0-beta**
- Platform: **Windows**
- Release type: **Public beta**
- Scope: **CPU monitoring only**

This release is intended for testing and feedback. Command behavior and output may change in future versions.

---

## 🧠 Design Philosophy

Sysmox follows a minimal and transparent design philosophy:

- One responsibility per feature
- Explicit output over hidden behavior
- No silent background processes
- Clear CLI-first workflow

The goal is not to replace existing system monitors, but to provide a clean, understandable tool for inspecting CPU behavior.

---

## 📌 Installation

Download the installer from the **Releases** section of this repository and follow the on-screen instructions.

After installation, the `sysmox` command will be available in the terminal.

---

## 📬 Feedback & Contributions

Feedback, bug reports, and suggestions are welcome.

If you encounter issues, please open a GitHub Issue with:

- The command used
- Expected output
- Actual output
- Your Windows version

---

Sysmox is an evolving project. Each release focuses on stability, clarity, and incremental improvement.

