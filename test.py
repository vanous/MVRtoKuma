import argparse
import sys
from uptime_kuma_api import UptimeKumaApi, MonitorType, UptimeKumaException


def main():
    parser = argparse.ArgumentParser(description="Add a monitor to Uptime Kuma.")
    parser.add_argument("--url", required=True, help="URL of the Uptime Kuma instance")
    parser.add_argument(
        "--timeout", type=int, default=1, help="Timeout for the API call in seconds"
    )
    args = parser.parse_args()

    try:
        api = UptimeKumaApi(args.url, timeout=args.timeout)
        api.login("admin", "aaaaa1A")
        result = api.add_monitor(
            type=MonitorType.HTTP, name="Google", url="https://google.com"
        )
        print("connect result", result)
        sys.exit(0)
    except UptimeKumaException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
