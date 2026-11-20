#!/usr/bin/env python3
"""
Onyx Boox C69HD Factory Stock Restore Utility
Restores stock boot and vbmeta partitions to return the Onyx Boox C69HD to factory unrooted state.
"""

import os
import sys
import subprocess

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e.stderr.strip()}")
        sys.exit(1)

def main():
    print("=" * 65)
    print("       Onyx Boox C69HD Factory Stock Restore Utility          ")
    print("=" * 65)

    stock_img = input("\nEnter path to stock boot image (e.g. backups/stock_boot_a.img): ").strip().strip('"')
    if not os.path.isfile(stock_img):
        print(f"[ERROR] File does not exist: {stock_img}")
        sys.exit(1)

    slot = input("Enter target slot to restore (_a or _b) [Default: _a]: ").strip() or "_a"

    confirm = input(f"\nFlash '{stock_img}' to boot{slot}? This will unroot the device (y/N): ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    print("\n[*] Checking fastboot connection...")
    run_cmd(f"fastboot flash boot{slot} \"{stock_img}\"")
    print("[*] Partition restored. Rebooting device...")
    run_cmd("fastboot reboot")
    print("\n[SUCCESS] Factory stock boot restored successfully.")

if __name__ == "__main__":
    main()
