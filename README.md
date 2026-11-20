# Onyx Boox C69HD Root & Recovery Utilities

Technical guide, partition backup workflows, and automated helper scripts for managing firmware and systemless Magisk on the **Onyx Boox C69HD** (`C69_M_STAR`, Qualcomm SM6225 / Bengal).

---

## Hardware & Architecture Overview

- **Device**: Onyx Boox C69HD (`C69_M_STAR`)
- **SoC**: Qualcomm SM6225 / Bengal (`scuba` / PM2250)
- **Android**: Android 11 (Kernel 4.19.157-perf)
- **Partition Scheme**: System-as-Root (SAR), A/B Slots (`boot_a`, `boot_b`, `vbmeta_a`, `vbmeta_b`)
- **Bootloader**: Factory unlocked (`unlocked:yes`)

---

## Included Utilities

- `c69hd_root_tool.py`: Python CLI tool to detect device slot, back up raw boot partitions, and automate flashing.
- `c69hd_restore_stock.py`: Python CLI tool to restore original stock boot partitions for a clean unroot.
- `c69hd_root_tool.bat` / `c69hd_restore_stock.bat`: Windows execution wrappers.

---

## Step-by-Step Procedure

### 1. Prerequisites
- Android SDK Platform-Tools (`adb` and `fastboot`) installed and accessible on PATH.
- USB Debugging enabled on the device.

### 2. Partition Backup
Run the backup tool to extract an untouched copy of your active slot partition:
```sh
python c69hd_root_tool.py
```
Select option 1 to save `stock_boot.img` locally. Always verify backup size (~96 MB) before proceeding.

### 3. Patching the Boot Image
1. Install the official Magisk app on your device.
2. Transfer the backed-up `stock_boot.img` to your device storage:
   ```sh
   adb push backups/stock_boot_a.img /sdcard/Download/
   ```
3. Open Magisk, tap **Install**, choose **Select and Patch a File**, and select `stock_boot_a.img`.
4. Pull the generated image back to your computer:
   ```sh
   adb pull /sdcard/Download/magisk_patched_*.img magisk_patched_boot.img
   ```

### 4. Flashing the Patched Boot Image
Reboot the device into fastboot mode:
```sh
adb reboot bootloader
```
Flash the patched image to the current slot:
```sh
fastboot flash boot_a magisk_patched_boot.img
fastboot reboot
```

### 5. Verification
Verify root status via ADB:
```sh
adb shell su -c "id"
```
Ensure Magisk app lists `Installed` with Superuser access granted.

---

## Restoring Factory Stock (Unroot)

To unroot and revert to stock bootloader execution:
```sh
python c69hd_restore_stock.py
```
Or manually in fastboot mode:
```sh
fastboot flash boot_a backups/stock_boot_a.img
fastboot reboot
```

---

## License
MIT License.
