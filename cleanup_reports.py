"""
Dọn dẹp file báo cáo — Kha Sơn Green Home
Chạy: python cleanup_reports.py
Zip tất cả báo cáo tháng cũ vào archive/, giữ nguyên tháng hiện tại.
"""
import os
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = WHITE = ""
    class Style:
        RESET_ALL = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")


def get_report_month(filename: str):
    """Trả về 'YYYY-MM' từ tên file báo cáo, hoặc None nếu không match."""
    m = re.match(r"bao_cao_(\d{4}-\d{2})-\d{2}\.txt$", filename)
    if m:
        return m.group(1)
    m2 = re.match(r"bao_cao_tuan_W(\d+)_(\d{4})\.txt$", filename)
    if m2:
        week, year = int(m2.group(1)), int(m2.group(2))
        try:
            d = date.fromisocalendar(year, week, 1)
            return d.strftime("%Y-%m")
        except ValueError:
            return None
    return None


def collect_old_files(current_month: str):
    """Thu thập file báo cáo của các tháng cũ hơn tháng hiện tại."""
    by_month = {}
    for f in Path(BASE_DIR).glob("bao_cao*.txt"):
        m = get_report_month(f.name)
        if m and m < current_month:
            by_month.setdefault(m, []).append(f)
    return by_month


def main():
    current_month = date.today().strftime("%Y-%m")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    print(Fore.CYAN + "\n" + "═" * 56)
    print(Fore.CYAN + "  DON DEP BAO CAO — KHA SON GREEN HOME")
    print(Fore.CYAN + "═" * 56)
    print(Fore.WHITE + f"\n  Thang hien tai : {current_month}  (giu nguyen)")
    print(Fore.WHITE + f"  Thu muc archive: {ARCHIVE_DIR}")

    by_month = collect_old_files(current_month)

    if not by_month:
        print(Fore.GREEN + "\n  Khong co file cu nao can don dep. Tat ca da gon gang!")
        input("\n  Nhan Enter de dong...")
        return

    total_files = sum(len(v) for v in by_month.values())
    print(Fore.YELLOW + f"\n  Tim thay {total_files} file bao cao cu ({len(by_month)} thang):")

    for month in sorted(by_month):
        files = by_month[month]
        print(Fore.WHITE + f"\n  Thang {month}:  {len(files)} file")
        for f in sorted(files):
            size_kb = f.stat().st_size // 1024 or 1
            print(Fore.WHITE + f"    - {f.name}  ({size_kb} KB)")

    print(Fore.YELLOW + "\n" + "─" * 56)
    confirm = input(Fore.WHITE + "  Zip va xoa cac file tren? [yes/N]: ").strip().lower()

    if confirm != "yes":
        print(Fore.YELLOW + "\n  Huy. Khong co gi thay doi.")
        input("  Nhan Enter de dong...")
        return

    print()
    zipped_count = 0
    for month in sorted(by_month):
        files = by_month[month]
        yyyy, mm = month.split("-")
        zip_name = os.path.join(ARCHIVE_DIR, f"bao_cao_thang_{mm}_{yyyy}.zip")

        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(files):
                zf.write(f, f.name)

        for f in files:
            f.unlink()

        zipped_count += len(files)
        print(Fore.GREEN + f"  [OK] Zip {len(files)} file thang {month} -> {os.path.basename(zip_name)}")

    print(Fore.CYAN + "\n" + "═" * 56)
    print(Fore.GREEN + f"  Xong! Da luu {zipped_count} file vao {ARCHIVE_DIR}")
    print(Fore.CYAN + "═" * 56)
    input(Fore.WHITE + "\n  Nhan Enter de dong...\n")


if __name__ == "__main__":
    main()
