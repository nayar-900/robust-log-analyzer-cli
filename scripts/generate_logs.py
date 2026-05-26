import json
import random
from datetime import datetime, UTC


METHODS = ["GET", "POST", "PUT", "DELETE"]
PATHS = [
    "/api/users",
    "/api/login",
    "/api/products",
    "/api/orders"
]


def generate_standard_log():
    return (
        f"{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')} "
        f"192.168.1.{random.randint(1,255)} "
        f"{random.choice(METHODS)} "
        f"{random.choice(PATHS)} "
        f"{random.choice([200, 201, 400, 401, 404, 500])} "
        f"{random.randint(10,500)}ms"
    )


def generate_json_log():
    return json.dumps({
        "timestamp": datetime.now(UTC).strftime(
            '%Y-%m-%dT%H:%M:%SZ'
        ),
        "ip": f"10.0.0.{random.randint(1,255)}",
        "method": random.choice(METHODS),
        "path": random.choice(PATHS),
        "status": random.choice([200, 500]),
        "response_time": f"{random.random()}s"
    })


def generate_malformed():
    samples = [
        "Traceback: connection reset",
        "INVALID LOG ENTRY",
        "",
        "partial line"
    ]

    return random.choice(samples)


def main():
    with open("sample_logs/sample.log", "w") as file:
        for _ in range(1000):
            choice = random.random()

            if choice < 0.75:
                line = generate_standard_log()
            elif choice < 0.90:
                line = generate_json_log()
            else:
                line = generate_malformed()

            file.write(line + "\n")


if __name__ == "__main__":
    main()