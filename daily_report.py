"""
Báo cáo hiệu suất cuối ngày — Kha Sơn Green Home
Chạy: python daily_report.py
Yêu cầu: pip install pandas colorama gspread google-auth
Nguồn dữ liệu: Google Sheets
"""
import os
import sys
import random
from datetime import datetime, date, timedelta

try:
    import pandas as pd
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Cài thư viện: pip install pandas colorama")
    sys.exit(1)

from sheets_connector import load_data, load_config, save_config, backup_to_csv

_cfg = load_config()
REMIND_DAYS = _cfg.get("remind_days", 3)
NURTURE_DAYS = _cfg.get("nurture_days", 14)
ACTIVE_STATUS = ["Mới", "Đang chăm sóc"]
CONVERT_STATUS = ["Hẹn xem đất", "Chốt cọc"]
DONE_STATUS = ["Từ chối", "Chốt cọc"]
FUNNEL_STAGES = ["Mới", "Đang chăm sóc", "Hẹn xem đất", "Chốt cọc"]


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


def build_summary(df, today_str):
    lead_moi = df[df["Ngày tiếp cận"] == today_str]
    dang_cham = df[~df["Trạng thái"].isin(DONE_STATUS)]
    chuyen_doi_hom_nay = df[
        (df["Ngày tương tác cuối"] == today_str) &
        (df["Trạng thái"].isin(CONVERT_STATUS))
    ]
    return {
        "lead_moi": len(lead_moi),
        "dang_cham": len(dang_cham),
        "chuyen_doi": len(chuyen_doi_hom_nay),
    }


def build_per_sale(df, today_str, sale_team):
    result = {}
    for sale in sale_team:
        sale_df = df[df["Sale chăm sóc"] == sale]
        dang_giu = len(sale_df[~sale_df["Trạng thái"].isin(DONE_STATUS)])

        chuyen_df = sale_df[
            (sale_df["Ngày tương tác cuối"] == today_str) &
            (sale_df["Trạng thái"].isin(CONVERT_STATUS))
        ]
        chuyen_hom_nay = len(chuyen_df)

        mask_active = sale_df["Trạng thái"].isin(ACTIVE_STATUS)
        mask_overdue = sale_df["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= REMIND_DAYS)
        nhu_cau_col = sale_df["Nhu cầu"].fillna("").astype(str) if "Nhu cầu" in sale_df.columns else pd.Series([""] * len(sale_df), index=sale_df.index, dtype=str)
        mask_nhu_cau_ok = (nhu_cau_col != "Không còn nhu cầu").astype(bool)
        mask_active_b = mask_active.astype(bool)
        mask_overdue_b = mask_overdue.astype(bool)
        qua_han_df = sale_df[mask_active_b & mask_overdue_b & mask_nhu_cau_ok]
        qua_han = len(qua_han_df)

        mask_knc = (nhu_cau_col == "Không còn nhu cầu").astype(bool)
        mask_nurture = sale_df["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= NURTURE_DAYS).astype(bool)
        mask_not_chot = (sale_df["Trạng thái"] != "Chốt cọc").astype(bool)
        giu_tt_df = sale_df[mask_knc & mask_nurture & mask_not_chot]
        giu_tt = len(giu_tt_df)

        ten_chuyen = [
            f"{r['Tên khách']} ({r['Trạng thái']})"
            for _, r in chuyen_df.iterrows()
        ]
        ten_qua_han = [
            f"{r['Tên khách']} ({days_since(r['Ngày tương tác cuối'])} ngày)"
            for _, r in qua_han_df.iterrows()
        ]
        ten_giu_tt = [
            f"{r['Tên khách']} ({days_since(r['Ngày tương tác cuối'])} ngày)"
            for _, r in giu_tt_df.iterrows()
        ]

        result[sale] = {
            "dang_giu": dang_giu,
            "chuyen_hom_nay": chuyen_hom_nay,
            "qua_han": qua_han,
            "giu_tt": giu_tt,
            "ten_chuyen": ten_chuyen,
            "ten_qua_han": ten_qua_han,
            "ten_giu_tt": ten_giu_tt,
        }
    return result


def build_nhu_cau(df):
    if "Nhu cầu" not in df.columns:
        return []
    rows = df[df["Nhu cầu"] == "Không còn nhu cầu"]
    return [{"ten": r["Tên khách"], "sale": r["Sale chăm sóc"], "tt": r["Trạng thái"],
             "days": days_since(r["Ngày tương tác cuối"])}
            for _, r in rows.iterrows()]


def build_funnel(df):
    counts = [len(df[df["Trạng thái"] == s]) for s in FUNNEL_STAGES]
    rates = [None]
    for i in range(1, len(counts)):
        rates.append(round(counts[i] / counts[i - 1] * 100, 1) if counts[i - 1] else 0.0)
    # Bottleneck: bước có rate thấp nhất (trong rates[1:])
    valid = [(r, i) for i, r in enumerate(rates) if r is not None]
    bottleneck_idx = min(valid, key=lambda x: x[0])[1] if valid else -1
    tu_choi = len(df[df["Trạng thái"] == "Từ chối"])
    tong_hd = len(df[~df["Trạng thái"].isin(DONE_STATUS)])
    chot_pct = round(counts[3] / (tong_hd + counts[3]) * 100, 1) if (tong_hd + counts[3]) else 0.0
    return {"counts": counts, "rates": rates, "bottleneck_idx": bottleneck_idx,
            "tu_choi": tu_choi, "tong_hd": tong_hd, "chot_pct": chot_pct}


def build_leaderboard(df, sale_team, today_str):
    month_prefix = today_str[:7]  # "YYYY-MM"
    result = []
    for sale in sale_team:
        sdf = df[df["Sale chăm sóc"] == sale]
        month_df = sdf[sdf["Ngày tương tác cuối"].str.startswith(month_prefix, na=False)]
        n_chot = len(month_df[month_df["Trạng thái"] == "Chốt cọc"])
        n_hen = len(month_df[month_df["Trạng thái"] == "Hẹn xem đất"])
        lb_mask_active = sdf["Trạng thái"].isin(ACTIVE_STATUS).astype(bool)
        lb_mask_overdue = sdf["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= REMIND_DAYS).astype(bool)
        lb_nhu_cau_col = sdf["Nhu cầu"].fillna("").astype(str) if "Nhu cầu" in sdf.columns else pd.Series([""] * len(sdf), index=sdf.index, dtype=str)
        lb_mask_nhu_cau_ok = (lb_nhu_cau_col != "Không còn nhu cầu").astype(bool)
        qua_han = len(sdf[lb_mask_active & lb_mask_overdue & lb_mask_nhu_cau_ok])
        bonus = 2 if qua_han == 0 and (n_chot + n_hen) > 0 else 0
        diem = n_chot * 10 + n_hen * 3 + bonus
        result.append({"sale": sale, "diem": diem, "chot": n_chot, "hen": n_hen, "bonus": bonus})
    result.sort(key=lambda x: x["diem"], reverse=True)
    return result


def print_report(summary, per_sale, today_str, nhu_cau_list=None, funnel=None, leaderboard=None,
                 streak_messages=None, is_golden=False, golden_name="", new_badges=None):
    W = 62
    print(Fore.CYAN + "\n" + "═" * W)
    print(Fore.CYAN + f"  BAO CAO HIEU SUAT TEAM — {today_str}")
    print(Fore.CYAN + "═" * W)

    # Block 1 — Tổng quan
    print(Fore.WHITE + f"\n  Lead mới hôm nay    : {Fore.YELLOW}{summary['lead_moi']} khách")
    print(Fore.WHITE + f"  Đang chăm sóc       : {Fore.YELLOW}{summary['dang_cham']} khách")
    print(Fore.WHITE + f"  Chuyển đổi hôm nay  : {Fore.GREEN}{summary['chuyen_doi']} (Hẹn xem + Chốt cọc)")

    # Block 2 — Bảng từng sale
    print(Fore.CYAN + "\n" + "─" * W)
    print(Fore.WHITE + f"  {'Tên Sale':<16} │ {'Đang giữ':^9} │ {'Hẹn/Chốt hôm nay':^20} │ {'Quá hạn':^9}")
    print("  " + "─" * 16 + "┼" + "─" * 11 + "┼" + "─" * 22 + "┼" + "─" * 10)

    best_sale = max(per_sale, key=lambda s: per_sale[s]["chuyen_hom_nay"], default=None)
    worst_sale = max(per_sale, key=lambda s: per_sale[s]["qua_han"], default=None)

    for sale, stats in per_sale.items():
        is_best = sale == best_sale and stats["chuyen_hom_nay"] > 0
        is_worst = sale == worst_sale and stats["qua_han"] > 0 and not is_best

        row_color = Fore.YELLOW if is_best else (Fore.RED if is_worst else Fore.WHITE)
        qua_han_str = f"{stats['qua_han']} 🔴" if stats["qua_han"] > 0 else "0"
        suffix = " ★" if is_best else (" !" if is_worst else "")

        print(row_color +
              f"  {sale:<16} │ {stats['dang_giu']:^9} │ {stats['chuyen_hom_nay']:^20} │ {qua_han_str:^9}{suffix}")

    # Block 2b — Chi tiết từng sale (tên khách cụ thể)
    has_detail = any(
        stats["ten_chuyen"] or stats["ten_qua_han"] or stats.get("ten_giu_tt")
        for stats in per_sale.values()
    )
    if has_detail:
        print(Fore.CYAN + "─" * W)
        print(Fore.WHITE + "  CHI TIẾT:")
        for sale, stats in per_sale.items():
            if not stats["ten_chuyen"] and not stats["ten_qua_han"] and not stats.get("ten_giu_tt"):
                continue
            first = True
            if stats["ten_chuyen"]:
                prefix = f"  {sale:<14}" if first else f"  {'':<14}"
                print(Fore.GREEN + f"{prefix} │ Hẹn/Chốt : {', '.join(stats['ten_chuyen'])}")
                first = False
            if stats["ten_qua_han"]:
                prefix = f"  {sale:<14}" if first else f"  {'':<14}"
                print(Fore.RED + f"{prefix} │ Quá hạn  : {', '.join(stats['ten_qua_han'])}")
                first = False
            if stats.get("ten_giu_tt"):
                prefix = f"  {sale:<14}" if first else f"  {'':<14}"
                print(Fore.YELLOW + f"{prefix} │ Giữ TT   : {', '.join(stats['ten_giu_tt'])}")

    # Block 3 — Khách không còn nhu cầu
    if nhu_cau_list:
        print(Fore.CYAN + "─" * W)
        print(Fore.RED + f"  KHACH KHONG CON NHU CAU ({len(nhu_cau_list)} khach):")
        for item in nhu_cau_list:
            days_str = f"{item['days']} ngày" if item['days'] < 9999 else "chưa có ngày"
            print(Fore.RED + f"    • {item['ten']} ({item['sale']}) — {item['tt']} — {days_str}")

    # Block 4 — Phễu chuyển đổi ASCII
    if funnel:
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.WHITE + "  PHEU CHUYEN DOI")
        print(Fore.CYAN + "  " + "─" * (W - 2))
        max_c = max(funnel["counts"]) or 1
        BAR = 20
        for i, (stage, count) in enumerate(zip(FUNNEL_STAGES, funnel["counts"])):
            bar_len = round(count / max_c * BAR)
            bar = "█" * bar_len
            color = Fore.GREEN if i == 3 else Fore.WHITE
            print(color + f"  {stage:<18} {bar:<22} {count} khach")
            if i < len(FUNNEL_STAGES) - 1 and funnel["rates"][i + 1] is not None:
                rate = funnel["rates"][i + 1]
                is_bn = (i + 1 == funnel["bottleneck_idx"])
                bn_label = Fore.RED + "  <- THAT CO CHAI" if is_bn else ""
                rate_color = Fore.RED if is_bn else Fore.YELLOW
                print(rate_color + f"  {'':18}   v {rate:.1f}%{bn_label}")
        print(Fore.CYAN + "  " + "─" * (W - 2))
        print(Fore.WHITE + f"  Tu choi: {funnel['tu_choi']}  |  Tong HD: {funnel['tong_hd']}  |  "
              f"Ty le chot: {funnel['chot_pct']}%")

    # Block 5 — Leaderboard tháng
    if leaderboard:
        month_label = today_str[:7].replace("-", "/")
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.WHITE + f"  LEADERBOARD THANG {month_label}")
        print(Fore.CYAN + "  " + "─" * (W - 2))
        medals = ["[1]", "[2]", "[3]", "   "]
        max_d = max(item["diem"] for item in leaderboard) or 1
        BAR = 16
        for i, item in enumerate(leaderboard):
            medal = medals[i] if i < 4 else "   "
            bar_len = round(item["diem"] / max_d * BAR)
            bar = "█" * bar_len
            detail = f"({item['chot']} chot, {item['hen']} hen"
            if item["bonus"]:
                detail += ", +bonus"
            detail += ")"
            color = Fore.YELLOW if i == 0 else Fore.WHITE
            print(color + f"  {medal} {item['sale']:<14} {bar:<18} {item['diem']:>3} diem  {detail}")

    # Block 6 — Streak lửa
    if streak_messages:
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.YELLOW + "  STREAK LUA HOm NAY:")
        for sale, count, bonus, msg in streak_messages:
            if msg and msg.startswith("💔"):
                print(Fore.RED + f"    {msg}")
            elif count > 0:
                fire = "🔥" * min(count // 7 + 1, 3)
                line = f"    {fire} {sale}: {count} ngay lien tiep"
                if bonus:
                    line += f"  [+{bonus} diem milestone!]"
                if msg and not msg.startswith("💔"):
                    line += f"  {msg}"
                print(Fore.YELLOW + line)

    # Block 7 — Ngày Vàng
    print(Fore.CYAN + "\n" + "─" * W)
    if is_golden:
        print(Fore.YELLOW + "  🌟 HOM NAY LA NGAY VANG — DIEM x3 DA AP DUNG!")
        print(Fore.YELLOW + f"  Moi lan cap nhat Hen/Chot hom nay ({today_str}) tinh gap 3!")
    else:
        print(Fore.WHITE + f"  ⏳ Ngay Vang tuan nay chua xuat hien... (tiep tuc co gang!)")

    # Block 8 — Huy hiệu mới
    if new_badges:
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.YELLOW + "  🏅 HUY HIEU MOI MO KHOA:")
        for sale, msg in new_badges:
            print(Fore.GREEN + f"    ★ {msg}")

    # Block cuối — Tuyên dương & Cảnh báo
    print(Fore.CYAN + "\n" + "═" * W)
    if best_sale and per_sale[best_sale]["chuyen_hom_nay"] > 0:
        n = per_sale[best_sale]["chuyen_hom_nay"]
        print(Fore.GREEN + f"  BEST TODAY  : {best_sale} — {n} chuyen doi — Xuat sac!")
    else:
        print(Fore.YELLOW + "  Hom nay chua co chuyen doi — Co len team!")

    if worst_sale and per_sale[worst_sale]["qua_han"] > 0:
        n = per_sale[worst_sale]["qua_han"]
        print(Fore.RED + f"  CAN CAI THIEN: {worst_sale} — {n} khach qua han, goi lai ngay!")

    print(Fore.CYAN + "═" * W + "\n")


def save_report(summary, per_sale, today_str, nhu_cau_list=None, funnel=None, leaderboard=None,
                streak_messages=None, is_golden=False, golden_name="", new_badges=None):
    lines = [
        f"BÁO CÁO HIỆU SUẤT TEAM — {today_str}",
        "=" * 58,
        f"Lead mới hôm nay    : {summary['lead_moi']} khách",
        f"Đang chăm sóc       : {summary['dang_cham']} khách",
        f"Chuyển đổi hôm nay  : {summary['chuyen_doi']} (Hẹn xem + Chốt cọc)",
        "",
        f"{'Tên Sale':<16} | {'Đang giữ':^8} | {'Hẹn/Chốt':^10} | {'Quá hạn':^8}",
        "-" * 50,
    ]
    for sale, stats in per_sale.items():
        lines.append(
            f"{sale:<16} | {stats['dang_giu']:^8} | {stats['chuyen_hom_nay']:^10} | {stats['qua_han']:^8}"
        )
    lines.append("=" * 58)

    # Chi tiết tên khách
    has_detail = any(
        stats["ten_chuyen"] or stats["ten_qua_han"] or stats.get("ten_giu_tt")
        for stats in per_sale.values()
    )
    if has_detail:
        lines.append("\nCHI TIET:")
        lines.append("-" * 58)
        for sale, stats in per_sale.items():
            if not stats["ten_chuyen"] and not stats["ten_qua_han"] and not stats.get("ten_giu_tt"):
                continue
            if stats["ten_chuyen"]:
                lines.append(f"{sale:<14} | Hen/Chot : {', '.join(stats['ten_chuyen'])}")
            if stats["ten_qua_han"]:
                prefix = f"{'':<14}" if stats["ten_chuyen"] else f"{sale:<14}"
                lines.append(f"{prefix} | Qua han  : {', '.join(stats['ten_qua_han'])}")
            if stats.get("ten_giu_tt"):
                prefix = f"{'':<14}" if (stats["ten_chuyen"] or stats["ten_qua_han"]) else f"{sale:<14}"
                lines.append(f"{prefix} | Giu TT   : {', '.join(stats['ten_giu_tt'])}")
        lines.append("=" * 58)

    # Khách không còn nhu cầu
    if nhu_cau_list:
        lines.append(f"\nKHACH KHONG CON NHU CAU ({len(nhu_cau_list)} khach):")
        lines.append("-" * 58)
        for item in nhu_cau_list:
            days_str = f"{item['days']} ngay" if item['days'] < 9999 else "chua co ngay"
            lines.append(f"  • {item['ten']} ({item['sale']}) — {item['tt']} — {days_str}")
        lines.append("=" * 58)

    # Phễu chuyển đổi
    if funnel:
        lines.append("\nPHEU CHUYEN DOI:")
        lines.append("-" * 58)
        max_c = max(funnel["counts"]) or 1
        for i, (stage, count) in enumerate(zip(FUNNEL_STAGES, funnel["counts"])):
            bar = "█" * round(count / max_c * 16)
            lines.append(f"  {stage:<18} {bar:<18} {count} khach")
            if i < len(FUNNEL_STAGES) - 1 and funnel["rates"][i + 1] is not None:
                rate = funnel["rates"][i + 1]
                bn = " <- THAT CO CHAI" if (i + 1 == funnel["bottleneck_idx"]) else ""
                lines.append(f"  {'':18}   v {rate:.1f}%{bn}")
        lines.append(f"  Tu choi: {funnel['tu_choi']} | Tong HD: {funnel['tong_hd']} | "
                     f"Ty le chot: {funnel['chot_pct']}%")
        lines.append("=" * 58)

    # Leaderboard
    if leaderboard:
        month_label = today_str[:7].replace("-", "/")
        lines.append(f"\nLEADERBOARD THANG {month_label}:")
        lines.append("-" * 58)
        for i, item in enumerate(leaderboard, 1):
            detail = f"({item['chot']} chot, {item['hen']} hen"
            if item["bonus"]:
                detail += ", +bonus"
            detail += ")"
            lines.append(f"  [{i}] {item['sale']:<14} {item['diem']:>3} diem  {detail}")
        lines.append("=" * 58)

    # Streak
    if streak_messages:
        lines.append("\nSTREAK LUA HOM NAY:")
        lines.append("-" * 58)
        for sale, count, bonus, msg in streak_messages:
            if msg and msg.startswith("💔"):
                lines.append(f"  {msg}")
            elif count > 0:
                line = f"  {sale}: {count} ngay"
                if bonus:
                    line += f" (+{bonus} diem)"
                if msg and not msg.startswith("💔"):
                    line += f" {msg}"
                lines.append(line)

    # Golden Day
    lines.append("")
    if is_golden:
        lines.append(f"🌟 HOM NAY LA NGAY VANG — DIEM x3 ({today_str})")
    else:
        lines.append("⏳ Ngay Vang tuan nay chua xuat hien")

    # New badges
    if new_badges:
        lines.append("\n🏅 HUY HIEU MOI:")
        lines.append("-" * 58)
        for sale, msg in new_badges:
            lines.append(f"  ★ {msg}")
        lines.append("=" * 58)

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"bao_cao_{today_str}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path


_DAY_NAMES = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu"]
_STREAK_MILESTONES = {3: 1, 7: 3, 14: 7, 30: 20}


def update_streaks(df, today_str, sale_team):
    """Cập nhật streak lửa cuối ngày cho từng player, trả về (bonus_dict, messages)."""
    cfg = load_config()
    streaks = cfg.get("streaks", {})
    players = [s for s in sale_team if s != "Hiển"]
    bonus_dict = {}
    messages = []

    for sale in players:
        sdf = df[df["Sale chăm sóc"] == sale]
        n_today = len(sdf[sdf["Ngày tương tác cuối"] == today_str])
        sd = streaks.get(sale, {"count": 0, "last_date": ""})
        last_date = sd.get("last_date", "")
        count = sd.get("count", 0)

        if last_date == today_str:
            bonus_dict[sale] = 0
            continue

        if n_today >= 2:
            new_count = count + 1
            streaks[sale] = {"count": new_count, "last_date": today_str}
            bonus = _STREAK_MILESTONES.get(new_count, 0)
            if new_count == 3:
                messages.append((sale, new_count, bonus, "🔥3 ngày liên tiếp!"))
            elif new_count == 7:
                messages.append((sale, new_count, bonus, "🔥🔥7 ngày — TUẦN VÀNG!"))
            elif new_count == 14:
                messages.append((sale, new_count, bonus, "🔥🔥🔥14 ngày — HUYỀN THOẠI!"))
            elif new_count == 30:
                messages.append((sale, new_count, bonus, "🏆30 ngày — BẤT KHẢ XÂM PHẠM!"))
            else:
                messages.append((sale, new_count, 0, None))
            bonus_dict[sale] = bonus
        else:
            if count > 0:
                messages.append((sale, 0, 0, f"💔 {sale} mất streak {count} ngày"))
            streaks[sale] = {"count": 0, "last_date": today_str}
            bonus_dict[sale] = 0

    cfg["streaks"] = streaks
    save_config(cfg)
    return bonus_dict, messages


def check_golden_day(today_str, leaderboard):
    """Kiểm tra / khởi tạo Ngày Vàng tuần — nếu hôm nay là Ngày Vàng thì x3 điểm."""
    today = datetime.strptime(today_str, "%Y-%m-%d").date()
    cur_week = today.isocalendar()[1]
    cur_weekday = today.weekday()  # 0=Thứ Hai … 4=Thứ Sáu

    cfg = load_config()
    gd = cfg.get("golden_day", {"week": 0, "day_of_week": -1})

    if gd.get("week", 0) != cur_week:
        chosen = random.randint(0, 4)
        gd = {"week": cur_week, "day_of_week": chosen}
        cfg["golden_day"] = gd
        save_config(cfg)

    golden_idx = gd.get("day_of_week", -1)
    is_golden = (cur_weekday == golden_idx) and (0 <= golden_idx <= 4)

    if is_golden:
        for item in leaderboard:
            item["diem"] = item["chot"] * 30 + item["hen"] * 9 + item.get("bonus", 0) + item.get("streak_bonus", 0)
            item["golden"] = True
    else:
        for item in leaderboard:
            item.setdefault("golden", False)

    golden_name = _DAY_NAMES[golden_idx] if 0 <= golden_idx <= 4 else "?"
    return is_golden, golden_name, gd


def check_badges(df, today_str, sale_team, streaks_after):
    """Kiểm tra 8 huy hiệu bí mật — chỉ thông báo khi mới đạt lần đầu."""
    cfg = load_config()
    badges_earned = cfg.get("badges_earned", {})
    players = [s for s in sale_team if s != "Hiển"]
    new_badges = []

    week_start_str = (date.today() - timedelta(days=date.today().weekday())).strftime("%Y-%m-%d")

    def _grant(sale, key, msg):
        if key not in badges_earned.get(sale, []):
            badges_earned.setdefault(sale, []).append(key)
            new_badges.append((sale, msg))

    for sale in players:
        sdf = df[df["Sale chăm sóc"] == sale]
        nhu_cau_col = (sdf["Nhu cầu"].fillna("").astype(str) if "Nhu cầu" in sdf.columns
                       else pd.Series([""] * len(sdf), index=sdf.index, dtype=str))

        # 🚀 Tên lửa — cập nhật 5 khách trong 1 ngày
        if len(sdf[sdf["Ngày tương tác cuối"] == today_str]) >= 5:
            _grant(sale, "ten_lua", f"🚀 {sale} mở khóa TÊN LỬA! (cập nhật 5+ khách hôm nay)")

        # 💎 Kim cương — chốt cọc
        if len(sdf[(sdf["Trạng thái"] == "Chốt cọc") & (sdf["Ngày tương tác cuối"] == today_str)]) > 0:
            _grant(sale, "kim_cuong", f"💎 {sale} — CHỐT CỌC — LEGENDARY!")

        # 🎯 Bắn tỉa — 3 lần Hẹn xem đất trong tuần
        if len(sdf[(sdf["Trạng thái"] == "Hẹn xem đất") & (sdf["Ngày tương tác cuối"] >= week_start_str)]) >= 3:
            _grant(sale, "ban_tia", f"🎯 {sale} — Bắn tỉa chuyên nghiệp! (3 hẹn xem đất tuần này)")

        # 🌱 Gieo hạt — 5 lead mới trong tuần
        if len(sdf[sdf["Ngày tiếp cận"] >= week_start_str]) >= 5:
            _grant(sale, "gieo_hat", f"🌱 {sale} — Người gieo hạt! (5 lead mới tuần này)")

        # 🔥 Bất diệt — streak 14 ngày
        streak_count = cfg.get("streaks", {}).get(sale, {}).get("count", 0)
        if streak_count >= 14:
            _grant(sale, "bat_diet", f"🔥 {sale} — STREAK {streak_count} NGÀY — Không ai dừng nổi!")

        # 🛡️ Vệ sĩ — 0 khách ACTIVE quá hạn (có ít nhất 3 lead đang chăm)
        active_m = sdf["Trạng thái"].isin(ACTIVE_STATUS).astype(bool)
        overdue_m = sdf["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= REMIND_DAYS).astype(bool)
        nc_ok_m = (nhu_cau_col != "Không còn nhu cầu").astype(bool)
        if len(sdf[active_m]) >= 3 and len(sdf[active_m & overdue_m & nc_ok_m]) == 0:
            _grant(sale, "ve_si", f"🛡️ {sale} — Không để sót một ai! (0 khách quá hạn)")

    if new_badges:
        cfg["badges_earned"] = badges_earned
        save_config(cfg)

    return new_badges


def main():
    today_str = date.today().strftime("%Y-%m-%d")
    print(Fore.YELLOW + "Đang tải dữ liệu từ Google Sheets...")
    df = load_data()
    # Tự động sao lưu dữ liệu CRM thành file CSV cục bộ
    backup_to_csv()

    sale_team = load_config().get("sale_team", [])
    if not sale_team:
        sale_team = [s for s in df["Sale chăm sóc"].dropna().unique() if s.strip()]
    if not sale_team:
        print(Fore.YELLOW + "Chưa có dữ liệu leads. Thêm khách qua tracker.py trước.")
        return

    summary = build_summary(df, today_str)
    per_sale = build_per_sale(df, today_str, sale_team)
    nhu_cau_list = build_nhu_cau(df)
    funnel = build_funnel(df)
    leaderboard = build_leaderboard(df, sale_team, today_str)

    # Cập nhật streak và áp bonus vào leaderboard
    bonus_dict, streak_messages = update_streaks(df, today_str, sale_team)
    for item in leaderboard:
        sb = bonus_dict.get(item["sale"], 0)
        item["diem"] += sb
        item["streak_bonus"] = sb
    leaderboard.sort(key=lambda x: x["diem"], reverse=True)

    # Kiểm tra Ngày Vàng (có thể nhân x3 điểm leaderboard)
    is_golden, golden_name, gd = check_golden_day(today_str, leaderboard)

    # Kiểm tra huy hiệu bí mật
    new_badges = check_badges(df, today_str, sale_team, bonus_dict)

    print_report(summary, per_sale, today_str, nhu_cau_list, funnel, leaderboard,
                 streak_messages=streak_messages, is_golden=is_golden,
                 golden_name=golden_name, new_badges=new_badges)

    path = save_report(summary, per_sale, today_str, nhu_cau_list, funnel, leaderboard,
                       streak_messages=streak_messages, is_golden=is_golden,
                       golden_name=golden_name, new_badges=new_badges)
    print(Fore.GREEN + f"  Báo cáo đã lưu: {path}")
    print(Fore.WHITE + "  Chụp màn hình gửi vào group Zalo team!\n")


if __name__ == "__main__":
    main()
