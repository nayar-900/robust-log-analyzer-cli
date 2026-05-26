# Robust Log Analyzer CLI

A resilient command-line log analysis tool built in Python that processes mixed-format server logs and generates operational insights while gracefully handling malformed data.

---

## Features

- Parses standard server log entries
- Supports JSON-formatted log lines
- Handles multiple timestamp formats
- Normalizes response times (`ms`, `s`, raw values)
- Gracefully skips malformed lines
- Tracks malformed/anomalous entries
- Displays:
  - Status code distribution
  - Top IP addresses
  - Slowest endpoints
  - Summary statistics

---

## Project Structure

```text
log-analyzer/
│
├── analyzer/
├── scripts/
├── sample_logs/
├── main.py
├── README.md
├── ANSWERS.md
└── requirements.txt