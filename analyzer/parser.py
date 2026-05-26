import json
import re
from datetime import datetime
from analyzer.models import LogEntry


STANDARD_LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\S+(?:\s+\S+)?)\s+'
    r'(?P<ip>\S+)\s+'
    r'(?P<method>GET|POST|PUT|DELETE|PATCH)\s+'
    r'(?P<path>\S+)\s+'
    r'(?P<status>\d+|-)\s+'
    r'(?P<response>\S+)'
)


def normalize_response_time(value):
    """
    Convert response times into milliseconds.
    Supports:
    - 142ms
    - 0.142s
    - 142
    """
    value = value.strip()

    if value.endswith("ms"):
        return float(value[:-2])

    if value.endswith("s"):
        return float(value[:-1]) * 1000

    return float(value)


def normalize_timestamp(timestamp):
    """
    Attempt multiple timestamp formats.
    """
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y/%m/%d %H:%M:%S",
        "%d-%b-%Y %H:%M:%S"
    ]

    # Unix epoch
    if timestamp.isdigit():
        return datetime.utcfromtimestamp(int(timestamp)).isoformat()

    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt).isoformat()
        except ValueError:
            continue

    return timestamp


def parse_json_line(line):
    """
    Parse JSON formatted log line.
    """
    data = json.loads(line)

    return LogEntry(
        timestamp=normalize_timestamp(
            str(data.get("timestamp", "unknown"))
        ),
        ip=data.get("ip", "unknown"),
        method=data.get("method", "UNKNOWN"),
        path=data.get("path", "unknown"),
        status_code=(
            int(data["status"])
            if str(data.get("status", "-")).isdigit()
            else None
        ),
        response_time_ms=normalize_response_time(
            str(data.get("response_time", "0"))
        )
    )


def parse_standard_line(line):
    """
    Parse traditional log format.
    """
    match = STANDARD_LOG_PATTERN.match(line)

    if not match:
        return None

    data = match.groupdict()

    status = data["status"]

    return LogEntry(
        timestamp=normalize_timestamp(data["timestamp"]),
        ip=data["ip"],
        method=data["method"],
        path=data["path"],
        status_code=int(status) if status.isdigit() else None,
        response_time_ms=normalize_response_time(
            data["response"]
        )
    )


def parse_line(line):
    """
    Main parsing pipeline.
    Returns:
    - LogEntry if valid
    - None if malformed
    """

    line = line.strip()

    if not line:
        return None

    try:
        # Attempt JSON parsing
        if line.startswith("{"):
            return parse_json_line(line)

        # Attempt standard parsing
        parsed = parse_standard_line(line)

        if parsed:
            return parsed

    except Exception:
        return None

    return None