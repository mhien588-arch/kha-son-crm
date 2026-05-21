"""
Công cụ sinh content marketing — Kha Sơn Green Home
Chạy: python content_helper.py
Không cần API — template thực chiến, chạy offline
"""
import os
import json
import random

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = YELLOW = WHITE = RED = MAGENTA = ""
    class Style:
        RESET_ALL = BRIGHT = ""

# ── THÔNG TIN DỰ ÁN — tải từ config.json (chỉnh trong config.json) ────────
def _load_project():
    try:
        _cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        with open(_cfg_path, encoding="utf-8") as f:
            return json.load(f).get("project", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

_proj = _load_project()
DU_AN    = _proj.get("ten_du_an", "Kha Sơn Green Home")
HOTLINE  = _proj.get("hotline", "0368.557.832")
KHU_VUC  = _proj.get("khu_vuc", "KCN Phú Bình, Thái Nguyên")
GIA_TU   = _proj.get("gia_tu", "chỉ từ 800 triệu")
DIEN_TICH = _proj.get("dien_tich", "80–120m²")
PHAP_LY  = _proj.get("phap_ly", "Sổ đỏ lâu dài, pháp lý minh bạch")
# ──────────────────────────────────────────────────────────────────────────

V = dict(du_an=DU_AN, hotline=HOTLINE, khu_vuc=KHU_VUC,
         gia_tu=GIA_TU, dien_tich=DIEN_TICH, phap_ly=PHAP_LY)

# ═══════════════════════════════════════════════════════════════════════════
# PHÍM 1 — KỊCH BẢN TELESALE (gây ấn tượng 30 giây đầu)
# ═══════════════════════════════════════════════════════════════════════════
TELESALE = [
    """\
━━━ KỊCH BẢN TELESALE A — Khơi gợi nhu cầu ━━━

SALE: "Alo! Cho em hỏi đây có phải số anh/chị [Tên] không ạ?"
  → (Khách xác nhận)

SALE: "Dạ, em là [Tên Sale] bên dự án {du_an}. Em gọi vì trước
đây anh/chị có quan tâm đến đất nền khu vực {khu_vuc}.
Không biết hiện tại anh/chị còn đang tìm hiểu không ạ?"
  → (Khách: Có / Đang xem)

SALE: "Dạ tuyệt! Bên em đang có đợt ra hàng đặc biệt —
{dien_tich}, giá {gia_tu} — vị trí đẹp, {phap_ly}.
Anh/chị có thể spare 15 phút cuối tuần này để em
đưa đi xem thực tế không ạ? Bên em có xe đưa đón."

📌 Mục tiêu: Hẹn xem đất — KHÔNG cố chốt qua điện thoại!
📞 Hotline: {hotline}""",

    """\
━━━ KỊCH BẢN TELESALE B — Tạo khan hiếm ━━━

SALE: "Alo, chào anh/chị [Tên] ạ! Em là [Tên Sale]
bên {du_an}. Em xin một phút thôi ạ!"
  → (Khách đồng ý nghe)

SALE: "Dạ, em báo tin này vì anh/chị nằm trong danh sách
khách hàng quan tâm của bên em — hôm qua vừa có khách
đặt cọc nền sát nền anh/chị đang để ý. Hiện chỉ còn
3 nền đẹp nhất, em muốn ưu tiên cho anh/chị trước."
  → (Khách: Giá bao nhiêu? / Nền nào?)

SALE: "Dạ đó là điều em muốn tư vấn trực tiếp cho anh/chị.
Anh/chị rảnh ngày [Thứ X] không? Em sẽ mang đầy đủ
bảng giá, pháp lý, sơ đồ nền ra cho anh/chị xem tận tay."

📌 Khóa hẹn: Đưa ra 2 thời gian cụ thể để khách chọn 1!
📞 Hotline: {hotline}""",

    """\
━━━ KỊCH BẢN TELESALE C — Khai thác đầu tư ━━━

SALE: "Anh/chị [Tên] ơi! Em [Tên Sale] đây ạ. Anh/chị
đang có kế hoạch đầu tư bất động sản trong năm nay không?"
  → (Khách: Có đang xem xét)

SALE: "Dạ vậy thì hôm nay em gọi đúng người rồi! Em đang
phụ trách dự án {du_an} tại {khu_vuc} — đây là
khu vực có tốc độ tăng giá cao nhất tỉnh, 25–30%/năm,
nhờ 5 khu công nghiệp lớn đang đổ vốn FDI về.
Giá hiện tại {gia_tu}, {phap_ly}."
  → (Khách hỏi thêm)

SALE: "Để em nói chính xác nhất, anh/chị có thể ra xem
thực địa không? Em cam kết anh/chị sẽ hiểu ngay tại
sao nhà đầu tư đang đổ xô về đây mua. Mình hẹn
[Thứ X] lúc [giờ] nhé anh/chị?"

📌 Luôn kết bằng câu hỏi đóng có 2 lựa chọn thời gian!
📞 Hotline: {hotline}""",
]

# ═══════════════════════════════════════════════════════════════════════════
# PHÍM 2 — BÀI ĐĂNG FACEBOOK
# ═══════════════════════════════════════════════════════════════════════════
FACEBOOK = [
    """\
🏡 ĐẤT NỀN {du_an} — {gia_tu}/nền!

✅ Diện tích: {dien_tich}
✅ Vị trí: ngay {khu_vuc}
✅ {phap_ly}
✅ Hạ tầng hoàn thiện, điện nước đầy đủ, xây được ngay

💥 Quỹ đất có hạn — Nền đẹp đang hết dần!
📞 Inbox hoặc gọi ngay: {hotline}

#datnen #{du_an} #ThaiNguyen #KCNPhuBinh #dautu2026""",

    """\
📊 TẠI SAO ĐẤT NỀN {khu_vuc} LÀ LỰA CHỌN SỐ 1 NĂM 2026?

🏭 50.000+ công nhân cần chỗ ở — cầu nhà ở tăng mạnh
🚗 30 phút từ Hà Nội qua cao tốc
📈 Giá đất tăng 25–35%/năm trong 3 năm qua
🏗️ Hạ tầng quốc gia đang đổ về khu vực này

Dự án {du_an}:
→ Giá: {gia_tu}
→ Pháp lý: {phap_ly}
→ Diện tích: {dien_tich}

💡 Mua đất hôm nay = tích sản cho 10 năm tới
📞 Tư vấn miễn phí: {hotline}""",

    """\
💬 KHÁCH HÀNG NÓI GÌ VỀ {du_an}?

"Ban đầu tôi chỉ xem cho biết, nhưng khi ra thực địa thấy
ngay cạnh KCN, nhà máy đang xây la liệt — tôi quyết cọc
luôn hôm đó. Sổ đỏ về trong 2 tháng, đúng như cam kết."

— Anh Minh Đức, nhà đầu tư từ Hà Nội

Bạn có muốn tận mắt xem không?
👉 Liên hệ {hotline} — Có xe đưa đón miễn phí
🏡 {du_an} — {khu_vuc}""",

    """\
🔥 CHỈ CÒN VÀI NỀN CUỐI — {du_an}

Không phải quảng cáo câu view — đây là sự thật:
→ Dự án mở bán 3 tháng
→ 70% nền đã có chủ
→ Các nền còn lại đều là vị trí đẹp

Nếu anh/chị đang tìm đất nền tỉnh:
✔ Giá tốt: {gia_tu}
✔ Pháp lý: {phap_ly}
✔ Vị trí: {khu_vuc}

⏰ Đừng để hỏi mua thì hết rồi!
📞 {hotline} — {du_an}""",

    """\
📍 VỊ TRÍ VÀNG — ĐẤT NỀN {du_an}

🏭 Ngay cạnh KCN Phú Bình — khu công nghiệp lớn nhất Thái Nguyên
🚗 Kết nối Hà Nội chỉ 30 phút (cao tốc)
🏪 Shophouse, trường học, bệnh viện cách 5 phút

Mua để ở hay đầu tư đều sinh lời!
→ Giá: {gia_tu} — {phap_ly}
→ Diện tích linh hoạt: {dien_tich}

📞 Hotline: {hotline}
Tag bạn bè cùng xem! 👇""",

    """\
💰 ĐẦU TƯ THÔNG MINH = ĐẤT NỀN GẦN KCN

Công thức đơn giản của nhà đầu tư kinh nghiệm:
📌 Mua đất gần KCN đang phát triển
📌 Pháp lý sạch, có sổ đỏ
📌 Hạ tầng đồng bộ, xây được ngay
📌 Giá vào đúng lúc thị trường chưa sôi

→ {du_an} đáp ứng đủ 4 tiêu chí này!
→ Giá: {gia_tu} | Vị trí: {khu_vuc}

📲 Để lại SĐT — em tư vấn trong 30 phút!
☎️ {hotline}""",
]

# ═══════════════════════════════════════════════════════════════════════════
# PHÍM 3 — TIN NHẮN ZALO CHĂM SÓC KHÁCH CŨ
# ═══════════════════════════════════════════════════════════════════════════
ZALO_CU = [
    """\
━━━ MẪU ZALO A — Nhắc sau khi đi xem đất ━━━

Gửi: [1–2 ngày sau khi khách xem thực địa]

"Chào anh/chị [Tên] ạ!

Em [Tên Sale] đây. Hôm đó mình đi xem đất em cảm ơn
anh/chị đã dành thời gian nha.

Không biết sau khi tham quan, anh/chị có thêm băn khoăn
gì không ạ? Em luôn sẵn sàng giải đáp thêm hoặc sắp xếp
cho anh/chị xem lần 2 nếu cần.

Anh/chị cứ nhắn em nhé! 🙏"

📌 TIP: Đừng hỏi thẳng "anh/chị có mua không" — tạo không
gian để khách tự mở lòng chia sẻ vướng mắc.""",

    """\
━━━ MẪU ZALO B — Cập nhật tin tức dự án ━━━

Gửi: [Khi có tin tức mới về dự án hoặc khu vực]

"Chào anh/chị [Tên]!

Em có tin vui muốn báo anh/chị:

🏗️ Tuần này bên em vừa hoàn thiện thêm [đường nội khu /
hạ tầng điện nước / cổng dự án] — dự án đang tiến độ
rất đẹp.

Anh/chị muốn em gửi ảnh/video thực tế mới nhất không ạ?

Chúc anh/chị ngày tốt lành! 😊"

📌 TIP: Kèm 1-2 ảnh thực tế mới nhất — tăng độ tin cậy.""",

    """\
━━━ MẪU ZALO C — Tạo urgency (giá sắp tăng) ━━━

Gửi: [Khi gần có đợt điều chỉnh giá hoặc hết hàng]

"Anh/chị [Tên] ơi, em [Tên Sale] đây!

Em muốn thông báo với anh/chị: Bên em dự kiến
điều chỉnh bảng giá vào [ngày cụ thể] do chi phí
hạ tầng tăng và nhu cầu thị trường đang rất cao.

Hiện tại còn [X] nền với mức giá cũ — anh/chị có muốn
em giữ ưu tiên 1 nền đẹp cho anh/chị không?

Chỉ cần anh/chị xác nhận, em book ngay ạ! 🙏"

📌 TIP: Thông tin phải THẬT — đừng tạo urgency giả.
Khách phát hiện 1 lần là mất tin tưởng mãi.""",
]


def print_content(title, content, color=Fore.WHITE):
    print(Fore.GREEN + f"\n{'═'*60}")
    print(Fore.GREEN + f"  {title}")
    print(Fore.GREEN + f"{'═'*60}\n")
    rendered = content.format(**V)
    print(color + rendered)
    print()


def menu_telesale():
    script = random.choice(TELESALE)
    print_content("KỊCH BẢN TELESALE — GÂY ẤN TƯỢNG 30 GIÂY ĐẦU",
                  script, Fore.YELLOW)
    print(Fore.CYAN + "  📋 Copy kịch bản, luyện 5 phút trước khi gọi!")
    input("\n  Nhấn Enter để tiếp tục...")


def menu_facebook():
    post = random.choice(FACEBOOK)
    print_content("BÀI ĐĂNG FACEBOOK — COPY & ĐĂNG NGAY",
                  post, Fore.WHITE)
    print(Fore.CYAN + "  📋 Copy bài, thêm 2–3 ảnh thực tế dự án, đăng ngay!")
    input("\n  Nhấn Enter để tiếp tục...")


def menu_zalo():
    msg = random.choice(ZALO_CU)
    print_content("TIN NHẮN ZALO — CHĂM SÓC KHÁCH CŨ",
                  msg, Fore.WHITE)
    print(Fore.CYAN + "  📋 Điền tên khách, tên sale, copy & gửi ngay!")
    input("\n  Nhấn Enter để tiếp tục...")


def main():
    while True:
        print(Fore.CYAN + "\n" + "═" * 52)
        print(Fore.CYAN + "  CONTENT HELPER — KHA SƠN GREEN HOME")
        print(Fore.CYAN + "═" * 52)
        print(f"\n  [{Fore.YELLOW}1{Fore.CYAN}] Kịch bản TELESALE   — gây ấn tượng 30 giây")
        print(f"  [{Fore.YELLOW}2{Fore.CYAN}] Bài đăng FACEBOOK   — thu hút tương tác")
        print(f"  [{Fore.YELLOW}3{Fore.CYAN}] Tin nhắn ZALO        — chăm sóc khách cũ")
        print(f"  [{Fore.YELLOW}4{Fore.CYAN}] Bộ công cụ TƯ VẤN KHÁCH HÀNG (YAML & Xử lý từ chối) ✨")
        print(f"  [{Fore.WHITE}0{Fore.CYAN}] Thoát\n")

        choice = input(Fore.WHITE + "  Chọn: ").strip()
        if choice == "1":
            menu_telesale()
        elif choice == "2":
            menu_facebook()
        elif choice == "3":
            menu_zalo()
        elif choice == "4":
            try:
                from consultation.cli import display_interactive_cli
                display_interactive_cli()
            except Exception as e:
                print(f"Lỗi khởi chạy bộ công cụ tư vấn: {e}")
                input("\n  Nhấn Enter để quay lại...")
        elif choice == "0":
            print("Chúc sale thành công! 💪")
            break
        else:
            print(Fore.YELLOW + "  Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
