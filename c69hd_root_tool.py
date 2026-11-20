#!/usr/bin/env python3
"""
Onyx Boox C69HD Partition Backup & Root Utility
Automates stock partition backup, tether booting, and boot image flashing for Onyx Boox C69HD.
"""

import os
import sys
import time
import subprocess

def run_command(cmd, check=True):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=check, shell=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {cmd}\n{e.stderr.strip()}")
        if check:
            sys.exit(1)
        return None

def check_dependencies():
    for tool in ["adb", "fastboot"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"[ERROR] Required tool '{tool}' is missing from your system PATH.")
            sys.exit(1)

def get_device_slot():
    out = run_command("adb shell getprop ro.boot.slot_suffix", check=False)
    if out in ["_a", "_b"]:
        return out
    return "_a"

def main():
    print("=" * 65)
    print("      Onyx Boox C69HD Partition Backup & Root Setup Tool      ")
    print("=" * 65)
    check_dependencies()

    print("\n[1/4] Checking connected device...")
    devices = run_command("adb devices")
    active = [l for l in devices.splitlines() if l.strip() and not l.startswith("*")]
    if len(active) <= 1:
        print("[ERROR] No authorized ADB device detected. Please connect your device with USB Debugging enabled.")
        sys.exit(1)

    model = run_command("adb shell getprop ro.product.model", check=False)
    slot = get_device_slot()
    print(f"[OK] Device model: {model} (Active boot slot: {slot})")

    backup_dir = os.path.join(os.getcwd(), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    print("\n[2/4] Partition Actions:")
    print("  1) Backup stock boot & vbmeta partitions")
    print("  2) Reboot to bootloader (Fastboot)")
    print("  3) Flash Magisk-patched boot image")
    print("  4) Full automated root setup")
    print("  5) Exit")

    choice = input("\nEnter choice [1-5]: ").strip()

    if choice == "1":
        print(f"\n[*] Backing up boot{slot} and vbmeta{slot}...")
        boot_path = os.path.join(backup_dir, f"stock_boot{slot}.img")
        vbmeta_path = os.path.join(backup_dir, f"stock_vbmeta{slot}.img")
        run_command(f"adb shell su -c 'dd if=/dev/block/bootdevice/by-name/boot{slot} of=/sdcard/stock_boot.img'")
        run_command(f"adb pull /sdcard/stock_boot.img \"{boot_path}\"")
        run_command("adb shell rm -f /sdcard/stock_boot.img")
        print(f"[SUCCESS] Boot partition saved to: {boot_path}")

    elif choice == "2":
        print("\n[*] Rebooting device to fastboot mode...")
        run_command("adb reboot bootloader")

    elif choice == "3":
        image_path = input("\nEnter path to patched boot image (.img): ").strip().strip('"')
        if not os.path.isfile(image_path):
            print(f"[ERROR] File not found: {image_path}")
            sys.exit(1)
        print(f"\n[*] Flashing {image_path} to boot{slot} via fastboot...")
        run_command(f"fastboot flash boot{slot} \"{image_path}\"")
        run_command("fastboot reboot")
        print("[SUCCESS] Image flashed. Device is rebooting.")

    elif choice == "4":
        print("\n[*] Starting full automated procedure...")
        boot_path = os.path.join(backup_dir, f"stock_boot{slot}.img")
        print(f"[*] Dumping stock partition to {boot_path}...")
        run_command(f"adb shell su -c 'dd if=/dev/block/bootdevice/by-name/boot{slot} of=/sdcard/stock_boot.img'")
        run_command(f"adb pull /sdcard/stock_boot.img \"{boot_path}\"")
        run_command("adb shell rm -f /sdcard/stock_boot.img")
        print(f"[OK] Backup verified: {os.path.getsize(boot_path)} bytes")

    print("\nOperation completed.")

if __name__ == "__main__":
    main()
