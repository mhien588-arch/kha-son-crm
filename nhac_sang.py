"""
Nhắc nhở 8:00 sáng — Kha Sơn Green Home
Chạy tự động qua Windows Task Scheduler (T2-T7 lúc 8:00).
Nếu không có khách quá hạn → thoát ngay, không làm phiền.
"""
import sys
from datetime import datetime, date

try:
    import pandas as pd
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Cai thu vien: pip install pandas colorama")
    sys.exit(1)

from sheets_connector import load_data, load_config, backup_to_csv

ACTIVE_STATUS = ["Mới", "Đang chăm sóc"]


def days_since(date_str):
    if not str(date_str).strip():
        return 9999
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            d = datetime.strptime(str(date_str).strip(), fmt).date()
            return (date.today() - d).days
        except ValueError:
            continue
    return 9999


def get_overdue(df, remind_days):
    """Trả về dict {sale: [(days, row), ...]} — ACTIVE_STATUS, còn nhu cầu, >= remind_days."""
    overdue = {}
    for _, row in df.iterrows():
        if row["Trạng thái"] not in ACTIVE_STATUS:
            continue
        if row.get("Nhu cầu", "") == "Không còn nhu cầu":
            continue
        d = days_since(row["Ngày tương tác cuối"])
        if d >= remind_days:
            sale = str(row["Sale chăm sóc"]).strip() or "Chua phan cong"
            overdue.setdefault(sale, []).append((d, row))
    for sale in overdue:
        overdue[sale].sort(key=lambda x: x[0], reverse=True)
    return overdue


def get_nurture(df, nurture_days):
    """Trả về dict {sale: [(days, row), ...]} — Không còn nhu cầu >= nurture_days."""
    nurture = {}
    for _, row in df.iterrows():
        if row.get("Nhu cầu", "") != "Không còn nhu cầu":
            continue
        if row["Trạng thái"] == "Chốt cọc":
            continue
        d = days_since(row["Ngày tương tác cuối"])
        if d >= nurture_days:
            sale = str(row["Sale chăm sóc"]).strip() or "Chua phan cong"
            nurture.setdefault(sale, []).append((d, row))
    for sale in nurture:
        nurture[sale].sort(key=lambda x: x[0], reverse=True)
    return nurture


def print_banner(total, remind_days):
    W = 56
    today_str = date.today().strftime("%d/%m/%Y")
    print(Fore.RED + "\n" + "╔" + "═" * (W - 2) + "╗")
    print(Fore.RED + f"║{'NHAC NHO SANG — ' + today_str:^{W-2}}║")
    print(Fore.RED + "╠" + "═" * (W - 2) + "╣")
    msg = f"{total} KHACH CHUA LIEN HE QUA {remind_days} NGAY"
    print(Fore.RED + f"║{msg:^{W-2}}║")
    print(Fore.RED + "╚" + "═" * (W - 2) + "╝")


def main():
    print(Fore.YELLOW + "Dang kiem tra du lieu tu Google Sheets...")
    cfg = load_config()
    remind_days = cfg.get("remind_days", 3)
    nurture_days = cfg.get("nurture_days", 14)

    try:
        df = load_data()
        # Tự động sao lưu dữ liệu CRM thành file CSV cục bộ
        backup_to_csv()
    except Exception as e:
        print(Fore.RED + f"Loi ket noi Google Sheets: {e}")
        input("Nhan Enter de dong...")
        sys.exit(1)

    overdue = get_overdue(df, remind_days)
    nurture = get_nurture(df, nurture_days)

    if not overdue and not nurture:
        print(Fore.GREEN + f"\n  Khong co canh bao nao hom nay. Chuc mung!")
        sys.exit(0)

    W = 56

    if overdue:
        total = sum(len(v) for v in overdue.values())
        print_banner(total, remind_days)
        for sale, items in sorted(overdue.items()):
            print(Fore.YELLOW + f"\n  [{sale}] — {len(items)} khach can goi ngay:")
            print(Fore.WHITE + "  " + "─" * (W - 2))
            for d, row in items:
                ten = str(row["Tên khách"])[:18]
                sdt = str(row["Số ĐT"])
                days_label = f"{d} ngay" if d < 9999 else "chua co ngay"
                urgency = Fore.RED if d >= 5 else Fore.YELLOW
                print(urgency + f"     -> {ten:<18} ({sdt})  —  {days_label}")
        print(Fore.RED + "\n" + "═" * W)
        print(Fore.WHITE + "  Vui long goi cho cac khach hang tren NGAY HOM NAY!")
        print(Fore.RED + "═" * W)

    if nurture:
        total_n = sum(len(v) for v in nurture.values())
        print(Fore.YELLOW + f"\n  {'='*W}")
        print(Fore.YELLOW + f"  GIU TUONG TAC — {total_n} khach 'Khong con nhu cau' > {nurture_days} ngay")
        print(Fore.YELLOW + f"  {'='*W}")
        for sale, items in sorted(nurture.items()):
            print(Fore.YELLOW + f"\n  [{sale}] — {len(items)} khach nen nhan hoi tham:")
            print(Fore.WHITE + "  " + "─" * (W - 2))
            for d, row in items:
                ten = str(row["Tên khách"])[:18]
                sdt = str(row["Số ĐT"])
                days_label = f"{d} ngay" if d < 9999 else "chua co ngay"
                print(Fore.YELLOW + f"     -> {ten:<18} ({sdt})  —  {days_label}")
        print(Fore.YELLOW + "  " + "═" * W)

    input(Fore.WHITE + "\n  Nhan Enter de dong cua so nay...\n")


if __name__ == "__main__":
    main()
