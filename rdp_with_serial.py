# -*- coding: utf-8 -*-
import json
import subprocess
import sys
import os

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def set_rdp_level(cli_path, rdp_level):
    print("RDP seviyesi", rdp_level, "olarak ayarlaniyor.")
    result = subprocess.run([
        cli_path, "-c", "port=SWD", "-ob", f"RDP={rdp_level}"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    return result.returncode == 0

def flash_hex(cli_path, hex_path):
    print(hex_path, "dosyasi yukleniyor.")
    result = subprocess.run([
        cli_path, "-c", "port=SWD", "-d", hex_path, "-v", "-rst"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("yukleme tamamlandi.")
    else:
        print("yukleme basarisiz.")
        print(result.stdout)
    return result.returncode == 0

def ascii_bytes_from_serial(serial_number):
    return [format(ord(c), '02X') for c in str(serial_number).zfill(3)]

def calculate_checksum(hex_line_without_checksum):
    byte_values = [int(hex_line_without_checksum[i:i+2], 16) for i in range(1, len(hex_line_without_checksum), 2)]
    total = sum(byte_values)
    checksum = ((~total + 1) & 0xFF)
    return format(checksum, '02X')

def update_hex_line_with_serial(line, serial_ascii_hex):
    new_data = line[:25] + ''.join(serial_ascii_hex) + line[31:-2]
    new_checksum = calculate_checksum(new_data)
    return new_data + new_checksum + "\n"

def update_hex_file_with_serial(hex_path, serial_number):
    with open(hex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 6537:
        print("oyle bir satir yok.")
        return False

    serial_ascii_hex = ascii_bytes_from_serial(serial_number)
    lines[6536] = update_hex_line_with_serial(lines[6536].strip(), serial_ascii_hex)

    with open(hex_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"seri numarasi {serial_number} seklinde degistirildi.")
    return True

def main():
    if not os.path.exists("config.json"):
        print("config.json bulunamadi.")
        sys.exit(1)

    config = load_config()
    hex_path = config.get("hex_path")
    rdp_level = config.get("rdp_level", "0xAA")
    cli_path = config.get("stlink_path")

    if not all([hex_path, cli_path]):
        print("json icinde eksik bilgi var.")
        sys.exit(1)

    try:
        serial_input = int(input("0-250 arasinda bir seri numarası giriniz: "))
        if not (0 <= serial_input <= 250):
            raise ValueError
    except:
        print("gecersiz seri numarasi.")
        sys.exit(1)

    if not update_hex_file_with_serial(hex_path, serial_input):
        print("HEX dosyasi guncellenemedi.")
        sys.exit(1)

    success_flash = flash_hex(cli_path, hex_path)
    success_rdp = set_rdp_level(cli_path, rdp_level)

    if success_rdp and success_flash:
        print("islemler basariyla tamamlandi")
    else:
        print("islemler sirasinda hata olustu.")

if __name__ == "__main__":
    main()
