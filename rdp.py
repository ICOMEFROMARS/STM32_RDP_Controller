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

    success_flash = flash_hex(cli_path, hex_path)
    success_rdp = set_rdp_level(cli_path, rdp_level)

    if success_rdp and success_flash:
        print("islemler basariyla tamamlandi")
    else:
        print("islemler sirasinda hata olustu.")

if __name__ == "__main__":
    main()
