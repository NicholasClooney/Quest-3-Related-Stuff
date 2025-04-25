# Filename: apk-extract-and-install-with-adb.py

import argparse
import os
import subprocess
import sys
from pathlib import Path

def run(cmd, dry_run=False, verbose=False):
    if verbose:
        print("\033[2m$", " ".join(cmd), "\033[0m")  # dim text for better compatibility
    if not dry_run:
        subprocess.run(cmd, check=True)

def get_matching_package(source_device_id, partial_name):
    print(f"Finding package matching '{partial_name}' on device {source_device_id}...")

    result = subprocess.run(
        [
            "adb", "-s", source_device_id, "shell", "pm", "list", "packages"
        ],
        stdout=subprocess.PIPE,
        check=True
    )

    packages = [line.strip().split(":")[-1] for line in result.stdout.decode().splitlines()]
    matches = [pkg for pkg in packages if partial_name.lower() in pkg.lower()]

    if not matches:
        print(f"No packages found matching '{partial_name}' on device {source_device_id}.")
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Multiple matches found for '{partial_name}':")
        for m in matches:
            print("  ", m)
        sys.exit(1)

    print(f"✔ Found package: {matches[0]}")

    return matches[0]

def get_apk_paths(source_device_id, package_name):
    print(f"Getting APK paths for '{package_name}' on device {source_device_id}...")

    result = subprocess.run(
        ["adb", "-s", source_device_id, "shell", "pm", "path", package_name],
        stdout=subprocess.PIPE,
        check=True
    )

    paths = [line.strip().replace("package:", "") for line in result.stdout.decode().splitlines()]

    print(f"✔ Found {len(paths)} APK file(s) to pull")

    return paths

def pull_apks(source_device_id, apk_paths, output_dir, dry_run=False, verbose=False):
    print(f"Pulling APKs to '{output_dir}' from device {source_device_id}...")

    for path in apk_paths:
        filename = os.path.basename(path)
        dest = os.path.join(output_dir, filename)
        run(["adb", "-s", source_device_id, "pull", path, dest], dry_run, verbose)

    print("✔ APKs pulled successfully")

def install_apks(target_device_id, apk_files, dry_run=False, verbose=False):
    print(f"Installing APKs on device {target_device_id}...")

    run(["adb", "-s", target_device_id, "install-multiple"] + apk_files, dry_run, verbose)

    print("✔ APKs installed successfully")

def prepare_output_path(base_dir, package_name):
    print(f"Preparing output directory for '{package_name}'...")

    output_base = Path(base_dir)
    output_base.mkdir(parents=True, exist_ok=True)
    app_output_dir = output_base / package_name
    app_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"✔ Output directory ready at: {app_output_dir}")

    return app_output_dir

def main():
    parser = argparse.ArgumentParser(description="Extract split APKs from a source device and optionally install them on a target device.")
    parser.add_argument("--source-device-id", required=True, help="ADB device ID to pull APKs from (e.g., emulator)")
    parser.add_argument("--target-device-id", required=False, help="ADB device ID to install APKs to (e.g., Quest 3)")
    parser.add_argument("--output-dir", default=str(Path.home() / "Documents" / "APKs"), help="Base directory to save APKs (app folder will be created inside). Defaults to ~/Documents/APKs")
    parser.add_argument("--install", action="store_true", help="Install APKs on the target device after pulling")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them")
    parser.add_argument("--verbose", action="store_true", help="Print commands as they run")
    parser.add_argument("--partial-app-name", required=True, help="Part of the app's package name")

    args = parser.parse_args()

    if args.install and not args.target_device_id:
        print("--install was specified but --target-device-id is missing.")
        sys.exit(1)

    partial_app_name = args.partial_app_name
    package_name = get_matching_package(args.source_device_id, partial_app_name)

    app_output_dir = prepare_output_path(args.output_dir, package_name)
    apk_paths = get_apk_paths(args.source_device_id, package_name)

    pull_apks(args.source_device_id, apk_paths, str(app_output_dir), args.dry_run, args.verbose)

    if args.install:
        apk_files = [str(app_output_dir / os.path.basename(path)) for path in apk_paths]
        install_apks(args.target_device_id, apk_files, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
