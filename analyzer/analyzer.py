from collections import Counter, defaultdict


class LogAnalyzer:
    def __init__(self):
        self.total_lines = 0
        self.valid_lines = 0
        self.malformed_lines = 0

        self.status_codes = Counter()
        self.ip_counter = Counter()
        self.anomaly_counts = Counter()

        self.endpoint_times = defaultdict(list)

    def process_entry(self, entry):
        self.valid_lines += 1

        if entry.status_code:
            self.status_codes[entry.status_code] += 1

        self.ip_counter[entry.ip] += 1

        self.endpoint_times[entry.path].append(
            entry.response_time_ms
        )

    def process_malformed(self):
        self.malformed_lines += 1
    
    def process_anomaly(self, anomaly_type):
        self.anomaly_counts[anomaly_type] += 1

    def generate_report(self):
        report = []

        report.append("==== LOG ANALYSIS REPORT ====\n")

        report.append(f"Total lines: {self.total_lines}")
        report.append(f"Valid lines: {self.valid_lines}")
        report.append(f"Malformed lines: {self.malformed_lines}\n")

        report.append("Status Codes:")

        for code, count in self.status_codes.items():
            report.append(f"  {code}: {count}")

        report.append("\nTop IP Addresses:")

        for ip, count in self.ip_counter.most_common(5):
            report.append(f"  {ip}: {count}")

        report.append("\nSlowest Endpoints:")

        averages = []

        for path, times in self.endpoint_times.items():
            avg = sum(times) / len(times)
            averages.append((path, avg))

        averages.sort(key=lambda x: x[1], reverse=True)

        for path, avg in averages[:5]:
            report.append(f"  {path}: {avg:.2f}ms")

        return "\n".join(report)