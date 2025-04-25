# Filename: check-apk-installed-on-device.py

import argparse
import subprocess
import sys

def get_matching_package(device_id, partial_name, print_all=False, verbose=False):
    if verbose:
        print("\033[2m$ adb -s", device_id, "shell pm list packages\033[0m")

    print(f"Checking for packages matching '{partial_name}' on device {device_id}...")

    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "pm", "list", "packages"],
        stdout=subprocess.PIPE,
        check=True
    )

    packages = [line.strip().split(":")[-1] for line in result.stdout.decode().splitlines()]
    matches = [pkg for pkg in packages if partial_name.lower() in pkg.lower()]

    if not matches:
        print(f"❌ No packages found matching '{partial_name}' on device {device_id}.")
        sys.exit(1)

    if print_all:
        print(f"✔ Found {len(matches)} match(es):")
        for pkg in matches:
            print("  ", pkg)
    else:
        if len(matches) > 1:
            print(f"⚠ Multiple matches found for '{partial_name}':")
            for pkg in matches:
                print("  ", pkg)
            sys.exit(1)
        print(f"✔ Found package: {matches[0]}")

    return matches

def main():
    parser = argparse.ArgumentParser(description="Check if an app is installed on a target device by partial package name.")
    parser.add_argument("--target-device-id", required=True, help="ADB device ID to check (e.g., Quest 3)")
    parser.add_argument("--partial-app-name", required=True, help="Part of the app's package name")
    parser.add_argument("--print-all", action="store_true", help="Print all matching packages")
    parser.add_argument("--verbose", action="store_true", help="Print adb commands")

    args = parser.parse_args()

    # This function is also used in apk-extract-and-install-with-adb.py
    get_matching_package(args.target_device_id, args.partial_app_name, args.print_all, args.verbose)

if __name__ == "__main__":
    main()
