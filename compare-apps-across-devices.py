# Filename: compare-apps-across-devices.py

import argparse
import subprocess
import sys

# Global ignore list for known system or irrelevant apps on source
IGNORED_SOURCE_PACKAGES = {
    "com.google.android.contactkeys",
    "com.google.ar.core"
}

def get_user_installed_packages(device_id, verbose=False):
    if verbose:
        print("\033[2m$ adb -s", device_id, "shell pm list packages -3\033[0m")

    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "pm", "list", "packages", "-3"],
        stdout=subprocess.PIPE,
        check=True
    )
    packages = [line.strip().split(":")[-1] for line in result.stdout.decode().splitlines()]
    filtered = [pkg for pkg in packages if pkg not in IGNORED_SOURCE_PACKAGES]
    return set(filtered)

def print_summary(source_pkgs, target_pkgs, show_extra_apps_on_target=False):
    only_on_source = sorted(source_pkgs - target_pkgs)
    only_on_target = sorted(target_pkgs - source_pkgs)

    if only_on_source:
        print("\nInstalled only on source:")
        for pkg in only_on_source:
            print("  -", pkg)
    else:
        print("\n✅ All source apps are present on the target device.")

    if only_on_target:
        if show_extra_apps_on_target:
            print("\nInstalled only on target:")
            for pkg in only_on_target:
                print("  -", pkg)
        else:
            print(f"\nℹ️  {len(only_on_target)} user-installed apps found only on target (use --show-extra-apps-on-target to list them)")

def main():
    parser = argparse.ArgumentParser(description="Compare user-installed apps between two Android devices and optionally show extras on target.")
    parser.add_argument("--source-device-id", required=True, help="ADB device ID to use as source")
    parser.add_argument("--target-device-id", required=True, help="ADB device ID to use as target")
    parser.add_argument("--verbose", action="store_true", help="Show adb commands being executed")
    parser.add_argument("--show-extra-apps-on-target", action="store_true", help="Show apps only installed on the target device")

    args = parser.parse_args()

    print(f"Getting user-installed apps from source device {args.source_device_id}...")
    source_pkgs = get_user_installed_packages(args.source_device_id, args.verbose)
    print(f"✔ Found {len(source_pkgs)} apps on source.")

    print(f"\nGetting user-installed apps from target device {args.target_device_id}...")
    target_pkgs = get_user_installed_packages(args.target_device_id, args.verbose)
    print(f"✔ Found {len(target_pkgs)} apps on target.")

    print_summary(source_pkgs, target_pkgs, args.show_extra_apps_on_target)

if __name__ == "__main__":
    main()
