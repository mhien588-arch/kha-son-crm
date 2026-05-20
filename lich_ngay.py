import subprocess
import sys
import os
import json
from datetime import date

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

def c(text, color=""):
    if not HAS_COLOR or not color:
        return text
    return color + text + Style.RESET_ALL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()
TIEN_DO_FILE = os.path.join(BASE_DIR, f"tien_do_{TODAY}.txt")

def _load_kpi():
    try:
        with open(os.path.join(BASE_DIR, "config.json"), encoding="utf-8") as f:
            kpi = json.load(f).get("kpi", {})
        cpl = kpi.get("cpl_max", 100000) // 1000
        return [
            f"Lead moi/tuan  : >= {kpi.get('lead_moi_per_tuan', 20)}",
            f"Xem dat/tuan   : >= {kpi.get('xem_dat_per_tuan', 5)}",
            f"Chot coc/thang : >= {kpi.get('chot_coc_per_thang', 3)}",
            f"CPL (Ads)      : < {cpl}.000d",
        ]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return [
            "Lead moi/tuan  : >= 20",
            "Xem dat/tuan   : >= 5",
            "Chot coc/thang : >= 3",
            "CPL (Ads)      : < 100.000d",
        ]

TASKS = [
    ("sang",  "08:00", "Tracker [3] — Kiem tra khach bi quen > 3 ngay → Goi sale ngay",   "tracker.py"),
    ("sang",  "08:05", "Ads Manager — Kiem tra Chi phi | So lead | CPL (< 100k = dat KPI)", None),
    ("sang",  "08:10", "Tracker [4] — Them lead moi tu Facebook (tu chia sale)",             "tracker.py"),
    ("chieu", "17:00", "Tracker [5] — Cap nhat trang thai khach hang",                       "tracker.py"),
    ("toi",   "18:00", "Bao cao ngay — Xem bang KPI tung sale va toan team",                 "daily_report.py"),
    ("toi",   "18:05", "Chup man hinh bao cao → Gui group Zalo team",                        None),
]

KPI = _load_kpi()


def load_done():
    done = set()
    if os.path.exists(TIEN_DO_FILE):
        with open(TIEN_DO_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    done.add(int(line))
    return done


def save_done(done):
    with open(TIEN_DO_FILE, "w", encoding="utf-8") as f:
        for idx in sorted(done):
            f.write(f"{idx}\n")


def print_checklist(done, filter_buoi=None):
    print()
    print(c("=" * 62, Fore.CYAN if HAS_COLOR else ""))
    print(c(f"  LICH LAM VIEC NGAY — KHA SON GREEN HOME ({TODAY})", Fore.CYAN if HAS_COLOR else ""))
    print(c("=" * 62, Fore.CYAN if HAS_COLOR else ""))

    current_buoi = None
    headers = {"sang": "BUOI SANG — 08:00 (15 phut)", "chieu": "BUOI CHIEU — 17:00 (10 phut)", "toi": "CUOI NGAY — 18:00 (5 phut)"}

    for i, (buoi, gio, mo_ta, script) in enumerate(TASKS, 1):
        if filter_buoi and buoi != filter_buoi:
            continue
        if buoi != current_buoi:
            current_buoi = buoi
            print()
            print(c(f"  {headers[buoi]}", Fore.YELLOW if HAS_COLOR else ""))
            print(c("  " + "-" * 50, Fore.YELLOW if HAS_COLOR else ""))
        tick = "x" if i in done else " "
        color = (Fore.GREEN if HAS_COLOR else "") if i in done else ""
        print(c(f"  [{tick}] {i}. {gio}  {mo_ta}", color))

    print()
    print(c("  KPI THANG:", Fore.MAGENTA if HAS_COLOR else ""))
    for k in KPI:
        print(f"       {k}")
    print()
    print(c("=" * 62, Fore.CYAN if HAS_COLOR else ""))


def launch_script(script_name):
    path = os.path.join(BASE_DIR, script_name)
    print()
    print(c(f"  >> Dang mo {script_name} ...", Fore.GREEN if HAS_COLOR else ""))
    print()
    try:
        subprocess.run([sys.executable, path], check=False)
    except Exception as e:
        print(c(f"  Loi: {e}", Fore.RED if HAS_COLOR else ""))


def mark_done_interactive(done):
    print()
    nhap = input("  Danh so cong viec da xong (vd: 1 2 3) hoac Enter de bo qua: ").strip()
    if nhap:
        for tok in nhap.split():
            if tok.isdigit():
                done.add(int(tok))
        save_done(done)
        print(c("  Da luu tien do.", Fore.GREEN if HAS_COLOR else ""))


def menu_buoi(done):
    print()
    print("  Chon buoi de lam viec:")
    print("    [1] Buoi sang (08:00)  — mo tracker.py")
    print("    [2] Buoi chieu (17:00) — mo tracker.py")
    print("    [3] Cuoi ngay (18:00)  — mo daily_report.py")
    print("    [4] Xem toan bo khach  — mo tracker.py")
    print("    [5] Danh dau cong viec da xong")
    print("    [0] Thoat")
    print()
    chon = input("  Lua chon: ").strip()

    if chon == "1":
        print_checklist(done, filter_buoi="sang")
        launch_script("tracker.py")
    elif chon == "2":
        print_checklist(done, filter_buoi="chieu")
        launch_script("tracker.py")
    elif chon == "3":
        print_checklist(done, filter_buoi="toi")
        launch_script("daily_report.py")
    elif chon == "4":
        launch_script("tracker.py")
    elif chon == "5":
        print_checklist(done)
        mark_done_interactive(done)
    elif chon == "0":
        return False
    else:
        print(c("  Lua chon khong hop le.", Fore.RED if HAS_COLOR else ""))

    return True


def main():
    done = load_done()
    print_checklist(done)

    while True:
        cont = menu_buoi(done)
        if not cont:
            break
        print()
        lai = input("  Tiep tuc? (Enter = co, 0 = thoat): ").strip()
        if lai == "0":
            break
        done = load_done()

    print()
    print(c("  Tam biet! Chuc ban ban ngay hieu qua.", Fore.CYAN if HAS_COLOR else ""))
    print()


if __name__ == "__main__":
    main()
