from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    timestamp: str
    ip: str
    method: str
    path: str
    status_code: Optional[int]
    response_time_ms: float