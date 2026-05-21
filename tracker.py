"""
Tracker quản lý leads — Kha Sơn Green Home
Chạy: python tracker.py
Yêu cầu: pip install pandas colorama gspread google-auth
"""
import re
import sys
import random
from datetime import datetime, date

try:
    import pandas as pd
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Cài thư viện: pip install pandas colorama")
    sys.exit(1)

from sheets_connector import (load_data, append_row, update_row, COLUMNS, load_config, save_config,
                               highlight_new_row, unhighlight_row,
                               append_staging_row, load_staging_data, transfer_checked_leads,
                               delete_crm_row, load_telesale_data, transfer_telesale_checked)

# ── CẤU HÌNH — tải từ config.json (chỉnh qua menu [7], không sửa tay) ─────
_DEFAULT_TEAM = ["Hiển", "Đức", "Sơn", "Tuấn Anh"]
_cfg = load_config()
SALE_TEAM = _cfg.get("sale_team", _DEFAULT_TEAM)
REMIND_DAYS = _cfg.get("remind_days", 3)
NURTURE_DAYS = _cfg.get("nurture_days", 14)
# ───────────────────────────────────────────────────────────────────────────

TRANG_THAI = ["Mới", "Đang chăm sóc", "Hẹn xem đất", "Từ chối", "Chốt cọc"]
NHU_CAU_OPTIONS = ["Còn nhu cầu", "Không còn nhu cầu"]
ACTIVE_STATUS = ["Mới", "Đang chăm sóc"]
DONE_STATUS = ["Từ chối", "Chốt cọc"]


def reload_team():
    global SALE_TEAM
    SALE_TEAM = load_config().get("sale_team", _DEFAULT_TEAM)


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


def _next_sale(df):
    mode = load_config().get("assign_mode", "roundrobin")
    if mode == "random":
        return random.choice(SALE_TEAM)
    if df.empty:
        return SALE_TEAM[0]
    last = df["Sale chăm sóc"].iloc[-1]
    idx = SALE_TEAM.index(last) if last in SALE_TEAM else -1
    return SALE_TEAM[(idx + 1) % len(SALE_TEAM)]


def _validate_sdt(sdt: str) -> bool:
    return bool(re.match(r'^0\d{9}$', sdt))


# ── CHỨC NĂNG CHÍNH ────────────────────────────────────────────────────────

def them_lead_moi(df):
    print(Fore.CYAN + "\n─── THÊM LEAD MỚI ───────────────────────────────")
    ten = input("  Tên khách: ").strip()
    if not ten:
        print(Fore.YELLOW + "  Bỏ qua — tên không được để trống.")
        return df

    # 1D — Validate SĐT chuẩn Việt Nam
    while True:
        sdt = input("  Số ĐT (để trống nếu chưa có): ").strip()
        if sdt == "":
            break
        if _validate_sdt(sdt):
            break
        print(Fore.RED + "  ✗ SĐT không hợp lệ — phải bắt đầu bằng 0, đủ 10 chữ số (VD: 0987123456)")

    # 1A — Kiểm tra trùng SĐT (cả CRM lẫn staging)
    if sdt:
        dup_crm = df[df["Số ĐT"].str.strip() == sdt] if not df.empty else pd.DataFrame()
        staging_df, _ = load_staging_data()
        dup_stg = staging_df[staging_df["Số ĐT"].str.strip() == sdt] if not staging_df.empty else pd.DataFrame()
        all_dups = pd.concat([dup_crm, dup_stg], ignore_index=True)
        if not all_dups.empty:
            row = all_dups.iloc[0]
            src = "SỐ MỚI KS" if dup_crm.empty else "hệ thống CRM"
            print(Fore.YELLOW + f"\n  ⚠  TRÙNG SĐT! Đã có trong {src}:")
            print(Fore.WHITE + f"     Tên       : {row['Tên khách']}")
            print(Fore.WHITE + f"     Sale      : {row['Sale chăm sóc']}")
            print(Fore.WHITE + f"     Trạng thái: {row['Trạng thái']}")
            confirm = input(Fore.YELLOW + "  Vẫn thêm? (y/N): ").strip().lower()
            if confirm != "y":
                print(Fore.YELLOW + "  Đã hủy.")
                return df

    nguon = input("  Nguồn (FB Ads / Zalo / Giới thiệu / Khác): ").strip() or "Khác"
    ghi_chu = input("  Ghi chú (Enter để bỏ qua): ").strip()
    today = date.today().strftime("%Y-%m-%d")

    print(Fore.CYAN + "\n  Phân công sale:")
    print(Fore.WHITE + "  [0] Tự động (round-robin / random)")
    for i, s in enumerate(SALE_TEAM, 1):
        print(Fore.WHITE + f"  [{i}] {s}")
    pick = input("  Chọn (Enter = tự động): ").strip()
    if pick.isdigit() and 1 <= int(pick) <= len(SALE_TEAM):
        sale = SALE_TEAM[int(pick) - 1]
        print(Fore.YELLOW + f"  → Chỉ định: {sale}")
    else:
        sale = _next_sale(df)
        print(Fore.YELLOW + f"  → Tự động: {sale}")
    new_row = {
        "Tên khách": ten,
        "Số ĐT": sdt,
        "Nguồn": nguon,
        "Sale chăm sóc": sale,
        "Trạng thái": "Mới",
        "Ghi chú": ghi_chu,
        "Ngày tiếp cận": today,
        "Ngày tương tác cuối": today,
    }
    print(Fore.YELLOW + "  Đang lưu vào SỐ MỚI KS...")
    append_staging_row(new_row)
    print(Fore.GREEN + f"\n  ✔ Đã thêm vào SỐ MỚI KS: {ten} ({sdt})")
    print(Fore.GREEN + f"  → Giao cho: {Fore.YELLOW}{sale}")
    print(Fore.WHITE + "  Vào Google Sheets tab 'SỐ MỚI KS', tích ✓ sau khi liên hệ lần đầu.")
    return df


def _show_new_leads_today(df):
    today = date.today().strftime("%Y-%m-%d")
    new_today = df[(df["Trạng thái"] == "Mới") & (df["Ngày tiếp cận"] == today)]
    if new_today.empty:
        return
    print(Fore.YELLOW + "\n  📬 LEAD MỚI HÔM NAY (chưa liên hệ):")
    print(Fore.YELLOW + "  " + "─" * 44)
    for _, row in new_today.iterrows():
        print(Fore.YELLOW + f"  → {row['Sale chăm sóc']}: {row['Tên khách']} ({row['Số ĐT']})")
    print(Fore.YELLOW + "  " + "─" * 44 + "\n")


def _show_nhu_cau_banner(df):
    if df.empty or "Nhu cầu" not in df.columns:
        return
    n = len(df[df["Nhu cầu"] == "Không còn nhu cầu"])
    if n > 0:
        print(Fore.RED + f"  *** {n} KHÁCH KHÔNG CÒN NHU CẦU — CẦN XEM LẠI ***")


def _show_staging_banner():
    staging_df, _ = load_staging_data()
    n = len(staging_df)
    if n == 0:
        return
    print(Fore.YELLOW + f"  📥 SỐ MỚI KS: {n} khách chờ xử lý — tích ✓ trong Sheets rồi nhấn [9]")


def _show_telesale_banner():
    tele_df, _ = load_telesale_data()
    n = len(tele_df)
    if n == 0:
        return
    print(Fore.MAGENTA + f"  📞 DATA TELESALE: {n} số chờ gọi — tích ✓ trong Sheets rồi nhấn [T]")


def xu_ly_so_moi(df):
    print(Fore.YELLOW + "  Đang kiểm tra SỐ MỚI KS...")
    names = transfer_checked_leads()
    if not names:
        print(Fore.YELLOW + "  Chưa có khách nào tích ✓.")
        _show_staging_banner()
        return df
    print(Fore.GREEN + f"  ✔ Đã chuyển {len(names)} khách vào CRM:")
    for n in names:
        print(Fore.GREEN + f"    → {n}")
    df = load_data()
    _show_staging_banner()
    return df


def xu_ly_data_telesale(df):
    print(Fore.MAGENTA + "  Đang kiểm tra DATA TELESALE...")
    names = transfer_telesale_checked()
    if not names:
        print(Fore.YELLOW + "  Chưa có số nào tích ✓.")
        _show_telesale_banner()
        return df
    print(Fore.GREEN + f"  ✔ Đã chuyển {len(names)} khách từ DATA TELESALE vào CRM:")
    for n in names:
        print(Fore.GREEN + f"    → {n}")
    df = load_data()
    _show_telesale_banner()
    return df


def tim_kiem_sdt(df):
    print(Fore.CYAN + "\n─── TÌM KIẾM THEO SĐT ──────────────────────────")
    sdt = input("  Nhập SĐT (hoặc một phần): ").strip()
    if not sdt:
        return df
    results = df[df["Số ĐT"].str.contains(sdt, na=False)]
    if results.empty:
        print(Fore.YELLOW + f"  Không tìm thấy khách nào với SĐT chứa '{sdt}'")
        return df
    print(Fore.CYAN + f"\n  Tìm thấy {len(results)} khách:")
    print("  " + "─" * 70)
    for i, (_, row) in enumerate(results.iterrows(), 1):
        nc = row.get("Nhu cầu", "") if "Nhu cầu" in row.index else ""
        nc_str = f" | Nhu cầu: {nc}" if nc else ""
        print(Fore.WHITE + f"  [{i}] {row['Tên khách']:<18} {row['Số ĐT']:<13} "
              f"{row['Trạng thái']:<16} Sale: {row['Sale chăm sóc']}{nc_str}")
        if row["Ghi chú"]:
            print(f"       Ghi chú: {row['Ghi chú']}")
        print(f"       Tương tác cuối: {row['Ngày tương tác cuối']}")
    print()
    if len(results) == 1:
        upd = input("  Cập nhật trạng thái khách này? (y/N): ").strip().lower()
        if upd == "y":
            df = cap_nhat_trang_thai(df, prefill_idx=results.index[0])
    return df


def kiem_tra_quen_khach(df):
    print(Fore.RED + f"\n{'═'*60}")
    print(Fore.RED + f"  ⚠  CẢNH BÁO — KHÁCH BỊ BỎ QUÊN > {REMIND_DAYS} NGÀY")
    print(Fore.RED + f"{'═'*60}")

    overdue = {}
    for _, row in df.iterrows():
        if row["Trạng thái"] not in ACTIVE_STATUS:
            continue
        if row.get("Nhu cầu", "") == "Không còn nhu cầu":
            continue
        d = days_since(row["Ngày tương tác cuối"])
        if d >= REMIND_DAYS:
            sale = row["Sale chăm sóc"] or "Chưa phân công"
            overdue.setdefault(sale, []).append((d, row))

    if not overdue:
        print(Fore.GREEN + "\n  Tốt lắm! Không có khách nào bị bỏ quên.\n")
        return

    for sale, items in sorted(overdue.items()):
        items.sort(key=lambda x: x[0], reverse=True)
        print(Fore.RED + f"\n  🔴 [{sale}]: {len(items)} khách cần gọi lại NGAY!")
        for d, row in items:
            print(f"     → {row['Tên khách']:<18} ({row['Số ĐT']}) — {d} ngày chưa liên hệ")
    print()


def kiem_tra_giu_tuong_tac(df):
    print(Fore.YELLOW + f"\n{'═'*60}")
    print(Fore.YELLOW + f"  💛  GIỮ TƯƠNG TÁC — NHẮN HỎI THĂM (> {NURTURE_DAYS} NGÀY)")
    print(Fore.YELLOW + f"{'═'*60}")

    nurture = {}
    for _, row in df.iterrows():
        if row.get("Nhu cầu", "") != "Không còn nhu cầu":
            continue
        if row["Trạng thái"] == "Chốt cọc":
            continue
        d = days_since(row["Ngày tương tác cuối"])
        if d >= NURTURE_DAYS:
            sale = row["Sale chăm sóc"] or "Chưa phân công"
            nurture.setdefault(sale, []).append((d, row))

    if not nurture:
        print(Fore.GREEN + "\n  Không có khách tiềm năng nào cần giữ tương tác.\n")
        return

    for sale, items in sorted(nurture.items()):
        items.sort(key=lambda x: x[0], reverse=True)
        print(Fore.YELLOW + f"\n  💛 [{sale}]: {len(items)} khách nên nhắn hỏi thăm:")
        for d, row in items:
            print(f"     → {row['Tên khách']:<18} ({row['Số ĐT']}) — {d} ngày")
    print()


def view_all(df):
    if df.empty:
        print(Fore.YELLOW + "\n  Chưa có khách hàng nào.")
        return
    print(Fore.CYAN + f"\n{'═'*80}")
    print(Fore.CYAN + f"  TẤT CẢ KHÁCH HÀNG ({len(df)} người)")
    print(Fore.CYAN + f"{'═'*80}")
    _print_table(df)


def view_by_sale(df):
    if df.empty:
        print(Fore.YELLOW + "\n  Chưa có dữ liệu.")
        return
    print("\n  Sale trong team:")
    for i, s in enumerate(SALE_TEAM, 1):
        count = len(df[df["Sale chăm sóc"] == s])
        print(f"  [{i}] {s} ({count} khách)")
    name = input("\n  Nhập tên sale: ").strip()
    filtered = df[df["Sale chăm sóc"].str.contains(name, case=False, na=False)]
    if filtered.empty:
        print(Fore.YELLOW + f"  Không tìm thấy sale '{name}'.")
        return
    print(Fore.CYAN + f"\n{'═'*80}")
    print(Fore.CYAN + f"  KHÁCH CỦA: {name.upper()} ({len(filtered)} người)")
    print(Fore.CYAN + f"{'═'*80}")
    _print_table(filtered)


def cap_nhat_trang_thai(df, prefill_idx=None):
    print(Fore.CYAN + "\n─── CẬP NHẬT TRẠNG THÁI ─────────────────────────")

    if prefill_idx is not None:
        pandas_idx = prefill_idx
    else:
        keyword = input("  Tên hoặc SĐT khách: ").strip()
        mask = (df["Tên khách"].str.contains(keyword, case=False, na=False) |
                df["Số ĐT"].str.contains(keyword, na=False))
        matches = df[mask]
        if matches.empty:
            print(Fore.YELLOW + "  Không tìm thấy khách hàng.")
            return df
        for i, (_, row) in enumerate(matches.iterrows(), 1):
            print(f"  [{i}] {row['Tên khách']} — {row['Số ĐT']} — {row['Trạng thái']}")
        try:
            choice = int(input("  Chọn số: ")) - 1
            pandas_idx = matches.index[choice]
        except (ValueError, IndexError):
            print(Fore.RED + "  Lựa chọn không hợp lệ.")
            return df

    row = df.loc[pandas_idx]
    print(f"\n  Khách: {Fore.WHITE}{row['Tên khách']} ({row['Số ĐT']})")
    print(f"  Trạng thái hiện tại: {Fore.YELLOW}{row['Trạng thái']}")
    old_tt = row["Trạng thái"]

    print(Fore.WHITE + "\n  Trạng thái mới:")
    for i, tt in enumerate(TRANG_THAI, 1):
        print(f"  [{i}] {tt}")
    try:
        new_tt = TRANG_THAI[int(input("  Chọn: ")) - 1]
    except (ValueError, IndexError):
        print(Fore.RED + "  Không hợp lệ.")
        return df

    ghi_chu = input("  Ghi chú thêm (Enter bỏ qua): ").strip()

    # Cập nhật nhu cầu khách hàng
    cur_nc = df.at[pandas_idx, "Nhu cầu"] if "Nhu cầu" in df.columns else ""
    nc_display = f" (hiện: {cur_nc})" if cur_nc else ""
    print(Fore.WHITE + f"\n  Nhu cầu{nc_display}:")
    print("  [1] Còn nhu cầu   [2] Không còn nhu cầu   [Enter] Giữ nguyên")
    nc_choice = input("  Chọn: ").strip()
    new_nc = NHU_CAU_OPTIONS[int(nc_choice) - 1] if nc_choice in ("1", "2") else None

    today = date.today().strftime("%Y-%m-%d")
    df.at[pandas_idx, "Trạng thái"] = new_tt
    df.at[pandas_idx, "Ngày tương tác cuối"] = today
    if ghi_chu:
        df.at[pandas_idx, "Ghi chú"] = ghi_chu
    if new_nc is not None and "Nhu cầu" in df.columns:
        df.at[pandas_idx, "Nhu cầu"] = new_nc

    row_idx = pandas_idx  # pandas_idx là sheet row thực tế (load_data dùng sheet-row index)
    print(Fore.YELLOW + "  Đang lưu lên Google Sheets...")
    update_row(row_idx, df.loc[pandas_idx].to_dict())
    if old_tt == "Mới":
        unhighlight_row(row_idx)
    nc_note = f" | Nhu cầu: {new_nc}" if new_nc else ""
    print(Fore.GREEN + f"  ✔ Cập nhật: {df.at[pandas_idx, 'Tên khách']} → {new_tt}{nc_note}")
    return df


def chuyen_leads_giua_sale(df):
    """Menu [7][e] — Chọn leads của 1 sale, chuyển sang SỐ MỚI KS với sale mới."""
    print(Fore.CYAN + "\n─── CHUYỂN LEADS SANG SALE KHÁC ──────────────────")

    # Bước 1: Chọn sale nguồn
    print(Fore.WHITE + "\n  Sale NGUỒN (đang giữ lead):")
    for i, s in enumerate(SALE_TEAM, 1):
        count = len(df[df["Sale chăm sóc"] == s])
        print(f"  [{i}] {s}  ({count} leads)")
    pick_src = input("  Chọn sale nguồn: ").strip()
    if not pick_src.isdigit() or not (1 <= int(pick_src) <= len(SALE_TEAM)):
        print(Fore.RED + "  Lựa chọn không hợp lệ.")
        return df
    nguon_sale = SALE_TEAM[int(pick_src) - 1]

    # Bước 2: Hiện leads của sale nguồn
    sale_df = df[df["Sale chăm sóc"] == nguon_sale].copy()
    if sale_df.empty:
        print(Fore.YELLOW + f"  {nguon_sale} không có lead nào.")
        return df
    print(Fore.CYAN + f"\n  Leads của {nguon_sale} ({len(sale_df)} người):")
    print(f"  {'#':>3}  {'Tên khách':<20} {'Số ĐT':<13} {'Trạng thái':<18} {'Tương tác cuối'}")
    print("  " + "─" * 72)
    for seq, (pidx, row) in enumerate(sale_df.iterrows(), 1):
        d = days_since(row.get("Ngày tương tác cuối", ""))
        days_str = f"{d}n" if d is not None else "—"
        print(f"  {seq:>3}  {row['Tên khách']:<20} {row['Số ĐT']:<13} {row['Trạng thái']:<18} {days_str}")

    # Bước 3: Chọn leads cần chuyển
    print(Fore.WHITE + "\n  Chọn số thứ tự cần chuyển (cách nhau bằng dấu cách, hoặc 'all'):")
    sel_input = input("  Chọn: ").strip().lower()
    if sel_input == "all":
        selected_indices = list(sale_df.index)
    else:
        selected_indices = []
        for tok in sel_input.split():
            if tok.isdigit():
                seq = int(tok)
                if 1 <= seq <= len(sale_df):
                    selected_indices.append(sale_df.index[seq - 1])
    if not selected_indices:
        print(Fore.YELLOW + "  Không có lead nào được chọn.")
        return df

    # Bước 4: Chọn sale đích
    dich_options = [s for s in SALE_TEAM if s != nguon_sale]
    print(Fore.WHITE + f"\n  Sale ĐÍCH (nhận {len(selected_indices)} lead):")
    for i, s in enumerate(dich_options, 1):
        print(f"  [{i}] {s}")
    pick_dst = input("  Chọn sale đích: ").strip()
    if not pick_dst.isdigit() or not (1 <= int(pick_dst) <= len(dich_options)):
        print(Fore.RED + "  Lựa chọn không hợp lệ.")
        return df
    dich_sale = dich_options[int(pick_dst) - 1]

    # Bước 5: Xác nhận
    print(Fore.YELLOW + f"\n  Sẽ chuyển {len(selected_indices)} lead: {nguon_sale} → {dich_sale}")
    print(Fore.WHITE + "  Lead vào SỐ MỚI KS — sale mới tích ✓ sau khi liên hệ lần đầu.")
    confirm = input(Fore.YELLOW + "  Xác nhận? (yes/N): ").strip().lower()
    if confirm != "yes":
        print(Fore.YELLOW + "  Đã hủy.")
        return df

    # Bước 6: Thực thi — append staging trước, xóa CRM sau (reverse tránh index shift)
    print(Fore.YELLOW + "  Đang chuyển...")
    today_str = date.today().strftime("%d/%m")
    for pidx in selected_indices:
        row_dict = df.loc[pidx].to_dict()
        row_dict["Sale chăm sóc"] = dich_sale
        # Ghi lịch sử đổi sale vào Ghi chú để không mất dấu ai đã cầm số trước
        log_entry = f"[{today_str} Sale: {nguon_sale}→{dich_sale}]"
        old_note = str(row_dict.get("Ghi chú", "")).strip()
        row_dict["Ghi chú"] = f"{old_note} {log_entry}".strip() if old_note else log_entry
        append_staging_row(row_dict)

    for sr in sorted(selected_indices, reverse=True):  # selected_indices đã là sheet rows
        delete_crm_row(sr)

    names = [df.loc[i, "Tên khách"] for i in selected_indices]
    print(Fore.GREEN + f"\n  ✔ Đã chuyển {len(names)} lead sang SỐ MỚI KS (sale: {dich_sale}):")
    for n in names:
        print(Fore.WHITE + f"    • {n}")
    print(Fore.CYAN + f"\n  Nhắc {dich_sale}: mở Google Sheets → tab 'SỐ MỚI KS' → tích ✓ sau khi liên hệ.")
    return load_data()


def _quan_ly_doi(df):
    """Menu [7][f] — Quản lý đội thi đấu."""
    while True:
        cfg = load_config()
        teams = cfg.get("teams", {})
        print(Fore.CYAN + "\n─── CƠ CẤU ĐỘI THI ĐẤU ────────────────────────")
        for doi_name, members in teams.items():
            icon = "🔴" if doi_name == "Đỏ" else "🔵"
            print(f"  Đội {doi_name} {icon}: {', '.join(members) if members else '(trống)'}")
        players = [s for s in SALE_TEAM if s != "Hiển"]
        all_in_team = [m for ms in teams.values() for m in ms]
        no_team = [s for s in players if s not in all_in_team]
        if no_team:
            print(Fore.YELLOW + f"\n  ⚠ Chưa xếp đội: {', '.join(no_team)}")
        print(Fore.WHITE + "\n  [m] Di chuyển người sang đội khác")
        print(Fore.WHITE + "  [r] Đổi tên đội")
        print(Fore.WHITE + "  [s] Reset đội (xóa tất cả)")
        print(Fore.WHITE + "  [0] Quay lại\n")
        sub = input("  Chọn: ").strip().lower()

        if sub == "0":
            return

        elif sub == "m":
            print(Fore.WHITE + "  Chọn thành viên:")
            for i, s in enumerate(players, 1):
                cur_team = next((d for d, ms in teams.items() if s in ms), "Chưa có đội")
                print(f"    [{i}] {s}  (hiện: Đội {cur_team})")
            pick = input("  Số thứ tự: ").strip()
            if not pick.isdigit() or not (1 <= int(pick) <= len(players)):
                print(Fore.RED + "  Không hợp lệ.")
                continue
            member = players[int(pick) - 1]
            doi_list = list(teams.keys())
            print(Fore.WHITE + "  Chuyển vào đội:")
            for i, d in enumerate(doi_list, 1):
                icon = "🔴" if d == "Đỏ" else "🔵"
                print(f"    [{i}] Đội {d} {icon}")
            pick_d = input("  Số thứ tự: ").strip()
            if not pick_d.isdigit() or not (1 <= int(pick_d) <= len(doi_list)):
                print(Fore.RED + "  Không hợp lệ.")
                continue
            target_doi = doi_list[int(pick_d) - 1]
            for d in teams:
                if member in teams[d]:
                    teams[d].remove(member)
            if member not in teams[target_doi]:
                teams[target_doi].append(member)
            cfg["teams"] = teams
            save_config(cfg)
            print(Fore.GREEN + f"  ✔ Đã chuyển {member} → Đội {target_doi}")

        elif sub == "r":
            doi_list = list(teams.keys())
            print(Fore.WHITE + "  Đổi tên đội nào:")
            for i, d in enumerate(doi_list, 1):
                print(f"    [{i}] Đội {d}")
            pick = input("  Số thứ tự: ").strip()
            if not pick.isdigit() or not (1 <= int(pick) <= len(doi_list)):
                print(Fore.RED + "  Không hợp lệ.")
                continue
            old_name = doi_list[int(pick) - 1]
            new_name = input(f"  Tên mới cho Đội {old_name}: ").strip()
            if not new_name or new_name in teams:
                print(Fore.RED + "  Tên không hợp lệ hoặc đã tồn tại.")
                continue
            teams[new_name] = teams.pop(old_name)
            cfg["teams"] = teams
            save_config(cfg)
            print(Fore.GREEN + f"  ✔ Đổi tên Đội {old_name} → Đội {new_name}")

        elif sub == "s":
            confirm = input(Fore.YELLOW + "  Reset tất cả đội về trống? (yes/N): ").strip().lower()
            if confirm != "yes":
                print(Fore.YELLOW + "  Đã hủy.")
                continue
            for d in teams:
                teams[d] = []
            cfg["teams"] = teams
            save_config(cfg)
            print(Fore.GREEN + "  ✔ Đã reset tất cả đội về trống.")

        else:
            print(Fore.YELLOW + "  Lựa chọn không hợp lệ.")


def quan_ly_team(df):
    """Menu [7] — Thêm/xóa thành viên team, tự cập nhật config.json."""
    while True:
        cur_mode = load_config().get("assign_mode", "roundrobin")
        mode_label = "🎲 Ngẫu nhiên" if cur_mode == "random" else "🔄 Round-robin"
        print(Fore.CYAN + "\n─── QUẢN LÝ TEAM SALE ───────────────────────────")
        print(f"  Team hiện tại ({len(SALE_TEAM)} người):")
        for i, name in enumerate(SALE_TEAM, 1):
            print(f"    {i}. {name}")
        print(f"\n  Chế độ phân công lead: {mode_label}")
        print(f"\n  [a] Thêm thành viên mới")
        print(f"  [c] Vô hiệu hóa thành viên (xóa khỏi round-robin)")
        print(f"  [d] Đổi chế độ phân công lead")
        print(Fore.YELLOW + f"  [e] Chuyển leads sang sale khác")
        print(Fore.CYAN + f"  [f] Cơ cấu đội thi đấu")
        print(Fore.WHITE + f"  [0] Quay lại\n")
        choice = input("  Chọn: ").strip().lower()

        if choice == "0":
            return df

        elif choice == "a":
            ten = input("  Tên thành viên mới: ").strip()
            if not ten:
                print(Fore.YELLOW + "  Tên không được để trống.")
                continue
            if ten in SALE_TEAM:
                print(Fore.YELLOW + f"  '{ten}' đã có trong team rồi.")
                continue
            cfg = load_config()
            team = cfg.get("sale_team", list(SALE_TEAM))
            team.append(ten)
            cfg["sale_team"] = team
            cfg.setdefault("streaks", {})[ten] = {"count": 0, "last_date": ""}
            cfg.setdefault("badges_earned", {})[ten] = []
            cfg.setdefault("weekly_targets", {})[ten] = {"lead": 0, "xem_dat": 0}
            save_config(cfg)
            reload_team()
            print(Fore.GREEN + f"  ✔ Đã thêm {ten} vào team!")
            print(Fore.GREEN + f"  Team hiện tại: {', '.join(SALE_TEAM)}")
            print(Fore.YELLOW + f"  ⚠ Chưa xếp đội cho {ten} — vào [f] để phân đội")

        elif choice == "c":
            if len(SALE_TEAM) <= 1:
                print(Fore.RED + "  Không thể xóa — team cần ít nhất 1 người.")
                continue
            print("  Chọn người muốn vô hiệu hóa:")
            for i, name in enumerate(SALE_TEAM, 1):
                print(f"    [{i}] {name}")
            try:
                idx = int(input("  Số thứ tự: ")) - 1
                ten = SALE_TEAM[idx]
            except (ValueError, IndexError):
                print(Fore.RED + "  Lựa chọn không hợp lệ.")
                continue
            confirm = input(Fore.YELLOW + f"  Xác nhận vô hiệu hóa '{ten}'? (yes/N): ").strip().lower()
            if confirm != "yes":
                print(Fore.YELLOW + "  Đã hủy.")
                continue
            cfg = load_config()
            team = cfg.get("sale_team", list(SALE_TEAM))
            if ten in team:
                team.remove(ten)
            cfg["sale_team"] = team
            cfg.get("streaks", {}).pop(ten, None)
            cfg.get("badges_earned", {}).pop(ten, None)
            cfg.get("weekly_targets", {}).pop(ten, None)
            team_warnings = []
            for doi_name, members in cfg.get("teams", {}).items():
                if ten in members:
                    members.remove(ten)
                    team_warnings.append(doi_name)
            save_config(cfg)
            reload_team()
            print(Fore.GREEN + f"  ✔ Đã vô hiệu hóa '{ten}'.")
            print(Fore.GREEN + f"  Team còn lại: {', '.join(SALE_TEAM)}")
            print(Fore.YELLOW + f"  Lưu ý: dữ liệu khách cũ của '{ten}' vẫn còn trong Sheet.")
            for doi in team_warnings:
                print(Fore.RED + f"  ⚠ '{ten}' đã bị xóa khỏi Đội {doi} — vào [f] để tái cơ cấu đội")

        elif choice == "d":
            cfg = load_config()
            cur = cfg.get("assign_mode", "roundrobin")
            new_mode = "random" if cur == "roundrobin" else "roundrobin"
            cfg["assign_mode"] = new_mode
            save_config(cfg)
            if new_mode == "random":
                print(Fore.GREEN + "  ✔ Đã đổi sang chế độ: 🎲 NGẪU NHIÊN")
                print(Fore.YELLOW + "  Mỗi lead mới sẽ được giao cho một sale bất kỳ.")
            else:
                print(Fore.GREEN + "  ✔ Đã đổi sang chế độ: 🔄 ROUND-ROBIN")
                print(Fore.YELLOW + "  Lead mới sẽ được giao tuần tự theo danh sách team.")

        elif choice == "e":
            df = chuyen_leads_giua_sale(df)

        elif choice == "f":
            _quan_ly_doi(df)

        else:
            print(Fore.YELLOW + "  Lựa chọn không hợp lệ.")


def _print_table(df):
    header = (f"  {'#':>3} {'Tên khách':<18} {'Số ĐT':<13} "
              f"{'Trạng thái':<16} {'Sale':<12} {'Tương tác cuối':<16} Nguồn")
    print(Fore.WHITE + header)
    print("  " + "─" * 78)
    for i, (_, row) in enumerate(df.iterrows(), 1):
        d = days_since(row["Ngày tương tác cuối"])
        tt = row["Trạng thái"]
        if d >= REMIND_DAYS and tt in ACTIVE_STATUS and row.get("Nhu cầu", "") != "Không còn nhu cầu":
            color = Fore.RED
        elif d >= NURTURE_DAYS and row.get("Nhu cầu", "") == "Không còn nhu cầu" and tt != "Chốt cọc":
            color = Fore.YELLOW
        elif tt == "Chốt cọc":
            color = Fore.GREEN
        elif tt in DONE_STATUS:
            color = Fore.LIGHTBLACK_EX
        else:
            color = Fore.WHITE

        warn = f" [{d}ng]" if d >= REMIND_DAYS and tt in ACTIVE_STATUS and row.get("Nhu cầu", "") != "Không còn nhu cầu" else ""
        print(color + f"  {i:>3} {row['Tên khách']:<18} {row['Số ĐT']:<13} "
              f"{tt:<16} {row['Sale chăm sóc']:<12} "
              f"{row['Ngày tương tác cuối']:<14}{warn:<6} {row['Nguồn']}")
    print()


# ── MAIN LOOP ──────────────────────────────────────────────────────────────

def main():
    print(Fore.YELLOW + "  Đang tải dữ liệu từ Google Sheets...")
    df = load_data()
    names = transfer_checked_leads()
    if names:
        df = load_data()
        print(Fore.GREEN + f"  ✔ Đã chuyển {len(names)} khách từ SỐ MỚI KS vào CRM.")
    tele_names = transfer_telesale_checked()
    if tele_names:
        df = load_data()
        print(Fore.GREEN + f"  ✔ Đã chuyển {len(tele_names)} khách từ DATA TELESALE vào CRM.")
    _show_nhu_cau_banner(df)
    _show_staging_banner()
    _show_telesale_banner()
    _show_new_leads_today(df)
    while True:
        overdue_count = sum(
            1 for _, r in df.iterrows()
            if r["Trạng thái"] in ACTIVE_STATUS
            and r.get("Nhu cầu", "") != "Không còn nhu cầu"
            and days_since(r["Ngày tương tác cuối"]) >= REMIND_DAYS
        )
        _cur_cfg = load_config()
        assign_mode = _cur_cfg.get("assign_mode", "roundrobin")
        mode_tag = "🎲 Random" if assign_mode == "random" else "🔄 Round-robin"
        print(Fore.CYAN + f"\n{'═'*50}")
        print(Fore.CYAN + "  TRACKER — KHA SƠN GREEN HOME")
        print(Fore.CYAN + f"{'═'*50}")
        if overdue_count:
            print(Fore.RED + f"  *** {overdue_count} KHÁCH CẦN GỌI LẠI NGAY! ***")
        # Hiển thị streak lửa của từng player (bỏ qua Hiển — trưởng nhóm)
        _streaks = _cur_cfg.get("streaks", {})
        _streak_parts = []
        for _s in SALE_TEAM:
            if _s == "Hiển":
                continue
            _cnt = _streaks.get(_s, {}).get("count", 0)
            _fire = "🔥" if _cnt > 0 else "·"
            _streak_parts.append(f"{_s}:{_cnt}{_fire}")
        if _streak_parts:
            print(Fore.YELLOW + "  " + "  ".join(_streak_parts))
        print(f"\n  Tổng leads: {len(df)}  |  Phân công: {mode_tag}")
        print("  [1] Xem tất cả khách hàng")
        print("  [2] Lọc theo sale")
        print(Fore.RED + "  [3] Kiểm tra khách bị quên (> 3 ngày)")
        print(Fore.WHITE + "  [4] Thêm lead mới (tự động / chỉ định sale)")
        print("  [5] Cập nhật trạng thái")
        print("  [6] Làm mới dữ liệu từ Sheet")
        print(Fore.CYAN + "  [7] Quản lý team sale")
        print(Fore.WHITE + "  [8] Tìm kiếm theo SĐT")
        print(Fore.YELLOW + "  [9] Xử lý SỐ MỚI KS (chuyển lead đã tích ✓)")
        print(Fore.MAGENTA + "  [T] Xử lý DATA TELESALE (chuyển lead đã tích ✓)")
        print(Fore.WHITE + "  [0] Thoát\n")
        choice = input("  Chọn: ").strip()

        if choice == "1":
            view_all(df)
        elif choice == "2":
            view_by_sale(df)
        elif choice == "3":
            kiem_tra_quen_khach(df)
            kiem_tra_giu_tuong_tac(df)
        elif choice == "4":
            df = them_lead_moi(df)
        elif choice == "5":
            df = cap_nhat_trang_thai(df)
        elif choice == "6":
            print(Fore.YELLOW + "  Đang tải lại từ Google Sheets...")
            df = load_data()
            names = transfer_checked_leads()
            if names:
                df = load_data()
                print(Fore.GREEN + f"  ✔ Đã chuyển {len(names)} khách từ SỐ MỚI KS vào CRM.")
            tele_names = transfer_telesale_checked()
            if tele_names:
                df = load_data()
                print(Fore.GREEN + f"  ✔ Đã chuyển {len(tele_names)} khách từ DATA TELESALE vào CRM.")
            print(Fore.GREEN + f"  ✔ Đã cập nhật — {len(df)} khách hàng.")
            _show_nhu_cau_banner(df)
            _show_staging_banner()
            _show_telesale_banner()
            _show_new_leads_today(df)
        elif choice == "7":
            df = quan_ly_team(df)
        elif choice == "8":
            df = tim_kiem_sdt(df)
        elif choice == "9":
            df = xu_ly_so_moi(df)
        elif choice.upper() == "T":
            df = xu_ly_data_telesale(df)
        elif choice == "0":
            print("Tạm biệt!")
            break
        else:
            print(Fore.YELLOW + "  Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
