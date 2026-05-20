"""
Web Dashboard CRM — Kha Sơn Green Home
Chạy: streamlit run dashboard.py
Yêu cầu: pip install streamlit plotly pandas gspread google-auth
"""
import os
import re
import sys
import json
import random
from datetime import datetime, date, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import textwrap

# Thiết lập cấu hình trang Streamlit với icon và tiêu đề chuyên nghiệp
st.set_page_config(
    page_title="CRM BKD2",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm path hiện tại để import sheets_connector
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if _BASE_DIR not in sys.path:
    sys.path.append(_BASE_DIR)

from sheets_connector import (
    load_data, append_row, update_row, COLUMNS, load_config, save_config,
    highlight_new_row, unhighlight_row, append_staging_row, load_staging_data,
    transfer_checked_leads, delete_crm_row, ensure_staging_tab, backup_to_csv
)

# ── CÁU HÌNH & KHỞI TẠO ──
TRANG_THAI_OPTIONS = ["Mới", "Đang chăm sóc", "Hẹn xem đất", "Từ chối", "Chốt cọc"]
NHU_CAU_OPTIONS = ["Còn nhu cầu", "Không còn nhu cầu"]
ACTIVE_STATUS = ["Mới", "Đang chăm sóc"]
DONE_STATUS = ["Từ chối", "Chốt cọc"]
CONVERT_STATUS = ["Hẹn xem đất", "Chốt cọc"]
FUNNEL_STAGES = ["Mới", "Đang chăm sóc", "Hẹn xem đất", "Chốt cọc"]
_DAY_NAMES = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu"]

# ── PHƯƠNG THỨC HỖ TRỢ ──

def clean_phone_number(phone: str) -> str:
    """Làm sạch và validate số điện thoại chuẩn Việt Nam."""
    cleaned = re.sub(r'\D', '', str(phone).strip())
    if not cleaned:
        return ""
    # Nếu dài 9 số và không có số 0 ở đầu, thêm số 0
    if len(cleaned) == 9 and not cleaned.startswith('0'):
        cleaned = '0' + cleaned
    return cleaned

def validate_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại có đúng định dạng 10 số bắt đầu bằng 0 hay không."""
    return bool(re.match(r'^0\d{9}$', phone))

def format_phone_display(phone: str) -> str:
    """Định dạng hiển thị số điện thoại dạng dễ đọc: 0982 287 863."""
    cleaned = clean_phone_number(phone)
    if len(cleaned) == 10:
        return f"{cleaned[:4]} {cleaned[4:7]} {cleaned[7:]}"
    return cleaned if cleaned else str(phone)

def clean_html(html: str) -> str:
    """Loại bỏ khoảng trắng thụt lề đầu dòng để tránh Markdown nhận nhầm thành code block."""
    return "\n".join(line.lstrip() for line in str(html).split("\n"))



def days_since(date_str):
    """Tính số ngày trôi qua từ ngày date_str."""
    if not str(date_str).strip():
        return 9999
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            d = datetime.strptime(str(date_str).strip(), fmt).date()
            return (date.today() - d).days
        except ValueError:
            continue
    return 9999

# Inject CSS để tạo giao diện premium với phong cách Navy lịch lãm
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Background and Style */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Custom Card Style with Glassmorphism and Hover Micro-animation */
    .premium-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
        border-color: #3B82F6;
    }
    
    /* Header design */
    .header-title {
        background: linear-gradient(to right, #60A5FA, #3B82F6, #1D4ED8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    .header-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Custom Badges */
    .custom-badge {
        padding: 6px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        text-align: center;
    }
    .badge-primary { background-color: #1E3A8A; color: #93C5FD; border: 1px solid #3B82F6; }
    .badge-success { background-color: #064E3B; color: #6EE7B7; border: 1px solid #10B981; }
    .badge-warning { background-color: #78350F; color: #FCD34D; border: 1px solid #F59E0B; }
    .badge-danger { background-color: #7F1D1D; color: #FCA5A5; border: 1px solid #EF4444; }
    .badge-secondary { background-color: #374151; color: #D1D5DB; border: 1px solid #4B5563; }
</style>
""", unsafe_allow_html=True)

# ── TẢI DỮ LIỆU CÓ CACHING ──
@st.cache_data(ttl=300)  # Cache 5 phút để tránh quá tải API 429
def get_cached_crm_data():
    return load_data()

@st.cache_data(ttl=300)
def get_cached_staging_data():
    return load_staging_data()

def clear_cache():
    st.cache_data.clear()
    st.toast("🔄 Đã tải lại dữ liệu mới nhất từ Google Sheets!", icon="⚡")

# Load cấu hình
cfg = load_config()
sale_team = cfg.get("sale_team", ["Hiển", "Đức", "Tuấn Anh", "Nam", "Chị Dung"])
remind_days = cfg.get("remind_days", 3)
nurture_days = cfg.get("nurture_days", 14)
assign_mode = cfg.get("assign_mode", "roundrobin")

# Sidebar navigation
with st.sidebar:
    st.markdown('<p style="font-size: 1.5rem; font-weight: 800; color: #3B82F6; margin-bottom: 20px; text-align: center;">KHA SƠN GREEN HOME</p>', unsafe_allow_html=True)
    
    # Nút đồng bộ nhanh
    if st.button("🔄 Tải lại dữ liệu (F5)", use_container_width=True):
        clear_cache()
    
    st.markdown("---")
    
    menu = st.radio(
        "ĐIỀU HƯỚNG HỆ THỐNG",
        [
            "🏠 Tổng quan & Báo cáo",
            "📋 Danh sách Leads CRM",
            "📥 Số Mới Chờ Duyệt (Staging)",
            "⚡ Nhập Số Hàng Loạt & Phân Chia",
            "👥 Quản lý Team & Cấu hình"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown(f"**Chế độ chia lead:** `{assign_mode.upper()}`")
    st.markdown(f"**Ngưỡng nhắc nhở:** `{remind_days} ngày`")
    st.markdown(f"**Ngưỡng nuôi dưỡng:** `{nurture_days} ngày`")
    st.markdown('<p style="color: #64748B; font-size: 0.8rem; text-align: center;">CRM Engine v2.0 • Powered by Antigravity</p>', unsafe_allow_html=True)

# Đọc dữ liệu từ Google Sheets
with st.spinner("Đang kết nối Google Sheets..."):
    df_crm = get_cached_crm_data()
    df_stg, stg_indices = get_cached_staging_data()

today_str = date.today().strftime("%Y-%m-%d")

# ───────────────────────────────────────────────────────────────────────────
# 🏠 TỔNG QUAN & BÁO CÁO (DASHBOARD)
# ───────────────────────────────────────────────────────────────────────────
if menu == "🏠 Tổng quan & Báo cáo":
    st.markdown('<p class="header-title">🏠 TỔNG QUAN & HIỆU SUẤT TEAM</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="header-subtitle">Dự án: Đất nền KCN Phú Bình, Thái Nguyên | Hôm nay: <b>{date.today().strftime("%d/%m/%Y")}</b></p>', unsafe_allow_html=True)

    if df_crm.empty:
        st.info("Chưa có dữ liệu leads nào. Hãy thêm khách hàng trước.")
    else:
        # 1. Tính toán KPIs
        total_leads = len(df_crm)
        
        # Leads mới tiếp cận hôm nay
        lead_moi_hom_nay = len(df_crm[df_crm["Ngày tiếp cận"] == today_str])
        
        # Đang chăm sóc (ACTIVE)
        active_leads = len(df_crm[~df_crm["Trạng thái"].isin(DONE_STATUS)])
        
        # Chuyển đổi hôm nay (Hẹn xem đất + Chốt cọc có ngày tương tác là hôm nay)
        chuyen_doi_hom_nay = len(df_crm[
            (df_crm["Ngày tương tác cuối"] == today_str) &
            (df_crm["Trạng thái"].isin(CONVERT_STATUS))
        ])
        
        # Số lượng chốt cọc tháng này
        month_prefix = today_str[:7]
        df_month = df_crm[df_crm["Ngày tương tác cuối"].str.startswith(month_prefix, na=False)]
        chot_coc_month = len(df_month[df_month["Trạng thái"] == "Chốt cọc"])
        hen_xem_month = len(df_month[df_month["Trạng thái"] == "Hẹn xem đất"])
        
        # 2. Hiển thị KPI Cards dạng Custom HTML
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.markdown(f"""
            <div class="premium-card">
                <p style="color: #94A3B8; font-size: 0.9rem; margin: 0; font-weight: 600;">TỔNG SỐ KHÁCH HÀNG</p>
                <p style="color: #60A5FA; font-size: 2.2rem; font-weight: 800; margin: 10px 0 0 0;">{total_leads}</p>
                <p style="color: #10B981; font-size: 0.8rem; margin: 5px 0 0 0; font-weight: 500;">📈 +{lead_moi_hom_nay} khách mới hôm nay</p>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
            <div class="premium-card">
                <p style="color: #94A3B8; font-size: 0.9rem; margin: 0; font-weight: 600;">ĐANG CHĂM SÓC (ACTIVE)</p>
                <p style="color: #FBBF24; font-size: 2.2rem; font-weight: 800; margin: 10px 0 0 0;">{active_leads}</p>
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 5px 0 0 0; font-weight: 500;">💼 Đang trực tiếp tương tác</p>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
            <div class="premium-card">
                <p style="color: #94A3B8; font-size: 0.9rem; margin: 0; font-weight: 600;">CHUYỂN ĐỔI HÔM NAY</p>
                <p style="color: #34D399; font-size: 2.2rem; font-weight: 800; margin: 10px 0 0 0;">{chuyen_doi_hom_nay}</p>
                <p style="color: #34D399; font-size: 0.8rem; margin: 5px 0 0 0; font-weight: 500;">✨ Hẹn xem đất hoặc Chốt cọc</p>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col4:
            st.markdown(f"""
            <div class="premium-card">
                <p style="color: #94A3B8; font-size: 0.9rem; margin: 0; font-weight: 600;">CHỐT THÁNG {datetime.now().strftime("%m/%Y")}</p>
                <p style="color: #F87171; font-size: 2.2rem; font-weight: 800; margin: 10px 0 0 0;">{chot_coc_month}</p>
                <p style="color: #F87171; font-size: 0.8rem; margin: 5px 0 0 0; font-weight: 500;">🎯 Mục tiêu tháng: {cfg.get('kpi', {}).get('chot_coc_per_thang', 3)} giao dịch</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Phân chia Cột: Biểu đồ Phễu vs Bảng Xếp Hạng Leaderboard
        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            st.markdown('<p style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin-bottom: 15px;">📊 PHỄU CHUYỂN ĐỔI KHÁCH HÀNG</p>', unsafe_allow_html=True)
            
            # Tính dữ liệu phễu
            funnel_counts = [len(df_crm[df_crm["Trạng thái"] == stage]) for stage in FUNNEL_STAGES]
            tu_choi = len(df_crm[df_crm["Trạng thái"] == "Từ chối"])
            
            # Vẽ biểu đồ phễu bằng Plotly
            fig_funnel = go.Figure(go.Funnel(
                y=FUNNEL_STAGES,
                x=funnel_counts,
                textinfo="value+percent initial",
                marker={"color": ["#60A5FA", "#3B82F6", "#2563EB", "#10B981"]},
                connector={"fillcolor": "#334155"}
            ))
            fig_funnel.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#F8FAFC", "family": "Inter"},
                margin={"t": 30, "l": 80, "r": 20, "b": 20},
                height=320
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
            st.write(f"ℹ️ *Có thêm **{tu_choi}** khách đã Từ chối chăm sóc.*")

        with chart_col2:
            st.markdown('<p style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin-bottom: 15px;">🏆 BẢNG XẾP HẠNG LEADERBOARD THÁNG</p>', unsafe_allow_html=True)
            
            # Tính điểm của từng Sale theo quy tắc daily_report
            leaderboard_data = []
            cur_weekday = date.today().weekday()
            is_golden = False
            
            # Kiểm tra Ngày Vàng từ config
            gd = cfg.get("golden_day", {"week": 0, "day_of_week": -1})
            cur_week = date.today().isocalendar()[1]
            if gd.get("week", 0) == cur_week and cur_weekday == gd.get("day_of_week", -1):
                is_golden = True
            
            for sale in sale_team:
                sdf = df_crm[df_crm["Sale chăm sóc"] == sale]
                month_df = sdf[sdf["Ngày tương tác cuối"].str.startswith(month_prefix, na=False)]
                n_chot = len(month_df[month_df["Trạng thái"] == "Chốt cọc"])
                n_hen = len(month_df[month_df["Trạng thái"] == "Hẹn xem đất"])
                
                # Cảnh báo quá hạn của sale
                lb_mask_active = sdf["Trạng thái"].isin(ACTIVE_STATUS).astype(bool)
                lb_mask_overdue = sdf["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= remind_days).astype(bool)
                lb_nhu_cau_col = sdf["Nhu cầu"].fillna("").astype(str) if "Nhu cầu" in sdf.columns else pd.Series([""] * len(sdf), index=sdf.index, dtype=str)
                lb_mask_nhu_cau_ok = (lb_nhu_cau_col != "Không còn nhu cầu").astype(bool)
                qua_han = len(sdf[lb_mask_active & lb_mask_overdue & lb_mask_nhu_cau_ok])
                
                # Bonus chuyên nghiệp
                bonus = 2 if qua_han == 0 and (n_chot + n_hen) > 0 else 0
                
                # Điểm số nhân ngày vàng nếu có
                if is_golden:
                    diem = n_chot * 30 + n_hen * 9 + bonus
                else:
                    diem = n_chot * 10 + n_hen * 3 + bonus
                
                # Thêm streak bonus nếu có lưu trong config
                streak_count = cfg.get("streaks", {}).get(sale, {}).get("count", 0)
                streak_bonus = 0
                if streak_count == 3: streak_bonus = 1
                elif streak_count == 7: streak_bonus = 3
                elif streak_count == 14: streak_bonus = 7
                elif streak_count == 30: streak_bonus = 20
                diem += streak_bonus
                
                leaderboard_data.append({
                    "Sale": sale,
                    "Điểm": diem,
                    "Chốt cọc": n_chot,
                    "Hẹn xem": n_hen,
                    "Streak (ngày)": streak_count,
                    "Huy hiệu": ", ".join(cfg.get("badges_earned", {}).get(sale, [])) or "Chưa có"
                })
            
            df_lb = pd.DataFrame(leaderboard_data).sort_values(by="Điểm", ascending=False)
            
            # Vẽ biểu đồ ngang cột điểm cực chuyên nghiệp
            fig_lb = px.bar(
                df_lb,
                x="Điểm",
                y="Sale",
                orientation="h",
                text="Điểm",
                color="Điểm",
                color_continuous_scale=["#1E3A8A", "#3B82F6", "#10B981"]
            )
            fig_lb.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#F8FAFC", "family": "Inter"},
                margin={"t": 10, "l": 20, "r": 20, "b": 10},
                height=280,
                coloraxis_showscale=False
            )
            fig_lb.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_lb, use_container_width=True)
            
            if is_golden:
                st.markdown('<span class="custom-badge badge-warning">🌟 NGÀY VÀNG: Điểm Hẹn/Chốt đang x3!</span>', unsafe_allow_html=True)

        st.markdown("---")
        
        # 4. Hiệu suất chi tiết của từng Sale
        st.markdown('<p style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin-bottom: 15px;">🔥 TÌNH HÌNH CHIẾN ĐẤU CỦA ĐỘI NGŨ SALE</p>', unsafe_allow_html=True)
        
        sale_cols = st.columns(len(sale_team))
        for idx, sale in enumerate(sale_team):
            with sale_cols[idx]:
                sdf = df_crm[df_crm["Sale chăm sóc"] == sale]
                
                # Tính toán các chỉ số cho sale card
                active_count = len(sdf[~sdf["Trạng thái"].isin(DONE_STATUS)])
                
                # Quá hạn của sale này
                m_active = sdf["Trạng thái"].isin(ACTIVE_STATUS).astype(bool)
                m_overdue = sdf["Ngày tương tác cuối"].apply(lambda x: days_since(x) >= remind_days).astype(bool)
                nhu_cau_col = sdf["Nhu cầu"].fillna("").astype(str) if "Nhu cầu" in sdf.columns else pd.Series([""] * len(sdf), index=sdf.index, dtype=str)
                m_nc_ok = (nhu_cau_col != "Không còn nhu cầu").astype(bool)
                overdue_count = len(sdf[m_active & m_overdue & m_nc_ok])
                
                streak = cfg.get("streaks", {}).get(sale, {}).get("count", 0)
                badges = cfg.get("badges_earned", {}).get(sale, [])
                
                badge_html = ""
                for b in badges[:2]:
                    if b == "ve_si": badge_html += "🛡️ "
                    elif b == "ten_lua": badge_html += "🚀 "
                    elif b == "kim_cuong": badge_html += "💎 "
                    elif b == "ban_tia": badge_html += "🎯 "
                    elif b == "gieo_hat": badge_html += "🌱 "
                    elif b == "bat_diet": badge_html += "🔥 "
                
                # Highlight viền đỏ nếu sale có khách quá hạn nhiều
                border_color = "#EF4444" if overdue_count > 0 else "#334155"
                bg_color = "rgba(127, 29, 29, 0.1)" if overdue_count > 0 else "rgba(30, 41, 59, 0.4)"
                
                st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 16px;
                    text-align: center;
                ">
                    <p style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin: 0;">{sale} {badge_html}</p>
                    <p style="font-size: 0.8rem; color: #94A3B8; margin: 2px 0 10px 0;">Streak: 🔥 {streak} ngày</p>
                    <hr style="border: 0; border-top: 1px solid #334155; margin: 8px 0;"/>
                    <div style="display: flex; justify-content: space-around; align-items: center;">
                        <div>
                            <p style="font-size: 0.75rem; color: #94A3B8; margin: 0;">Đang Giữ</p>
                            <p style="font-size: 1.3rem; font-weight: 700; color: #3B82F6; margin: 0;">{active_count}</p>
                        </div>
                        <div>
                            <p style="font-size: 0.75rem; color: #94A3B8; margin: 0;">Quá Hạn</p>
                            <p style="font-size: 1.3rem; font-weight: 700; color: {'#EF4444' if overdue_count > 0 else '#10B981'}; margin: 0;">{overdue_count}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────────────────
# 📋 DANH SÁCH LEADS CRM & THAO TÁC NHANH
# ───────────────────────────────────────────────────────────────────────────
elif menu == "📋 Danh sách Leads CRM":
    st.markdown('<p class="header-title">📋 HỆ THỐNG QUẢN LÝ KHÁCH HÀNG CRM</p>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Bộ lọc thông minh, chỉnh sửa dữ liệu thời gian thực và quản lý tập trung</p>', unsafe_allow_html=True)

    # 1. Phần Bộ lọc dữ liệu trực quan
    st.markdown('<p style="font-size: 1.2rem; font-weight: 600; color: #3B82F6;">🔍 BỘ LỌC TÌM KIẾM</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        search_query = st.text_input("Tìm theo Tên hoặc Số ĐT:", "").strip()
    with col_f2:
        filter_sale = st.selectbox("Lọc theo Sale chăm sóc:", ["Tất cả"] + list(sale_team))
    with col_f3:
        filter_status = st.selectbox("Lọc theo Trạng thái:", ["Tất cả"] + TRANG_THAI_OPTIONS)
    with col_f4:
        filter_need = st.selectbox("Lọc theo Nhu cầu:", ["Tất cả", "Còn nhu cầu", "Không còn nhu cầu", "(Trống)"])
        
    # Áp dụng bộ lọc
    filtered_df = df_crm.copy()
    
    if search_query:
        # Tìm kiếm không phân biệt chữ hoa thường hoặc kiểm tra số ĐT
        filtered_df = filtered_df[
            filtered_df["Tên khách"].str.contains(search_query, case=False, na=False) |
            filtered_df["Số ĐT"].str.contains(search_query, na=False)
        ]
        
    if filter_sale != "Tất cả":
        filtered_df = filtered_df[filtered_df["Sale chăm sóc"] == filter_sale]
        
    if filter_status != "Tất cả":
        filtered_df = filtered_df[filtered_df["Trạng thái"] == filter_status]
        
    if filter_need != "Tất cả":
        if filter_need == "(Trống)":
            filtered_df = filtered_df[filtered_df["Nhu cầu"].isna() | (filtered_df["Nhu cầu"] == "")]
        else:
            filtered_df = filtered_df[filtered_df["Nhu cầu"] == filter_need]

    # Tính toán chỉ số sau lọc
    st.write(f"✨ Tìm thấy **{len(filtered_df)}** khách hàng phù hợp bộ lọc.")

    # 2. Hiển thị bảng dữ liệu với màu sắc cực kỳ tinh tế
    if not filtered_df.empty:
        # Chuẩn bị một DataFrame hiển thị có màu sắc trạng thái
        display_df = filtered_df.copy()
        
        # Thêm cột tính ngày quá hạn để hiển thị trực quan
        display_df["Quá hạn (ngày)"] = display_df["Ngày tương tác cuối"].apply(
            lambda x: f"{days_since(x)} ngày" if days_since(x) < 9999 else "Chưa tương tác"
        )
        
        # Xây dựng bảng hiển thị HTML để tùy biến màu sắc tinh tế cho từng Trạng thái
        html_table = """
        <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse: collapse; background-color: #1E293B; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <thead>
                <tr style="background-color: #0F172A; text-align: left; color: #94A3B8; border-bottom: 2px solid #334155;">
                    <th style="padding: 12px 16px;">Hàng (Sheet)</th>
                    <th style="padding: 12px 16px;">Tên Khách Hàng</th>
                    <th style="padding: 12px 16px;">Số Điện Thoại</th>
                    <th style="padding: 12px 16px;">Nguồn</th>
                    <th style="padding: 12px 16px;">Sale Phụ Trách</th>
                    <th style="padding: 12px 16px;">Trạng Thái</th>
                    <th style="padding: 12px 16px;">Quá Hạn</th>
                    <th style="padding: 12px 16px;">Nhu Cầu</th>
                    <th style="padding: 12px 16px;">Ghi Chú</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Thiết lập bảng màu nền tinh tế cho từng trạng thái
        status_colors = {
            "Mới": "rgba(245, 158, 11, 0.15)",         # Vàng nhạt
            "Đang chăm sóc": "rgba(59, 130, 246, 0.15)",  # Xanh dương nhạt
            "Hẹn xem đất": "rgba(16, 185, 129, 0.15)",    # Xanh lá nhạt
            "Từ chối": "rgba(100, 116, 139, 0.15)",       # Xám nhạt
            "Chốt cọc": "rgba(16, 185, 129, 0.3)"         # Xanh lá đậm hơn
        }
        
        for idx, row in display_df.iterrows():
            stt = row["Trạng thái"]
            bg_color = status_colors.get(stt, "rgba(255, 255, 255, 0.05)")
            
            # Cảnh báo màu đỏ nổi bật cho những khách quá hạn chăm sóc
            days = days_since(row["Ngày tương tác cuối"])
            is_overdue = days >= remind_days and stt in ACTIVE_STATUS and row["Nhu cầu"] != "Không còn nhu cầu"
            overdue_style = "color: #EF4444; font-weight: 700;" if is_overdue else "color: #10B981;"
            
            # Badge trạng thái dạng pill
            badge_class = "badge-primary"
            if stt == "Mới": badge_class = "badge-warning"
            elif stt == "Hẹn xem đất": badge_class = "badge-primary"
            elif stt == "Chốt cọc": badge_class = "badge-success"
            elif stt == "Từ chối": badge_class = "badge-danger"
            elif stt == "Đang chăm sóc": badge_class = "badge-secondary"
            
            need_badge = ""
            if row["Nhu cầu"] == "Còn nhu cầu":
                need_badge = '<span class="custom-badge badge-success">Còn</span>'
            elif row["Nhu cầu"] == "Không còn nhu cầu":
                need_badge = '<span class="custom-badge badge-danger">KNC</span>'
            
            html_table += f"""
            <tr style="background-color: {bg_color}; border-bottom: 1px solid #334155;">
                <td style="padding: 12px 16px; font-weight: 600;">{idx}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #FFF;">{row['Tên khách']}</td>
                <td style="padding: 12px 16px;">{format_phone_display(row['Số ĐT'])}</td>
                <td style="padding: 12px 16px;">{row['Nguồn']}</td>
                <td style="padding: 12px 16px; font-weight: 500; color: #3B82F6;">{row['Sale chăm sóc']}</td>
                <td style="padding: 12px 16px;"><span class="custom-badge {badge_class}">{stt}</span></td>
                <td style="padding: 12px 16px; {overdue_style}">{row['Quá hạn (ngày)']}</td>
                <td style="padding: 12px 16px;">{need_badge}</td>
                <td style="padding: 12px 16px; font-size: 0.9rem; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{row['Ghi chú']}">{row['Ghi chú']}</td>
            </tr>
            """
            
        html_table += "</tbody></table></div>"
        st.markdown(clean_html(html_table), unsafe_allow_html=True)
    else:
        st.warning("Không có khách hàng nào phù hợp với bộ lọc.")

    st.markdown("---")

    # 3. Form thao tác chỉnh sửa và Cập nhật trực tiếp
    st.markdown('<p style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin-bottom: 15px;">⚙️ THAO TÁC & CẬP NHẬT TRẠNG THÁI KHÁCH HÀNG</p>', unsafe_allow_html=True)
    
    col_act1, col_act2 = st.columns([1, 1])
    
    with col_act1:
        st.markdown('<p style="font-weight: 600; color: #3B82F6;">📝 CHỈNH SỬA / CẬP NHẬT LEAD HIỆN TẠI</p>', unsafe_allow_html=True)
        
        # Chọn khách hàng để sửa
        cust_choices = [f"Dòng {i}: {r['Tên khách']} ({r['Số ĐT']}) - {r['Sale chăm sóc']}" for i, r in df_crm.iterrows()]
        selected_cust = st.selectbox("Chọn khách hàng cần cập nhật:", ["--- Chọn khách hàng ---"] + cust_choices)
        
        if selected_cust != "--- Chọn khách hàng ---":
            # Trích xuất chỉ số hàng từ chuỗi lựa chọn
            row_num = int(selected_cust.split(":")[0].replace("Dòng ", ""))
            row_data = df_crm.loc[row_num]
            
            # Hiển thị form cập nhật dữ liệu của khách đó
            with st.form("update_lead_form"):
                c_ten = st.text_input("Tên khách hàng:", row_data["Tên khách"])
                c_sdt = st.text_input("Số điện thoại:", row_data["Số ĐT"])
                c_nguon = st.text_input("Nguồn lead:", row_data["Nguồn"])
                c_sale = st.selectbox("Sale chăm sóc:", list(sale_team), index=list(sale_team).index(row_data["Sale chăm sóc"]) if row_data["Sale chăm sóc"] in sale_team else 0)
                c_status = st.selectbox("Trạng thái hiện tại:", TRANG_THAI_OPTIONS, index=TRANG_THAI_OPTIONS.index(row_data["Trạng thái"]) if row_data["Trạng thái"] in TRANG_THAI_OPTIONS else 0)
                c_need = st.selectbox("Nhu cầu:", [""] + NHU_CAU_OPTIONS, index=([""] + NHU_CAU_OPTIONS).index(row_data["Nhu cầu"]) if row_data["Nhu cầu"] in ([""] + NHU_CAU_OPTIONS) else 0)
                c_ghichu = st.text_area("Ghi chú tiến độ chăm sóc:", row_data["Ghi chú"])
                
                # Checkbox để cập nhật ngày tương tác thành ngày hôm nay
                update_interactive_date = st.checkbox("Cập nhật 'Ngày tương tác cuối' thành hôm nay", value=True)
                
                submit_update = st.form_submit_button("💾 Xác nhận Cập nhật Lên Google Sheets")
                
                if submit_update:
                    if not c_ten.strip():
                        st.error("Tên khách hàng không được phép để trống!")
                    else:
                        updated_row = {
                            "Tên khách": c_ten.strip(),
                            "Số ĐT": c_sdt.strip(),
                            "Nguồn": c_nguon.strip(),
                            "Sale chăm sóc": c_sale,
                            "Trạng thái": c_status,
                            "Ghi chú": c_ghichu.strip(),
                            "Ngày tiếp cận": row_data["Ngày tiếp cận"],
                            "Ngày tương tác cuối": today_str if update_interactive_date else row_data["Ngày tương tác cuối"],
                            "Nhu cầu": c_need
                        }
                        
                        # Gọi cập nhật lên Google Sheets API
                        with st.spinner("Đang lưu lên hệ thống Cloud..."):
                            update_row(row_num, updated_row)
                            
                            # Nếu đổi trạng thái khỏi "Mới", hủy in đậm
                            if row_data["Trạng thái"] == "Mới" and c_status != "Mới":
                                unhighlight_row(row_num)
                                
                            clear_cache()
                            st.success(f"✔ Đã cập nhật thành công thông tin của khách hàng: {c_ten}!")
                            st.rerun()

    with col_act2:
        st.markdown('<p style="font-weight: 600; color: #10B981;">➕ THÊM LEAD MỚI THỦ CÔNG</p>', unsafe_allow_html=True)
        
        with st.form("add_new_lead_form"):
            new_ten = st.text_input("Tên khách hàng mới:")
            new_sdt = st.text_input("Số điện thoại (để trống nếu chưa có):")
            new_nguon = st.text_input("Nguồn lead (FB Ads, Zalo, Giới thiệu,...):", value="Khách thủ công")
            
            # Chọn sale phân chia
            new_sale_choice = st.selectbox(
                "Phân công cho Sale:", 
                ["Tự động chia (Round-robin / Random)"] + list(sale_team)
            )
            new_ghichu = st.text_area("Ghi chú ban đầu:")
            
            submit_add = st.form_submit_button("➕ Thêm mới vào Tab Staging (Chờ liên hệ)")
            
            if submit_add:
                if not new_ten.strip():
                    st.error("Không được bỏ trống Tên khách hàng!")
                else:
                    # Clean và validate số điện thoại
                    cleaned_s = clean_phone_number(new_sdt)
                    valid_s = True
                    if new_sdt.strip() != "":
                        if not validate_phone(cleaned_s):
                            st.error("Số điện thoại không hợp lệ! Phải đủ 10 số bắt đầu bằng đầu số 0.")
                            valid_s = False
                            
                    if valid_s:
                        # Kiểm tra trùng lặp số điện thoại
                        is_duplicate = False
                        if cleaned_s != "":
                            dup_crm = df_crm[df_crm["Số ĐT"].str.strip() == cleaned_s] if not df_crm.empty else pd.DataFrame()
                            dup_stg = df_stg[df_stg["Số ĐT"].str.strip() == cleaned_s] if not df_stg.empty else pd.DataFrame()
                            all_dups = pd.concat([dup_crm, dup_stg])
                            
                            if not all_dups.empty:
                                row_dup = all_dups.iloc[0]
                                src = "Staging" if dup_crm.empty else "CRM chính thức"
                                st.warning(f"⚠️ Trùng SĐT với khách **{row_dup['Tên khách']}** của sale **{row_dup['Sale chăm sóc']}** trong hệ thống {src}!")
                                is_duplicate = True
                        
                        if is_duplicate:
                            st.info("Vẫn thêm khách này? Nếu muốn ghi đè hoặc thêm trùng, hãy sử dụng tính năng 'Nhập số hàng loạt' hoặc liên hệ trưởng nhóm.")
                        
                        # Quyết định chọn sale chăm sóc
                        if "Tự động chia" in new_sale_choice:
                            # Bộ chia lead tự động
                            if assign_mode == "random":
                                assigned_sale = random.choice(sale_team)
                            else:
                                if df_crm.empty:
                                    assigned_sale = sale_team[0]
                                else:
                                    last_sale = df_crm["Sale chăm sóc"].iloc[-1]
                                    idx = sale_team.index(last_sale) if last_sale in sale_team else -1
                                    assigned_sale = sale_team[(idx + 1) % len(sale_team)]
                        else:
                            assigned_sale = new_sale_choice
                            
                        # Thêm lead mới
                        new_lead = {
                            "Tên khách": new_ten.strip(),
                            "Số ĐT": cleaned_s,
                            "Nguồn": new_nguon.strip(),
                            "Sale chăm sóc": assigned_sale,
                            "Trạng thái": "Mới",
                            "Ghi chú": new_ghichu.strip(),
                            "Ngày tiếp cận": today_str,
                            "Ngày tương tác cuối": today_str
                        }
                        
                        with st.spinner("Đang thêm lead mới vào hệ thống..."):
                            append_staging_row(new_lead)
                            clear_cache()
                            st.success(f"✔ Đã thêm thành công khách hàng {new_ten} vào Tab Staging! Hãy vào tab 'Số Mới Chờ Duyệt' để kiểm duyệt.")
                            st.rerun()

# ───────────────────────────────────────────────────────────────────────────
# 📥 SỐ MỚI CHỜ DUYỆT (STAGING TAB)
# ───────────────────────────────────────────────────────────────────────────
elif menu == "📥 Số Mới Chờ Duyệt (Staging)":
    st.markdown('<p class="header-title">📥 TAB STAGING — SỐ MỚI CHỜ DUYỆT</p>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">leads mới đổ về từ Facebook Ads hoặc nhập ngoài sẽ lưu tại đây để Sale liên hệ lần đầu, sau đó tích chọn để chuyển vào CRM chính thức.</p>', unsafe_allow_html=True)

    if df_stg.empty:
        st.success("🎉 Tuyệt vời! Hiện không còn lead mới nào tồn đọng trong Tab Staging.")
    else:
        st.markdown(f"💼 Hiện đang có **{len(df_stg)}** leads mới chưa được xử lý liên hệ lần đầu.")
        
        # Hiển thị DataFrame danh sách staging
        df_stg_display = df_stg.copy()
        
        # Render bảng HTML Staging với style Navy đẹp mắt
        html_stg_table = """
        <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse: collapse; background-color: #1E293B; border-radius: 12px; overflow: hidden;">
            <thead>
                <tr style="background-color: #0F172A; text-align: left; color: #94A3B8; border-bottom: 2px solid #334155;">
                    <th style="padding: 12px 16px;">Tên Khách Hàng</th>
                    <th style="padding: 12px 16px;">Số Điện Thoại</th>
                    <th style="padding: 12px 16px;">Nguồn</th>
                    <th style="padding: 12px 16px;">Sale Phụ Trách</th>
                    <th style="padding: 12px 16px;">Ngày Tiếp Cận</th>
                    <th style="padding: 12px 16px;">Trạng Thái</th>
                    <th style="padding: 12px 16px;">Ghi Chú Ban Đầu</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, row in df_stg_display.iterrows():
            html_stg_table += f"""
            <tr style="border-bottom: 1px solid #334155;">
                <td style="padding: 12px 16px; font-weight: 600; color: #FFF;">{row['Tên khách']}</td>
                <td style="padding: 12px 16px;">{format_phone_display(row['Số ĐT'])}</td>
                <td style="padding: 12px 16px;">{row['Nguồn']}</td>
                <td style="padding: 12px 16px; font-weight: 600; color: #3B82F6;">{row['Sale chăm sóc']}</td>
                <td style="padding: 12px 16px;">{row['Ngày tiếp cận']}</td>
                <td style="padding: 12px 16px;"><span class="custom-badge badge-warning">Chờ duyệt</span></td>
                <td style="padding: 12px 16px; font-size: 0.9rem;">{row['Ghi chú']}</td>
            </tr>
            """
        html_stg_table += "</tbody></table></div>"
        st.markdown(clean_html(html_stg_table), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Cơ chế duyệt chuyển leads từ Staging vào CRM
        st.markdown('<p style="font-size: 1.2rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">⚡ DUYỆT & ĐẨY KHÁCH HÀNG SANG CRM CHÍNH</p>', unsafe_allow_html=True)
        
        st.info("💡 Hướng dẫn: Để đẩy khách hàng từ Staging sang CRM, sale cần lên file Google Sheets tab 'SỐ MỚI KS', tích chọn vào ô cột **'✓ Đã xử lý'** sau khi thực hiện cuộc gọi/tương tác đầu tiên. Sau đó nhấn nút Duyệt ở dưới đây!")
        
        if st.button("🚀 Bắt đầu Quét & Duyệt Leads đã Tích chọn", use_container_width=True):
            with st.spinner("Đang đồng bộ và chuyển các leads đã tương tác vào CRM chính..."):
                checked_names = transfer_checked_leads()
                if checked_names:
                    # Tạo sao lưu tự động ngay khi có thay đổi lớn
                    backup_to_csv()
                    clear_cache()
                    st.success(f"✔ Đã duyệt và chuyển thành công **{len(checked_names)}** leads vào CRM chính thức: {', '.join(checked_names)}")
                    st.rerun()
                else:
                    st.warning("⚠️ Không tìm thấy lead nào được tích ✓ trong tab 'SỐ MỚI KS' trên Google Sheets.")

# ───────────────────────────────────────────────────────────────────────────
# ⚡ NHẬP SỐ HÀNG LOẠT & TỰ ĐỘNG CHIA LEADS (BULK IMPORT)
# ───────────────────────────────────────────────────────────────────────────
elif menu == "⚡ Nhập Số Hàng Loạt & Phân Chia":
    st.markdown('<p class="header-title">⚡ NHẬP SỐ HÀNG LOẠT & PHÂN PHỐI SALE</p>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Hỗ trợ Trưởng nhóm nhập nhanh hàng chục, hàng trăm số điện thoại từ tệp danh sách thô, tự động làm sạch, kiểm tra trùng lặp và phân chia công bằng cho Sale chỉ trong 3 giây.</p>', unsafe_allow_html=True)

    # 1. Khu vực dán data thô
    st.markdown('<p style="font-size: 1.2rem; font-weight: 600; color: #3B82F6;">📋 DÁN DANH SÁCH SỐ ĐIỆN THOẠI THÔ</p>', unsafe_allow_html=True)
    
    st.info("""
    💡 Định dạng chấp nhận (Mỗi dòng một khách):
    - Dạng 1 (Chỉ số ĐT): `0987123456`
    - Dạng 2 (Tên - SĐT): `Anh Hòa - 0912345678`
    - Dạng 3 (Tên, SĐT): `Chị Lan, 0345678912`
    """)
    
    raw_leads_text = st.text_area(
        "Nhập danh sách vào đây:",
        height=200,
        placeholder="Anh Bình - 0912345678\n0987654321\nChị Hoa, 0933445566"
    )

    # 2. Cấu hình quy chuẩn phân chia leads
    st.markdown('<p style="font-size: 1.2rem; font-weight: 600; color: #3B82F6; margin-top: 20px;">⚙️ THIẾT LẬP PHÂN CHIA LEADS</p>', unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        # Lựa chọn các sale sẽ được chia trong đợt này
        st.write("👥 Chọn các Sale nhận lead đợt này:")
        active_sales_for_bulk = []
        for s in sale_team:
            if st.checkbox(s, value=True, key=f"bulk_sale_{s}"):
                active_sales_for_bulk.append(s)
                
    with col_b2:
        # Chọn chế độ chia lead
        bulk_mode = st.radio(
            "Chế độ chia số:",
            ["Xoay vòng (Round-robin) — Chia đều", "Ngẫu nhiên (Random)"],
            index=0
        )
        
    with col_b3:
        # Thiết lập Nguồn lead và ghi chú
        bulk_source = st.text_input("Nguồn lead đợt này:", "Tệp Leads Nguội")
        bulk_ghichu = st.text_input("Ghi chú đính kèm:", "Nhập hàng loạt qua Dashboard")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Nút hành động nhập số và chia leads
    if st.button("🚀 Bắt đầu Nhập số & Tự động Phân phối cho Sale", use_container_width=True):
        if not raw_leads_text.strip():
            st.error("Vui lòng dán danh sách số điện thoại thô!")
        elif not active_sales_for_bulk:
            st.error("Vui lòng chọn ít nhất một Sale để phân chia số điện thoại!")
        else:
            # Bắt đầu phân tách dữ liệu thô
            lines = raw_leads_text.strip().split("\n")
            parsed_leads = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Thử phân tách bằng dấu gạch ngang, phẩy, tab, chấm phẩy
                parts = []
                for sep in ("-", ",", "\t", ";"):
                    if sep in line:
                        parts = [p.strip() for p in line.split(sep, 1)]
                        break
                        
                if len(parts) == 2:
                    name, phone = parts[0], parts[1]
                else:
                    name = "Khách Hàng Mới"
                    phone = line
                    
                cleaned_p = clean_phone_number(phone)
                
                # Chỉ lấy số điện thoại hợp lệ
                if cleaned_p:
                    parsed_leads.append({"Tên khách": name, "Số ĐT": cleaned_p})
            
            if not parsed_leads:
                st.error("❌ Không tìm thấy số điện thoại hợp lệ nào trong danh sách dán vào!")
            else:
                st.markdown("### 📊 KẾT QUẢ XỬ LÝ LÔ HÀNG LOẠT:")
                
                total_input = len(lines)
                valid_count = len(parsed_leads)
                
                # Thực hiện lọc trùng lặp chéo với CRM chính và Staging
                duplicates_removed = 0
                final_leads = []
                
                # Tạo set để lọc trùng trong chính lô đang nhập
                seen_in_batch = set()
                
                with st.spinner("Đang lọc trùng số điện thoại thời gian thực..."):
                    for lead in parsed_leads:
                        ph = lead["Số ĐT"]
                        
                        # 1. Trùng trong lô nhập
                        if ph in seen_in_batch:
                            duplicates_removed += 1
                            continue
                            
                        # 2. Trùng trong CRM chính thức
                        dup_crm = df_crm[df_crm["Số ĐT"].str.strip() == ph] if not df_crm.empty else pd.DataFrame()
                        
                        # 3. Trùng trong Staging
                        dup_stg = df_stg[df_stg["Số ĐT"].str.strip() == ph] if not df_stg.empty else pd.DataFrame()
                        
                        if not dup_crm.empty or not dup_stg.empty:
                            duplicates_removed += 1
                            continue
                            
                        seen_in_batch.add(ph)
                        final_leads.append(lead)
                
                # Hiển thị số liệu lọc
                col_st1, col_st2, col_st3 = st.columns(3)
                col_st1.metric("Tổng dòng đầu vào", total_input)
                col_st2.metric("Số ĐT hợp lệ", valid_count)
                col_st3.metric("Số trùng đã lọc bỏ", duplicates_removed)
                
                if not final_leads:
                    st.warning("⚠️ Sau khi làm sạch và lọc trùng chéo hệ thống, không còn lead mới nào để thêm!")
                else:
                    st.success(f"✔ Tìm thấy **{len(final_leads)}** leads hoàn toàn mới sẵn sàng chia và đưa vào Staging!")
                    
                    # Tiến hành chia lead cho active sale
                    assigned_results = []
                    
                    # Tìm index bắt đầu xoay vòng của round-robin dựa trên lịch sử
                    next_sale_idx = 0
                    if "Round-robin" in bulk_mode and not df_crm.empty:
                        last_sale = df_crm["Sale chăm sóc"].iloc[-1]
                        if last_sale in active_sales_for_bulk:
                            next_sale_idx = (active_sales_for_bulk.index(last_sale) + 1) % len(active_sales_for_bulk)
                            
                    with st.spinner("Đang phân bổ leads cho Sale..."):
                        for i, lead in enumerate(final_leads):
                            if "Ngẫu nhiên" in bulk_mode:
                                assigned_sale = random.choice(active_sales_for_bulk)
                            else:
                                # Chế độ Round-robin xoay vòng đều
                                assigned_sale = active_sales_for_bulk[(next_sale_idx + i) % len(active_sales_for_bulk)]
                                
                            # Chuẩn bị bản ghi lưu
                            new_record = {
                                "Tên khách": lead["Tên khách"],
                                "Số ĐT": lead["Số ĐT"],
                                "Nguồn": bulk_source,
                                "Sale chăm sóc": assigned_sale,
                                "Trạng thái": "Mới",
                                "Ghi chú": f"{bulk_ghichu} [Lô nhập {today_str}]",
                                "Ngày tiếp cận": today_str,
                                "Ngày tương tác cuối": today_str
                            }
                            
                            # Lưu trực tiếp vào tab staging
                            append_staging_row(new_record)
                            assigned_results.append((lead["Tên khách"], lead["Số ĐT"], assigned_sale))
                            
                    # Tự động thực hiện backup dữ liệu hệ thống
                    backup_to_csv()
                    clear_cache()
                    
                    # Báo cáo phân chia leads dạng bảng
                    st.markdown("#### 📋 DANH SÁCH BẢNG PHÂN CHIA LEADS CHO TỪNG SALE:")
                    df_assign_report = pd.DataFrame(assigned_results, columns=["Tên Khách", "Số Điện Thoại", "Sale Đảm Nhận"])
                    st.dataframe(df_assign_report, use_container_width=True)
                    
                    # Bảng tổng hợp số lượng của từng sale
                    st.markdown("#### 📊 TỔNG HỢP SỐ LƯỢNG LEADS PHÂN CHIA:")
                    summary_count = df_assign_report["Sale Đảm Nhận"].value_counts().reset_index()
                    summary_count.columns = ["Tên Sale", "Số Lượng Số Được Chia"]
                    st.table(summary_count)
                    
                    st.success("🎉 Đợt phân phối leads hàng loạt hoàn thành mỹ mãn! Leads đã chuyển vào tab Staging chờ Sale tiếp cận cuộc gọi đầu.")

# ───────────────────────────────────────────────────────────────────────────
# 👥 QUẢN LÝ TEAM & CẤU HÌNH (SETTINGS)
# ───────────────────────────────────────────────────────────────────────────
elif menu == "👥 Quản lý Team & Cấu hình":
    st.markdown('<p class="header-title">👥 CẤU HÌNH HỆ THỐNG & ĐỘI NGŨ</p>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Quản lý danh sách sale kích hoạt, chế độ phân lead tự động mặc định, ngưỡng cảnh báo chăm sóc khách và chuyển leads hàng loạt.</p>', unsafe_allow_html=True)

    tab_config, tab_transfer, tab_project = st.tabs(["⚙️ Cấu Hình Team", "🔄 Chuyển Leads Hàng Loạt", "🏠 Thông Tin Dự Án"])

    # 1. Cấu hình Team & Thông số chung
    with tab_config:
        st.markdown("### ⚙️ CẤU HÌNH THÀNH VIÊN VÀ HỆ THỐNG")
        
        with st.form("sys_config_form"):
            st.markdown("**1. Danh sách đội ngũ Sale hoạt động:**")
            st.caption("Nhập tên các Sale hoạt động trong nhóm, cách nhau bằng dấu phẩy.")
            sale_team_str = st.text_input("Đội ngũ Sale (cách nhau bằng dấu phẩy):", ", ".join(sale_team))
            
            st.markdown("---")
            st.markdown("**2. Bộ chia Leads tự động mặc định:**")
            mode_choice = st.selectbox(
                "Chế độ phân phối lead tự động mặc định:",
                ["roundrobin", "random"],
                index=0 if assign_mode == "roundrobin" else 1,
                format_func=lambda x: "Xoay vòng (Round-robin)" if x == "roundrobin" else "Ngẫu nhiên (Random)"
            )
            
            st.markdown("---")
            st.markdown("**3. Cài đặt Thời gian nhắc nhở (ngày):**")
            new_remind_days = st.number_input("Cảnh báo Quá hạn chăm sóc (remind_days):", min_value=1, max_value=30, value=remind_days)
            new_nurture_days = st.number_input("Ngưỡng giữ mối quan hệ tương tác (nurture_days):", min_value=1, max_value=60, value=nurture_days)
            
            submit_config = st.form_submit_button("💾 Ghi Nhận Thay Đổi Cấu Hình")
            
            if submit_config:
                # Phân tích danh sách sale mới
                new_sales = [s.strip() for s in sale_team_str.split(",") if s.strip()]
                if not new_sales:
                    st.error("Đội ngũ sale không được để trống!")
                else:
                    # Lưu vào config.json
                    cfg["sale_team"] = new_sales
                    cfg["assign_mode"] = mode_choice
                    cfg["remind_days"] = int(new_remind_days)
                    cfg["nurture_days"] = int(new_nurture_days)
                    
                    save_config(cfg)
                    st.success("✔ Đã lưu cấu hình thành công vào config.json! Hệ thống tự động áp dụng thông số mới.")
                    st.rerun()

    # 2. Chuyển leads hàng loạt giữa các sale
    with tab_transfer:
        st.markdown("### 🔄 BỘ CHUYỂN BÀN GIAO LEADS HÀNG LOẠT")
        st.caption("Công cụ đắc lực hỗ trợ Trưởng nhóm khi có nhân viên nghỉ việc hoặc nghỉ phép, cần chuyển nhanh toàn bộ leads đang chăm sóc của một Sale sang Sale khác.")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            transfer_from = st.selectbox("1. Bàn giao từ Sale:", ["--- Chọn Sale bàn giao ---"] + list(sale_team))
        with col_t2:
            transfer_to = st.selectbox("2. Bàn giao cho Sale nhận:", ["--- Chọn Sale đảm nhận ---"] + list(sale_team))
            
        st.markdown("**3. Chọn trạng thái lead sẽ bàn giao:**")
        status_to_transfer = st.multiselect(
            "Chọn trạng thái khách sẽ được chuyển giao:",
            TRANG_THAI_OPTIONS,
            default=["Mới", "Đang chăm sóc", "Hẹn xem đất"]
        )
        
        if st.button("🚀 Thực hiện Bàn giao & Chuyển Leads", use_container_width=True):
            if transfer_from == "--- Chọn Sale bàn giao ---" or transfer_to == "--- Chọn Sale đảm nhận ---":
                st.error("Vui lòng chọn đầy đủ Sale bàn giao và Sale nhận bàn giao!")
            elif transfer_from == transfer_to:
                st.error("Sale bàn giao và Sale nhận không được trùng nhau!")
            elif not status_to_transfer:
                st.error("Vui lòng lựa chọn ít nhất một Trạng thái lead cần chuyển giao!")
            else:
                # Đếm số leads phù hợp
                leads_to_move = df_crm[
                    (df_crm["Sale chăm sóc"] == transfer_from) &
                    (df_crm["Trạng thái"].isin(status_to_transfer))
                ]
                
                if leads_to_move.empty:
                    st.warning(f"⚠️ Không tìm thấy khách hàng nào có trạng thái {status_to_transfer} do sale **{transfer_from}** phụ trách!")
                else:
                    st.success(f"🔍 Tìm thấy **{len(leads_to_move)}** khách hàng phù hợp thỏa mãn điều kiện chuyển giao.")
                    
                    with st.spinner("Đang cập nhật dữ liệu và đồng bộ lên Google Sheets..."):
                        count_moved = 0
                        for idx, row in leads_to_move.iterrows():
                            # Cập nhật sale mới và chèn lịch sử chuyển lead
                            updated_rec = dict(row)
                            updated_rec["Sale chăm sóc"] = transfer_to
                            updated_rec["Ghi chú"] = f"{row['Ghi chú']} (Bàn giao từ {transfer_from} -> {transfer_to} {today_str})".strip()
                            
                            update_row(idx, updated_rec)
                            count_moved += 1
                            
                        # Thực hiện backup
                        backup_to_csv()
                        clear_cache()
                        st.success(f"🎉 Bàn giao thành công! Đã chuyển nhượng toàn bộ **{count_moved}** leads từ **{transfer_from}** sang **{transfer_to}** chăm sóc.")
                        st.rerun()

    # 3. Cấu hình thông tin dự án
    with tab_project:
        st.markdown("### 🏠 THÔNG TIN DỰ ÁN BẤT ĐỘNG SẢN")
        st.caption("Các thông số này sẽ hiển thị bên ngoài báo cáo hoặc các tài liệu hướng dẫn.")
        
        prj = cfg.get("project", {})
        
        with st.form("project_info_form"):
            p_name = st.text_input("Tên dự án:", prj.get("ten_du_an", "Kha Sơn Green Home"))
            p_loc = st.text_input("Địa điểm dự án:", prj.get("khu_vuc", "KCN Phú Bình, Thái Nguyên"))
            p_price = st.text_input("Giá chào bán:", prj.get("gia_tu", "chỉ từ 800 triệu"))
            p_area = st.text_input("Diện tích lô đất mẫu:", prj.get("dien_tich", "80-120m²"))
            p_legal = st.text_input("Pháp lý dự án:", prj.get("phap_ly", "Sổ đỏ lâu dài, pháp lý minh bạch"))
            p_hotline = st.text_input("Hotline trưởng nhóm:", prj.get("hotline", "0368.557.832"))
            
            submit_prj = st.form_submit_button("💾 Ghi Nhận Thông Tin Dự Án")
            
            if submit_prj:
                cfg["project"] = {
                    "ten_du_an": p_name.strip(),
                    "khu_vuc": p_loc.strip(),
                    "gia_tu": p_price.strip(),
                    "dien_tich": p_area.strip(),
                    "phap_ly": p_legal.strip(),
                    "hotline": p_hotline.strip()
                }
                save_config(cfg)
                st.success("✔ Đã cập nhật thành công thông tin dự án vào file config!")
                st.rerun()
