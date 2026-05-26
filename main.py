import argparse

from rich.console import Console
from rich.table import Table

from analyzer.parser import parse_line
from analyzer.analyzer import LogAnalyzer


console = Console()


def display_report(analyzer):
    console.print("\n[bold cyan]==== LOG ANALYSIS REPORT ====[/bold cyan]\n")

    summary = Table(title="Summary")
    summary.add_column("Metric", style="green")
    summary.add_column("Value", style="yellow")

    summary.add_row("Total Lines", str(analyzer.total_lines))
    summary.add_row("Valid Lines", str(analyzer.valid_lines))
    summary.add_row("Malformed Lines", str(analyzer.malformed_lines))

    console.print(summary)

    status_table = Table(title="Status Codes")
    status_table.add_column("Status")
    status_table.add_column("Count")

    for code, count in analyzer.status_codes.items():
        status_table.add_row(str(code), str(count))

    console.print(status_table)

    ip_table = Table(title="Top IP Addresses")
    ip_table.add_column("IP Address")
    ip_table.add_column("Requests")

    for ip, count in analyzer.ip_counter.most_common(5):
        ip_table.add_row(ip, str(count))

    console.print(ip_table)

    slow_table = Table(title="Slowest Endpoints")
    slow_table.add_column("Endpoint")
    slow_table.add_column("Average Response Time")

    averages = []

    for path, times in analyzer.endpoint_times.items():
        avg = sum(times) / len(times)
        averages.append((path, avg))

    averages.sort(key=lambda x: x[1], reverse=True)

    for path, avg in averages[:5]:
        slow_table.add_row(path, f"{avg:.2f} ms")

    console.print(slow_table)


def main():
    parser = argparse.ArgumentParser(
        description="Robust Log Analyzer CLI"
    )

    parser.add_argument(
        "logfile",
        help="Path to log file"
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer()

    try:
        with open(args.logfile, "r", encoding="utf-8") as file:
            for line in file:
                analyzer.total_lines += 1

                entry = parse_line(line)

                if entry:
                    analyzer.process_entry(entry)
                else:
                    analyzer.process_malformed()

        display_report(analyzer)

    except FileNotFoundError:
        console.print(
            "[bold red]Error:[/bold red] Log file not found."
        )


if __name__ == "__main__":
    main()