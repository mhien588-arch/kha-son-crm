"""
Báo cáo hiệu suất tuần — Kha Sơn Green Home
Chạy: python weekly_report.py
Dùng mỗi thứ Hai để so sánh tuần vừa qua với tuần trước.
"""
import os
import sys
from datetime import datetime, date, timedelta

try:
    import pandas as pd
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Cài thư viện: pip install pandas colorama")
    sys.exit(1)

from sheets_connector import load_data, load_config

_cfg = load_config()
REMIND_DAYS = _cfg.get("remind_days", 3)
ACTIVE_STATUS = ["Mới", "Đang chăm sóc"]
DONE_STATUS = ["Từ chối", "Chốt cọc"]


def get_week_range(offset=0):
    """Trả về (ngày đầu tuần, ngày cuối tuần) — offset=-1 là tuần trước."""
    today = date.today()
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def _in_range(date_str, start, end):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            d = datetime.strptime(str(date_str).strip(), fmt).date()
            return start <= d <= end
        except ValueError:
            continue
    return False


def build_weekly_summary(df, week_start, week_end, sale_team):
    lead_moi = len(df[df["Ngày tiếp cận"].apply(lambda x: _in_range(x, week_start, week_end))])
    in_week = df["Ngày tương tác cuối"].apply(lambda x: _in_range(x, week_start, week_end)).astype(bool)
    hen_xem = len(df[df["Trạng thái"].isin(["Hẹn xem đất", "Chốt cọc"]) & in_week])
    chot_coc = len(df[(df["Trạng thái"] == "Chốt cọc") & in_week])
    tong_active = len(df[~df["Trạng thái"].isin(DONE_STATUS)])
    ty_le_chot = round(chot_coc / tong_active * 100, 1) if tong_active else 0.0

    # Sale hiệu quả nhất tuần
    best_sale, best_score = None, -1
    for sale in sale_team:
        sdf = df[df["Sale chăm sóc"] == sale]
        in_week = sdf["Ngày tương tác cuối"].apply(lambda x: _in_range(x, week_start, week_end)).astype(bool)
        score = (
            len(sdf[(sdf["Trạng thái"] == "Chốt cọc") & in_week]) * 10 +
            len(sdf[(sdf["Trạng thái"] == "Hẹn xem đất") & in_week]) * 3
        )
        if score > best_score:
            best_score, best_sale = score, sale

    return {"lead_moi": lead_moi, "hen_xem": hen_xem, "chot_coc": chot_coc,
            "tong_active": tong_active, "ty_le_chot": ty_le_chot,
            "best_sale": best_sale, "best_score": best_score}


def build_source_analysis(df):
    result = []
    for nguon, gdf in df.groupby("Nguồn"):
        if not nguon or not str(nguon).strip():
            nguon = "Khác"
        total = len(gdf)
        chot = len(gdf[gdf["Trạng thái"] == "Chốt cọc"])
        ty_le = round(chot / total * 100, 1) if total else 0.0
        stars = "★★★" if ty_le >= 20 else ("★★" if ty_le >= 10 else ("★" if ty_le > 0 else ""))
        result.append({"nguon": str(nguon), "total": total, "chot": chot, "ty_le": ty_le, "stars": stars})
    result.sort(key=lambda x: x["ty_le"], reverse=True)
    return result


def build_team_scores(df, week_start, week_end, cfg):
    """Tính điểm đội Đỏ và Xanh trong tuần, trả về dict."""
    teams = cfg.get("teams", {})
    result = {}
    for doi_name, members in teams.items():
        total_diem = 0
        per_member = {}
        for sale in members:
            sdf = df[df["Sale chăm sóc"] == sale]
            in_week = sdf["Ngày tương tác cuối"].apply(lambda x: _in_range(x, week_start, week_end)).astype(bool)
            n_chot = len(sdf[(sdf["Trạng thái"] == "Chốt cọc") & in_week])
            n_hen = len(sdf[(sdf["Trạng thái"] == "Hẹn xem đất") & in_week])
            diem = n_chot * 10 + n_hen * 3
            per_member[sale] = {"diem": diem, "chot": n_chot, "hen": n_hen}
            total_diem += diem
        result[doi_name] = {"total": total_diem, "members": per_member}
    return result


def build_commitment_vs_actual(df, week_start, week_end, cfg, sale_team):
    """So sánh cam kết đầu tuần vs thực tế, trả về list."""
    targets = cfg.get("weekly_targets", {})
    players = [s for s in sale_team if s != "Hiển"]
    result = []
    for sale in players:
        sdf = df[df["Sale chăm sóc"] == sale]
        in_week_leads = sdf["Ngày tiếp cận"].apply(lambda x: _in_range(x, week_start, week_end))
        in_week_hen = sdf["Ngày tương tác cuối"].apply(lambda x: _in_range(x, week_start, week_end)).astype(bool)
        actual_lead = len(sdf[in_week_leads])
        actual_xem = len(sdf[(sdf["Trạng thái"].isin(["Hẹn xem đất", "Chốt cọc"])) & in_week_hen])
        t = targets.get(sale, {"lead": 0, "xem_dat": 0})
        target_lead = t.get("lead", 0)
        target_xem = t.get("xem_dat", 0)
        lead_ok = actual_lead >= target_lead if target_lead > 0 else None
        xem_ok = actual_xem >= target_xem if target_xem > 0 else None
        result.append({
            "sale": sale,
            "target_lead": target_lead,
            "actual_lead": actual_lead,
            "lead_ok": lead_ok,
            "target_xem": target_xem,
            "actual_xem": actual_xem,
            "xem_ok": xem_ok,
        })
    return result


def _delta_str(cur, prev):
    if prev == 0 and cur == 0:
        return "(=)"
    if prev == 0:
        return f"(+{cur})"
    diff = cur - prev
    if diff > 0:
        return f"(+{diff} so tuan truoc)"
    if diff < 0:
        return f"({diff} so tuan truoc)"
    return "(= so tuan truoc)"


def print_weekly(cur, prev, week_start, week_end, source_analysis, sale_team,
                 team_scores=None, commitment=None):
    W = 58
    week_num = week_start.isocalendar()[1]
    date_range = f"{week_start.strftime('%d/%m')} – {week_end.strftime('%d/%m/%Y')}"
    print(Fore.CYAN + "\n" + "═" * W)
    print(Fore.CYAN + f"  BAO CAO TUAN W{week_num}/2026  ({date_range})")
    print(Fore.CYAN + "═" * W)

    print(Fore.WHITE + f"\n  Lead moi tuan nay  : {Fore.YELLOW}{cur['lead_moi']:>3}  "
          + Fore.WHITE + _delta_str(cur["lead_moi"], prev["lead_moi"]))
    print(Fore.WHITE + f"  Hen xem dat        : {Fore.YELLOW}{cur['hen_xem']:>3}  "
          + Fore.WHITE + _delta_str(cur["hen_xem"], prev["hen_xem"]))
    print(Fore.WHITE + f"  Chot coc           : {Fore.GREEN}{cur['chot_coc']:>3}  "
          + Fore.WHITE + _delta_str(cur["chot_coc"], prev["chot_coc"]))
    print(Fore.WHITE + f"  Ty le chot         : {Fore.YELLOW}{cur['ty_le_chot']}%")
    print(Fore.WHITE + f"  Tong dang hoat dong: {Fore.WHITE}{cur['tong_active']} khach")

    kpi = _cfg.get("kpi", {})
    cpl_max = kpi.get("cpl_max", 100000)
    print(Fore.CYAN + "\n" + "─" * W)
    if cur["best_sale"] and cur["best_score"] > 0:
        print(Fore.GREEN + f"  SALE HIEU QUA NHAT : {cur['best_sale']} ({cur['best_score']} diem)")
    else:
        print(Fore.YELLOW + "  Tuan nay chua co chuyen doi nao.")

    lead_per_week_kpi = kpi.get("lead_moi_per_tuan", 20)
    kpi_ok = "OK" if cur["lead_moi"] >= lead_per_week_kpi else "CHUA DAT"
    print(Fore.WHITE + f"  CPL KPI            : <{cpl_max:,}d/lead  (leads: {cur['lead_moi']}, KPI: {lead_per_week_kpi}/tuan [{kpi_ok}])")

    # Phân tích nguồn
    if source_analysis:
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.WHITE + "  PHAN TICH NGUON LEAD")
        print(Fore.CYAN + "  " + "─" * (W - 2))
        print(Fore.WHITE + f"  {'Nguon':<18} {'Leads':>6} {'Chot':>6} {'Ty le':>8}  ")
        print("  " + "─" * (W - 2))
        for item in source_analysis:
            color = Fore.GREEN if item["stars"] == "★★★" else (Fore.YELLOW if item["stars"] else Fore.WHITE)
            print(color + f"  {item['nguon']:<18} {item['total']:>6} {item['chot']:>6} {item['ty_le']:>7.1f}%  {item['stars']}")

    # Block điểm đội
    if team_scores:
        print(Fore.CYAN + "\n" + "─" * W)
        print(Fore.WHITE + "  KET QUA DOI THI DAU TUAN NAY")
        print(Fore.CYAN + "  " + "─" * (W - 2))
        scores_list = sorted(team_scores.items(), key=lambda x: x[1]["total"], reverse=True)
        for i, (doi_name, data) in enumerate(scores_list):
            icon = "🔴" if doi_name == "Đỏ" else "🔵"
            color = Fore.YELLOW if i == 0 else Fore.WHITE
            win_tag = " ← THANG!" if i == 0 and len(scores_list) > 1 and data["total"] > scores_list[1][1]["total"] else ""
            print(color + f"  Doi {doi_name} {icon}: {data['total']} diem{win_tag}")
            for sale, stats in data["members"].items():
                print(Fore.WHITE + f"    • {sale:<14} {stats['diem']} diem  ({stats['chot']} chot, {stats['hen']} hen)")
        if len(scores_list) >= 2 and scores_list[0][1]["total"] > scores_list[1][1]["total"]:
            loser = scores_list[1][0]
            print(Fore.RED + f"  => Doi {loser} THUA — theo doi thang quyet dinh!")

    # Block cam kết vs thực tế
    if commitment:
        has_targets = any(r["target_lead"] > 0 or r["target_xem"] > 0 for r in commitment)
        if has_targets:
            print(Fore.CYAN + "\n" + "─" * W)
            print(Fore.WHITE + "  CAM KET vs THUC TE TUAN NAY")
            print(Fore.CYAN + "  " + "─" * (W - 2))
            print(Fore.WHITE + f"  {'Sale':<14} {'Lead cam':>9} {'Lead TT':>9} {'Xem cam':>9} {'Xem TT':>9}")
            print("  " + "─" * (W - 2))
            for r in commitment:
                lead_color = Fore.GREEN if r["lead_ok"] else (Fore.RED if r["lead_ok"] is False else Fore.WHITE)
                xem_color = Fore.GREEN if r["xem_ok"] else (Fore.RED if r["xem_ok"] is False else Fore.WHITE)
                lead_tag = "✓" if r["lead_ok"] else ("✗" if r["lead_ok"] is False else "-")
                xem_tag = "✓" if r["xem_ok"] else ("✗" if r["xem_ok"] is False else "-")
                print(Fore.WHITE + f"  {r['sale']:<14}" +
                      lead_color + f" {r['target_lead']:>9} {r['actual_lead']:>8}{lead_tag}" +
                      xem_color + f" {r['target_xem']:>9} {r['actual_xem']:>8}{xem_tag}")
        else:
            print(Fore.CYAN + "\n" + "─" * W)
            print(Fore.YELLOW + "  Chua co cam ket dau tuan — vao [7][g] de nhap muc tieu.")

    print(Fore.CYAN + "\n" + "═" * W + "\n")


def save_weekly(cur, prev, week_start, week_end, source_analysis, team_scores=None, commitment=None):
    week_num = week_start.isocalendar()[1]
    date_range = f"{week_start.strftime('%d/%m')} – {week_end.strftime('%d/%m/%Y')}"
    lines = [
        f"BAO CAO TUAN W{week_num}/2026  ({date_range})",
        "=" * 58,
        f"Lead moi tuan nay  : {cur['lead_moi']:>3}  {_delta_str(cur['lead_moi'], prev['lead_moi'])}",
        f"Hen xem dat        : {cur['hen_xem']:>3}  {_delta_str(cur['hen_xem'], prev['hen_xem'])}",
        f"Chot coc           : {cur['chot_coc']:>3}  {_delta_str(cur['chot_coc'], prev['chot_coc'])}",
        f"Ty le chot         : {cur['ty_le_chot']}%",
        f"Tong dang hoat dong: {cur['tong_active']} khach",
    ]
    if cur["best_sale"] and cur["best_score"] > 0:
        lines.append(f"Sale hieu qua nhat : {cur['best_sale']} ({cur['best_score']} diem)")
    lines.append("=" * 58)
    if source_analysis:
        lines.append("\nPHAN TICH NGUON LEAD:")
        lines.append("-" * 58)
        lines.append(f"{'Nguon':<18} {'Leads':>6} {'Chot':>6} {'Ty le':>8}")
        lines.append("-" * 58)
        for item in source_analysis:
            lines.append(f"{item['nguon']:<18} {item['total']:>6} {item['chot']:>6} {item['ty_le']:>7.1f}%  {item['stars']}")
        lines.append("=" * 58)

    # Điểm đội
    if team_scores:
        lines.append("\nKET QUA DOI THI DAU:")
        lines.append("-" * 58)
        for doi_name, data in sorted(team_scores.items(), key=lambda x: x[1]["total"], reverse=True):
            lines.append(f"  Doi {doi_name}: {data['total']} diem")
            for sale, stats in data["members"].items():
                lines.append(f"    • {sale:<14} {stats['diem']} diem ({stats['chot']} chot, {stats['hen']} hen)")
        lines.append("=" * 58)

    # Cam kết vs thực tế
    if commitment:
        has_targets = any(r["target_lead"] > 0 or r["target_xem"] > 0 for r in commitment)
        if has_targets:
            lines.append("\nCAM KET vs THUC TE:")
            lines.append("-" * 58)
            lines.append(f"{'Sale':<14} {'Lead cam':>9} {'Lead TT':>9} {'Xem cam':>9} {'Xem TT':>9}")
            lines.append("-" * 58)
            for r in commitment:
                lead_tag = "OK" if r["lead_ok"] else ("X" if r["lead_ok"] is False else "-")
                xem_tag = "OK" if r["xem_ok"] else ("X" if r["xem_ok"] is False else "-")
                lines.append(f"{r['sale']:<14} {r['target_lead']:>9} {r['actual_lead']:>8}({lead_tag}) "
                             f"{r['target_xem']:>9} {r['actual_xem']:>8}({xem_tag})")
            lines.append("=" * 58)

    fname = f"bao_cao_tuan_W{week_num}_2026.txt"
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path


def main():
    print(Fore.YELLOW + "Dang tai du lieu tu Google Sheets...")
    df = load_data()
    sale_team = load_config().get("sale_team", [])
    if not sale_team:
        sale_team = [s for s in df["Sale chăm sóc"].dropna().unique() if s.strip()]

    week_start, week_end = get_week_range(offset=0)
    prev_start, prev_end = get_week_range(offset=-1)

    cur = build_weekly_summary(df, week_start, week_end, sale_team)
    prev = build_weekly_summary(df, prev_start, prev_end, sale_team)
    source_analysis = build_source_analysis(df)

    cfg = load_config()
    team_scores = build_team_scores(df, week_start, week_end, cfg)
    commitment = build_commitment_vs_actual(df, week_start, week_end, cfg, sale_team)

    print_weekly(cur, prev, week_start, week_end, source_analysis, sale_team,
                 team_scores=team_scores, commitment=commitment)

    path = save_weekly(cur, prev, week_start, week_end, source_analysis,
                       team_scores=team_scores, commitment=commitment)
    print(Fore.GREEN + f"  Bao cao da luu: {path}")
    print(Fore.WHITE + "  Chup man hinh gui vao group Zalo team!\n")


if __name__ == "__main__":
    main()
