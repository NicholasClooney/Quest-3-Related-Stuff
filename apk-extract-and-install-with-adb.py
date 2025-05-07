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
    print(f"Finding package matching '\u001b[1;36m{partial_name}\u001b[0m' on device {source_device_id}...")

    result = subprocess.run(
        ["adb", "-s", source_device_id, "shell", "pm", "list", "packages"],
        stdout=subprocess.PIPE,
        check=True
    )

    packages = [line.strip().split(":")[-1] for line in result.stdout.decode().splitlines()]
    matches = [pkg for pkg in packages if partial_name.lower() in pkg.lower()]

    if not matches:
        print(f"No packages found matching '{partial_name}' on device {source_device_id}.")
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Multiple matches found for '\u001b[1;36m{partial_name}\u001b[0m':")
        for idx, m in enumerate(matches):
            print(f"  [\u001b[1;33m{idx}\u001b[0m] {m}")

        try:
            choice = input(f"Select a package to use [\u001b[2mdefault: 0\u001b[0m]: ").strip()
            index = int(choice) if choice else 0
            selected = matches[index]
        except (ValueError, IndexError):
            print("\u274c Invalid selection.")
            sys.exit(1)

        print(f"\u2714 Selected package: {selected}")
        return selected

    print(f"\u2714 Selected package: {matches[0]}")
    return matches[0]

def get_matching_cached_package(output_dir, partial_name):
    print(f"Finding cached package matching '\u001b[1;36m{partial_name}\u001b[0m' in '{output_dir}'...")
    base = Path(output_dir)
    if not base.exists():
        return None
    dirs = [d.name for d in base.iterdir() if d.is_dir()]
    matches = [d for d in dirs if partial_name.lower() in d.lower()]

    if not matches:
        return None
    elif len(matches) > 1:
        print(f"Multiple matches found for cached '\u001b[1;36m{partial_name}\u001b[0m':")
        for idx, m in enumerate(matches):
            print(f"  [\u001b[1;33m{idx}\u001b[0m] {m}")
        try:
            choice = input(f"Select a cached package to use [\u001b[2mdefault: 0\u001b[0m]: ").strip()
            index = int(choice) if choice else 0
            selected = matches[index]
        except (ValueError, IndexError):
            print("\u274c Invalid selection.")
            return None
        print(f"\u2714 Selected cached package: {selected}")
        return selected
    print(f"\u2714 Found cached package: {matches[0]}")
    return matches[0]

def get_apk_paths(source_device_id, package_name):
    print(f"Getting APK paths for '{package_name}' on device {source_device_id}...")
    result = subprocess.run(
        ["adb", "-s", source_device_id, "shell", "pm", "path", package_name],
        stdout=subprocess.PIPE,
        check=True
    )
    paths = [line.strip().replace("package:", "") for line in result.stdout.decode().splitlines()]
    print(f"\u2714 Found {len(paths)} APK file(s) to pull")
    return paths

def pull_apks(source_device_id, apk_paths, output_dir, dry_run=False, verbose=False):
    print(f"Pulling APKs to '{output_dir}' from device {source_device_id}...")
    for path in apk_paths:
        filename = os.path.basename(path)
        dest = os.path.join(output_dir, filename)
        run(["adb", "-s", source_device_id, "pull", path, dest], dry_run, verbose)
    print("\u2714 APKs pulled successfully")

def install_apks(target_device_id, apk_files, dry_run=False, verbose=False):
    print(f"Installing APKs on device {target_device_id}...")
    run(["adb", "-s", target_device_id, "install-multiple"] + apk_files, dry_run, verbose)
    print("\u2714 APKs installed successfully")

def prepare_output_path(base_dir, package_name):
    output_base = Path(base_dir)
    output_base.mkdir(parents=True, exist_ok=True)
    app_output_dir = output_base / package_name
    app_output_dir.mkdir(parents=True, exist_ok=True)
    return app_output_dir

def list_cached_apps(output_dir):
    print(f"Listing cached apps in '{output_dir}'...")
    output_path = Path(output_dir)
    if not output_path.exists():
        print("No cached apps found.")
        return
    for item in output_path.iterdir():
        if item.is_dir():
            print(f"  - {item.name}")

def get_cached_apk_files(output_dir, folder_name):
    app_path = Path(output_dir) / folder_name
    if not app_path.exists() or not app_path.is_dir():
        return None
    apk_files = sorted(str(f) for f in app_path.glob("*.apk"))
    return apk_files if apk_files else None

def parse_partial_app_names(raw_input):
    lines = raw_input.strip().splitlines()
    if len(lines) == 1:
        lines = raw_input.strip().split()
    cleaned = [line.strip().lstrip('-').strip() for line in lines if line.strip()]
    print("\u2714 Parsed app list:")
    for app in cleaned:
        print("  -", app)
    if len(cleaned) > 1:
        confirm = input(f"Proceed with installing all {len(cleaned)} apps? [Y/n]: ").strip().lower()
        if confirm not in ('', 'y', 'yes'):
            print("Aborted.")
            sys.exit(0)
    return cleaned

def main():
    parser = argparse.ArgumentParser(description="Extract split APKs from a source device and optionally install them on a target device.")
    parser.add_argument("--source-device-id", required=False)
    parser.add_argument("--target-device-id", required=False)
    parser.add_argument("--output-dir", default=str(Path.home() / "Documents" / "APKs"))
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--partial-app-names", required=False)
    parser.add_argument("--list-cached", action="store_true")
    parser.add_argument("--use-cached", action="store_true")
    args = parser.parse_args()

    if args.list_cached:
        list_cached_apps(args.output_dir)
        return

    if args.install and not args.target_device_id:
        print("--install was specified but --target-device-id is missing.")
        sys.exit(1)

    if not args.partial_app_names:
        print("--partial-app-names is required unless using --list-cached.")
        sys.exit(1)

    partial_app_names = parse_partial_app_names(args.partial_app_names)

    for name in partial_app_names:
        print(f"=== Processing: {name} ===")
        if args.use_cached:
            cached_folder = get_matching_cached_package(args.output_dir, name)
            if cached_folder:
                print(f"✔ Using cached APKs for {cached_folder}")
                cached_apks = get_cached_apk_files(args.output_dir, cached_folder)
                if cached_apks:
                    if args.install:
                        install_apks(args.target_device_id, cached_apks, args.dry_run, args.verbose)
                    else:
                        print(f"Skipping installing {name} (specify `--install`)")
                    continue
                else:
                    print(f"⚠ No APKs found for cached package '{cached_folder}'. Continuing with extraction...")
            else:
                print(f"⚠ No cached package matching '{name}'. Continuing with extraction...")

        if not args.source_device_id:
            print("--source-device-id is required to extract APKs when no cache is found.")
            continue

        package_name = get_matching_package(args.source_device_id, name)
        app_output_dir = prepare_output_path(args.output_dir, package_name)
        apk_paths = get_apk_paths(args.source_device_id, package_name)
        pull_apks(args.source_device_id, apk_paths, str(app_output_dir), args.dry_run, args.verbose)

        if args.install:
            apk_files = [str(app_output_dir / os.path.basename(path)) for path in apk_paths]
            install_apks(args.target_device_id, apk_files, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
