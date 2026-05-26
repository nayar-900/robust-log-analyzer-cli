import argparse

from analyzer.parser import parse_line
from analyzer.analyzer import LogAnalyzer


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

    with open(args.logfile, "r", encoding="utf-8") as file:
        for line in file:
            analyzer.total_lines += 1

            entry = parse_line(line)

            if entry:
                analyzer.process_entry(entry)
            else:
                analyzer.process_malformed()

    print(analyzer.generate_report())


if __name__ == "__main__":
    main()