# HỆ THỐNG VẬN HÀNH — KHA SƠN GREEN HOME
> Dự án: Đất nền KCN Phú Bình, Thái Nguyên | Cập nhật: 21/05/2026 (phiên 24)

---

## TEAM OVERVIEW

**Đội ngũ 6 chiến binh Sale cốt cán**

| # | Tên | Vai trò | Nhiệm vụ chính |
|---|-----|---------|----------------|
| 1 | Hiển | Sale Leader | Dẫn dắt team, chốt deal lớn, báo cáo BGĐ |
| 2 | Đức | Sale Senior | Chăm sóc leads nóng, đưa khách đi xem đất |
| 3 | Chị Dung | Sale Senior | Chăm sóc leads nóng, telesale cold-call |
| 4 | Tuấn Anh | Sale Junior | Tìm kiếm leads mới, chăm sóc leads lạnh |
| 5 | Nam | Sale Junior | Tìm kiếm leads mới, hỗ trợ content FB/Zalo |
| 6 | Chương | Sale Junior | Tìm kiếm leads mới, telesale cold-call |

> Thêm/bớt thành viên: dùng **menu [7] trong tracker.py** → [a] Thêm / [c] Vô hiệu hóa → tự động cập nhật `config.json` (không cần sửa code)

**Mục tiêu tối cao:** Tối ưu năng suất cá nhân — bám sát từng lead để tăng tỷ lệ chốt cọc đất nền.

**KPI tháng:**
- Số lead mới/tuần: ≥ 20
- Lượt xem đất/tuần: ≥ 5
- Số cọc/tháng: ≥ 3
- CPL (Cost Per Lead) từ Ads: < 100.000đ

---

## TRẠNG THÁI SCRIPTS — CẬP NHẬT 21/05/2026 (phiên 25)

| Script | Trạng thái | Nguồn dữ liệu |
|--------|-----------|---------------|
| **config.json** | ✅ **Phiên 16** — thêm `nurture_days: 14` — ngưỡng ngày nhắc giữ tương tác khách "Không còn nhu cầu" | — |
| **Google Sheets CRM** | ✅ **Phiên 26** — 75 leads (khôi phục 11 leads bị mất do bug `append_row()`) | — |
| tracker.py | ✅ **Phiên 24** — thêm `_show_telesale_banner()` + menu `[T]` Xử lý DATA TELESALE (transfer leads đã tích ✓ vào CRM); **Phiên 19**: fix bug row-index | **Google Sheets** + config.json |
| sheets_connector.py | ✅ **Phiên 26** — Fix 6 bug nghiêm trọng: `append_row()` `if v` filter gây ghi đè dữ liệu; `load_data()` + `load_telesale_data()` filter cả 2 cột; `transfer_telesale_checked()` tách retry; batch write telesale; expand tab 1500 rows; **Phiên 24**: 4 hàm TELESALE; **Phiên 23**: `_get_credentials()` | Google Sheets API |
| daily_report.py | ✅ **Phiên 22** — tự động gọi `backup_to_csv()` ngay khi khởi chạy báo cáo | **Google Sheets** + config.json |
| weekly_report.py | ✅ **Tạo mới phiên 11** — Báo cáo tuần + phân tích nguồn lead → `bao_cao_tuan_W{N}_2026.txt` | **Google Sheets** + config.json |
| Bao Cao Tuan.bat | ✅ **Tạo mới phiên 11** — double-click để chạy weekly_report.py | — |
| nhac_sang.py | ✅ **Phiên 22** — tự động gọi `backup_to_csv()` + nhắc nhở quá hạn chăm sóc sáng | **Google Sheets** + config.json |
| setup_task_scheduler.py | ✅ **Tạo mới phiên 12** — chạy 1 lần (Admin) để đăng ký Task Scheduler Windows | — |
| Nhac Sang.bat | ✅ **Tạo mới phiên 12** — double-click để test nhac_sang.py thủ công | — |
| cleanup_reports.py | ✅ **Tạo mới phiên 12** — zip báo cáo tháng cũ vào archive/, giữ tháng hiện tại | — |
| Don Dep Bao Cao.bat | ✅ **Tạo mới phiên 12** — double-click để chạy cleanup_reports.py | — |
| dashboard.py | ✅ **Phiên 25** — thêm Tab "💡 Kịch Bản Tư Vấn" (dropdown lọc theo Sale và mẫu kịch bản, render trực quan, copy 1 chạm); **Phiên 24**: tab Data Telesale | **Google Sheets** + config.json |
| content_helper.py | ✅ **Phiên 25** — bổ sung tùy chọn `[4]` liên kết khởi chạy Bộ kịch bản tư vấn mới ngay trong menu console | **config.json** + consultation |
| consultation/ | ✅ **Tạo mới phiên 25** — gói quản lý kịch bản mẫu câu độc lập (templates.yaml, loader.py, cli.py) | templates.yaml |
| Tư Vấn Mẫu Câu.bat | ✅ **Tạo mới phiên 25** — phím tắt chạy nhanh CLI kịch bản tư vấn dạng tương tác trên Windows | — |
| Mo Dashboard.bat | ✅ **Tạo mới phiên 22** — chạy Streamlit trên môi trường python3.13 | — |
| Viet Content.bat | ✅ **Phiên 25** — chạy content_helper.py và hỗ trợ gọi nhanh bộ kịch bản tư vấn | — |
| C:\Users\PC\Desktop\Mo CRM Kha Son.bat | ✅ **Tạo mới phiên 22** — Launcher thông minh ngoài Desktop, kiểm tra xung đột cổng, khởi động/mở trình duyệt nhanh | — |
| **GitHub repo** | ✅ **Phiên 23** — `github.com/mhien588-arch/kha-son-crm` (public) — nguồn deploy tự động cho Streamlit Cloud | — |
| **Streamlit Community Cloud** | ✅ **Phiên 23** — App live tại `https://kha-son-crm-k3tfrnb488ckvq4nb5xsm7.streamlit.app` — team truy cập từ điện thoại, thêm vào màn hình chính như app thật | Cloud |
| fix_and_validate_crm.py | ✅ **Phiên 16** — cài date picker (calendar) cho cột G "Ngày tiếp cận" và H "Ngày tương tác cuối", rows 2–300 | Google Sheets API |
| **Huong_Dan_Truong_Nhom.docx** | ✅ **Tạo mới phiên 13** — hướng dẫn vận hành tổng hợp 10 chương dành cho Hiển | — |
| **Huong_Dan_Nhan_Su.docx** | ✅ **Tạo mới phiên 13** — hướng dẫn nhân sự mới 9 chương (trạng thái, quy trình, KPI, kịch bản) | — |
| make_huong_dan_v2.py | ✅ **Tạo mới phiên 13** — script python-docx tạo lại 2 file .docx bất cứ lúc nào | — |
| **Huong_Dan_Toan_Dien_CRM.docx** | ✅ **Cập nhật phiên 21** — 8 phần, bổ sung lỗi thứ 11 (TypeError int64) vào Phần 5; cập nhật Phần 7 quy tắc bất biến | — |
| **Huong_Dan_Toan_Dien_CRM.pdf** | ✅ **Cập nhật phiên 21** — bản PDF mới nhất sau khi thêm lỗi int64 | — |
| ~~Huong_Dan_Van_Hanh_CRM.docx~~ | ❌ **Xóa phiên 13** — thay bằng 2 file mới ở trên | — |
| ~~make_huong_dan.py~~ | ❌ **Xóa phiên 13** — thay bằng make_huong_dan_v2.py | — |
| content_helper.py | ✅ Phiên 7 — đọc project variables (ten_du_an, hotline, gia_tu...) từ config | Offline + config.json |
| lich_ngay.py | ✅ Phiên 7 — đọc KPI từ config | — |
| import_khach_cu.py | ✅ Tạo mới phiên 4 — nhập hàng loạt từ sheet ngoài vào CRM | Google Sheets API |
| fix_table_layout.py | ✅ Tạo mới phiên 4 — sắp xếp lại dữ liệu vào đúng bảng định dạng | Google Sheets API |
| format_sheet.py | ✅ Phiên 5 — định dạng xanh rừng (đã thay bởi apply_format_crm.py ở phiên 6) | Google Sheets API |
| reimport_with_dates.py | ✅ Tạo mới phiên 5 — re-import từ sheet nguồn mới với date forward-fill | Google Sheets API |
| check_data.py | ✅ Tạo mới phiên 5 — kiểm tra chất lượng data (SĐT, tên, sale) | Google Sheets API |
| fix_sale_name.py | ✅ Tạo mới phiên 5 — đổi "TA" → "Tuấn Anh" trong cột Sale | Google Sheets API |
| format_ban2_daks.py | ✅ Tạo mới phiên 6 — tạo tab mới với định dạng navy + user guide (script tái dùng được) | Google Sheets API |
| apply_format_crm.py | ✅ Tạo mới phiên 6 — áp định dạng navy mới + User Guide I56:L90 vào CRM tab chính | Google Sheets API |
| data/leads.csv | ⚠ Không còn dùng — chỉ giữ tham khảo | — |
| Mo Tracker.bat | ✅ Hiển double-click để mở (chỉ Hiển dùng .bat để quản lý) | — |
| Bao Cao Ngay.bat | ✅ Hiển double-click để mở | — |
| Viet Content.bat | ✅ Hiển double-click để mở | — |
| Lich Ngay.bat | ✅ Tạo mới phiên 3 — Hiển double-click để mở | — |

**Claude Code Skills (slash commands) — Tạo mới phiên 3:**

| Skill | Lệnh gõ | Tác dụng |
|-------|---------|----------|
| .claude/commands/lich-ngay.md | `/lich-ngay` | Hiển thị checklist 6 việc theo buổi, chạy script phù hợp |
| .claude/commands/chay-he-thong.md | `/chay-he-thong` | Mở tracker.py với hướng dẫn menu [1]–[6] |
| .claude/commands/bao-cao.md | `/bao-cao` | Chạy daily_report.py + giải thích từng chỉ số KPI |
| .claude/commands/kiem-tra-sheet.md | `/kiem-tra-sheet` | Kiểm tra kết nối Sheet + xem danh sách khách hiện tại |
| .claude/commands/xoa-demo.md | `/xoa-demo` | Xóa dữ liệu demo (có xác nhận yes/no trước khi xóa) |

**Cài thư viện một lần (nếu chưa cài):**
```
pip install pandas colorama gspread google-auth
```

**Google Sheets (nguồn dữ liệu thật):**
- Sheet ID: `1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA`
- **Tab 1:** `KhaSonGreenHome_CRM` — dữ liệu CRM chính, định dạng navy, User Guide I56:L90
- **Tab 2:** `SỐ MỚI KS` — staging inbox, tạo tự động lần đầu khi chạy tracker.py (phiên 9)
- **Tab 3:** `DATA TELESALE` — cold-call inbox, header cam #E65100, checkbox cột I, 1111 số đã import (phiên 24); tạo tự động khi chạy `ensure_telesale_tab()`
- Credentials: `data/google_creds.json` (Service Account — KHÔNG xóa, KHÔNG chia sẻ)
- Trạng thái hiện tại: **75 khách hàng CRM thật + ~1100 số DATA TELESALE — định dạng navy chuyên nghiệp** (75 sau khi phục hồi 11 leads mất do bug phiên 26)
- Link CRM chính: https://docs.google.com/spreadsheets/d/1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA/edit?gid=1033447423#gid=1033447423

---

## SCRIPTS VẬN HÀNH

### tracker.py — Quản Lý Khách Hàng
```
python tracker.py
```

**Tính năng:**
- `[1]` Xem tất cả khách hàng (bảng màu, cảnh báo quá hạn)
- `[2]` Lọc khách theo sale phụ trách
- `[3]` Kiểm tra khách bị quên > 3 ngày → in tên sale + danh sách đích danh
- `[4]` Thêm lead mới → validate SĐT → kiểm tra trùng → vào tab **SỐ MỚI KS** (staging)
- `[5]` Cập nhật trạng thái lead
- `[6]` Làm mới dữ liệu từ Sheet + tự động chuyển lead đã tích ✓ từ SỐ MỚI KS vào CRM
- `[7]` Quản lý team sale → `[a]` Thêm thành viên | `[c]` Vô hiệu hóa thành viên
- `[8]` Tìm kiếm theo SĐT (hỗ trợ tìm một phần) → xem thông tin + cập nhật ngay
- `[9]` Xử lý SỐ MỚI KS → chuyển lead đã tích ✓ vào CRM chính (auto in đậm dòng mới)
- `[T]` Xử lý DATA TELESALE → chuyển lead đã tích ✓ từ tab "DATA TELESALE" vào CRM với trạng thái "Đang chăm sóc"

**Luồng lead mới (phiên 9):**
1. Nhập `[4]` → Validate SĐT (phải bắt đầu `0`, đủ 10 số) → Kiểm tra trùng CRM + staging
2. Lead vào tab **SỐ MỚI KS** (checkbox FALSE, chờ xử lý)
3. Sale mở Google Sheets → tích ✓ checkbox sau khi liên hệ lần đầu
4. Chạy `[9]` hoặc khởi động lại tracker → lead tự động chuyển vào CRM + in đậm

**File dữ liệu:** Google Sheets → tab `KhaSonGreenHome_CRM` + tab `SỐ MỚI KS` (staging)

**Trạng thái khách hàng hợp lệ:**
- `Mới` — Vừa có lead, chưa liên hệ
- `Đang chăm sóc` — Đã liên hệ, đang theo dõi
- `Hẹn xem đất` — Đã hẹn lịch đi xem
- `Chốt cọc` — Đã đặt cọc (THẮNG)
- `Từ chối` — Không mua (thua)

**Màu sắc bảng:**
- Đỏ = quá 3 ngày chưa liên hệ
- Xanh lá = Chốt cọc
- Xám = Từ chối / Chốt cọc (xong)

---

### daily_report.py — Báo Cáo Cuối Ngày
```
python daily_report.py
```

**Output 3 block:**
1. Tổng quan: Lead mới hôm nay | Đang chăm | Chuyển đổi hôm nay
2. Bảng từng sale: Đang giữ | Hẹn/Chốt hôm nay | Quá hạn
3. Tuyên dương Best Today + Cảnh báo sale nhiều khách quá hạn

**File dữ liệu:** Google Sheets → tab `KhaSonGreenHome_CRM` (không cần BaoCaoKinhDoanh.xlsx, không cần leads.csv)
**Lưu báo cáo:** `bao_cao_YYYY-MM-DD.txt`

---

### content_helper.py — Trợ Lý Viết Content
```
python content_helper.py
```

- `[1]` Kịch bản TELESALE — random 1 trong 3 kịch bản (A/B/C)
- `[2]` Bài đăng FACEBOOK — random 1 trong 6 mẫu
- `[3]` Tin nhắn ZALO — random 1 trong 3 mẫu chăm sóc khách cũ

**Không cần API, chạy offline hoàn toàn.**

---

## QUY TẮC VẬN HÀNH HÀNG NGÀY

> Sale không cần terminal — chỉ cần double-click file .bat trên Desktop

### Buổi sáng (8:00 — 15 phút)
1. Double-click **Mo Tracker.bat** → `[3]` Kiểm tra khách bị quên → Gọi ngay sale có tên trong cảnh báo
2. Kiểm tra Ads Manager: Chi phí | Số lead | CPL
3. `[4]` Thêm lead mới từ Facebook (hệ thống tự chia sale, tự lưu Google Sheets)

### Buổi chiều (17:00 — 10 phút)
1. Double-click **Mo Tracker.bat** → `[5]` Cập nhật trạng thái khách hàng

### Cuối ngày (18:00 — 5 phút)
1. Double-click **Bao Cao Ngay.bat** → Xem bảng KPI
2. Chụp màn hình gửi group Zalo team

---

## QUY TẮC CHĂM SÓC KHÁCH HÀNG

| Tình huống | Hành động |
|-----------|----------|
| Lead mới (< 1 giờ) | Gọi điện NGAY, không để qua ngày |
| Chưa nghe máy | Nhắn Zalo, gọi lại sau 2 tiếng |
| Hứa gọi lại | Đặt nhắc nhở trong tracker |
| Chưa liên hệ > 3 ngày | Tracker tự nhắc — ưu tiên xử lý |
| Đã xem đất > 3 ngày | Hỏi thăm, gửi thêm thông tin pháp lý |
| Từ chối | Ghi lý do, hỏi thăm sau 30 ngày |

---

## TÀI NGUYÊN

- Quy trình chạy Ads Facebook: `docs/QuyTrinhAds.txt`
- **Dữ liệu leads: Google Sheets** ← nguồn chính từ phiên 2 trở đi
- Credentials Google: `data/google_creds.json` ← KHÔNG xóa, KHÔNG đổi tên
- Báo cáo ngày: `bao_cao_YYYY-MM-DD.txt`
- **Hướng dẫn trưởng nhóm:** `Huong_Dan_Truong_Nhom.docx` — vận hành tổng hợp 10 chương
- **Hướng dẫn nhân sự:** `Huong_Dan_Nhan_Su.docx` — onboarding nhân viên mới 9 chương
- (Tham khảo cũ — không dùng nữa): `data/leads.csv`, `data/BaoCaoKinhDoanh.xlsx`

---

## THÔNG TIN DỰ ÁN

| Hạng mục | Chi tiết |
|----------|---------|
| Tên dự án | Kha Sơn Green Home |
| Vị trí | Gần KCN Phú Bình, Thái Nguyên |
| Loại sản phẩm | Đất nền |
| Hotline | 0368.557.832 |
| Fanpage | Kha Sơn Green Home |
| Tài khoản Ads | 554148377448431 |

---

## NHẬT KÝ PHÁT TRIỂN

### Phiên 1 — 16/05/2026 — Viết lại toàn bộ hệ thống (CSV)

**Đã hoàn thành:**
- Cấu trúc lại thư mục `D:\QuanLyBKD2\` (thêm `data/`, `docs/`)
- Viết lại `tracker.py`: chuyển từ Excel → CSV, thêm round-robin chia lead, cảnh báo đích danh từng sale
- Viết lại `daily_report.py`: đọc hoàn toàn từ `leads.csv`, 3 block báo cáo tự động
- Viết lại `content_helper.py`: 3 phím trực tiếp, bổ sung 3 kịch bản telesale mới
- Tạo `data/leads.csv` với 5 dòng dữ liệu demo

**Quyết định kiến trúc phiên 1:**

| Quyết định | Lý do |
|-----------|-------|
| Dùng CSV thay Excel | Không cần openpyxl, dễ đọc/sửa bằng tay, đủ cho quy mô nhỏ |
| Một nguồn dữ liệu duy nhất (leads.csv) | Tránh nhập tay 2 lần, daily_report tự tính từ CSV |
| Round-robin dựa vào dòng cuối CSV | Đơn giản, không cần DB, đủ công bằng với team nhỏ |
| Kịch bản telesale random | Sale không bị nhàm, mỗi lần bấm ra script khác nhau |
| Không dùng AI API trong content_helper | Chạy offline, không mất phí, team dùng được ngay |

---

### Phiên 2 — 16/05/2026 — Chuyển sang Google Sheets (đã hoàn thành & xác minh)

**Vấn đề phát sinh sau phiên 1:**
- Sale không biết dùng terminal / Claude Code → không thể nhập liệu
- CSV chỉ tồn tại trên 1 máy → team không chia sẻ được dữ liệu real-time
- Cần hệ sinh thái Google để cả team cùng truy cập từ điện thoại / máy tính bất kỳ

**Đã hoàn thành:**
- Tạo `sheets_connector.py` — module kết nối Google Sheets API trung tâm, dùng chung cho mọi script
- Sửa `tracker.py` — xóa toàn bộ logic CSV, thay bằng `append_row()` / `update_row()` / `load_data()` từ sheets_connector; thêm menu [6] Làm mới từ Sheet
- Sửa `daily_report.py` — xóa CSV load, thay bằng `from sheets_connector import load_data`
- Tạo `Mo Tracker.bat` — sale double-click, không cần terminal
- Tạo `Bao Cao Ngay.bat` — sale double-click, không cần terminal
- Tạo `Viet Content.bat` — sale double-click, không cần terminal
- **Xác minh thực tế:** `python sheets_connector.py` → kết nối thành công, tải 5 khách; `python daily_report.py` → báo cáo in đúng, file .txt lưu thành công

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `WorksheetNotFound: Khach_Hang` | Tên tab thực tế khác tên khai báo | Liệt kê tất cả worksheets → phát hiện tab thật là `KhaSonGreenHome_CRM` |
| `UnicodeEncodeError` khi chạy trong PowerShell | Windows terminal mặc định CP1252 | Thêm `$env:PYTHONIOENCODING = "utf-8"` khi chạy qua terminal (bat files dùng `chcp 65001` nên không bị lỗi này) |

**Quyết định kiến trúc phiên 2:**

| Quyết định | Lý do |
|-----------|-------|
| Google Sheets thay CSV | Sale nhập từ điện thoại / bất kỳ máy nào; dữ liệu real-time cho cả team |
| Service Account (không phải OAuth) | Không cần login thủ công mỗi lần, script chạy tự động hoàn toàn |
| Module `sheets_connector.py` tách riêng | Không lặp code kết nối ở tracker và daily_report; đổi Sheet ID một chỗ là xong |
| `.bat` file double-click | Sale không cần biết Python/terminal; giảm rào cản vận hành xuống 0 |
| Row index = pandas_idx + 2 | Row 1 là header trong Sheet, data bắt đầu từ row 2, pandas bắt đầu từ 0 |

---

### Phiên 4 — 16/05/2026 — Nhập Dữ Liệu Khách Hàng Cũ & Sửa Layout Bảng

**Vấn đề phát sinh sau phiên 3:**
- Có sẵn 57 khách hàng cũ trong sheet riêng (`Khach_Hang_Ban2_Updated`, ID: `12zUF0GNXB96eHyoW6XcxWmVqyOdwrYREWI5EPsuYIXw`) cần chuyển sang CRM chính
- Sau khi nhập, dữ liệu bị đẩy xuống row 27 thay vì row 2 do user đã tạo sẵn 25 dòng trống có định dạng (bảng thủ công) trong CRM sheet
- 5 dòng demo từ phiên cũ vẫn còn dù tưởng đã xóa

**Đã hoàn thành:**
- Tạo `import_khach_cu.py` — script nhập hàng loạt từ bất kỳ sheet ngoài vào CRM:
  - Tự động tìm worksheet theo gid (không phụ thuộc tên tab)
  - Column mapping thông minh: nhận diện ~25 tên cột tiếng Việt khác nhau (VD: "Số điện thoại" / "SĐT" / "Phone" → đều map vào "Số ĐT")
  - Bỏ qua dòng trống và dòng thiếu cả tên lẫn SĐT
  - Trạng thái không hợp lệ → tự đặt về "Mới"; Nguồn trống → tự điền "Khách cũ"
  - Ghi theo batch 50 dòng để tránh timeout
- Tạo `fix_table_layout.py` — sắp xếp lại dữ liệu về đúng vị trí trong bảng:
  - Đọc toàn bộ raw data, lọc dòng trống + demo, giữ lại khách thật
  - Ghi khách thật vào A2:H(N) — đúng ngay từ row 2
  - Dùng `ws.batch_clear()` (xóa value, **giữ nguyên định dạng/màu/border**)
  - Xóa vùng thừa phía dưới sau khi ghi xong
- **Kết quả sau phiên 4:** 52 khách thật trong bảng (rows 2–53), 0 dòng trống, 0 demo, định dạng bảng nguyên vẹn

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `APIError 403: The caller does not have permission` | Service Account chưa được chia sẻ quyền sheet nguồn | Vào sheet nguồn → Chia sẻ → thêm email `quanlybkd2-bot@brave-airship-495710-i4.iam.gserviceaccount.com` với quyền Viewer |
| Dữ liệu nhập vào row 27 thay vì row 2 | Sheet CRM đã có sẵn 25 dòng trống có định dạng; `append_rows()` chèn sau hết dòng trống | Dùng `fix_table_layout.py`: đọc raw → lọc → ghi đè A2:H(N) |
| 5 demo vẫn còn dù tưởng đã xóa phiên 3 | Phiên 3 xóa demo trong sheet cũ, nhưng khi nhập lại từ sheet nguồn thì sheet nguồn vẫn có demo | `fix_table_layout.py` lọc hardcode DEMO_NAMES khi ghi lại |

**Quyết định kiến trúc phiên 4:**

| Quyết định | Lý do |
|-----------|-------|
| `ws.batch_clear()` thay vì `ws.clear()` | `ws.clear()` xóa cả định dạng (màu, border) — `batch_clear()` chỉ xóa value, giữ nguyên formatting |
| Column mapping dạng dict (không dùng tên cột cứng) | Sheet nguồn có thể có tên cột khác nhau; mapping linh hoạt giúp script dùng lại được cho nhiều sheet nguồn khác |
| Lọc DEMO_NAMES trong fix_table_layout.py | Đảm bảo demo không thể lọt vào kể cả khi script nhập lại từ sheet nguồn có chứa demo |
| Ghi batch 50 dòng trong import_khach_cu.py | Google Sheets API có giới hạn rate; batch nhỏ tránh timeout với dataset lớn hơn sau này |

---

### Phiên 3 — 16/05/2026 — Tạo Skills & Xóa Dữ Liệu Demo

**Vấn đề phát sinh sau phiên 2:**
- Cần một điểm truy cập duy nhất để biết hôm nay cần làm gì (thay vì nhớ từng lệnh riêng lẻ)
- Cần các lệnh tắt nhanh trong Claude Code để không phải gõ lại quy trình mỗi lần
- Dữ liệu demo vẫn còn trong Sheet, cần xóa trước khi dùng thật

**Đã hoàn thành:**
- Tạo `lich_ngay.py` — script Python tương tác: hiển thị checklist 6 việc theo buổi, launch script phù hợp, lưu tiến độ vào `tien_do_YYYY-MM-DD.txt`
- Tạo `Lich Ngay.bat` — launcher double-click (cùng pattern với 3 .bat hiện có)
- Tạo 5 Claude Code skills trong `.claude/commands/`:
  - `lich-ngay.md` → `/lich-ngay`: checklist 6 việc theo buổi sáng/chiều/tối
  - `chay-he-thong.md` → `/chay-he-thong`: mở tracker với hướng dẫn menu
  - `bao-cao.md` → `/bao-cao`: chạy báo cáo + giải thích từng chỉ số
  - `kiem-tra-sheet.md` → `/kiem-tra-sheet`: ping kết nối + xem danh sách khách
  - `xoa-demo.md` → `/xoa-demo`: xóa dữ liệu demo (có bước xác nhận yes/no)
- **Xóa 5 dòng demo** khỏi Google Sheet → Sheet hiện trống, sẵn sàng dùng thật
- Xác minh kết nối: `python sheets_connector.py` → "Sheet trống hoặc chưa có dữ liệu" ✅

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `UnicodeEncodeError` khi chạy python trong PowerShell | Terminal dùng CP1252 mặc định | Thêm `$env:PYTHONIOENCODING="utf-8"` trước lệnh python khi chạy từ PowerShell (bat files không bị vì đã có `chcp 65001`) |

**Quyết định kiến trúc phiên 3:**

| Quyết định | Lý do |
|-----------|-------|
| Skills lưu dạng `.md` trong `.claude/commands/` | Chuẩn Claude Code — gõ `/tên-skill` là dùng được ngay, không cần cài thêm gì |
| `lich_ngay.py` song song với skill `/lich-ngay` | Skill dùng khi có Claude Code; .py + .bat dùng khi không có Claude — cùng một quy trình, hai cách tiếp cận |
| `/xoa-demo` yêu cầu xác nhận "yes" | Xóa dữ liệu trên Sheet là thao tác không hoàn tác được → cần barrier thủ công |
| Lưu tiến độ ngày vào `tien_do_YYYY-MM-DD.txt` | Mỗi ngày một file riêng, tự archive — không cần DB, dễ xem lại |

---

### Phiên 5 — 16/05/2026 — Re-import với Date Logic & Định Dạng Bảng Chuyên Nghiệp

**Vấn đề phát sinh sau phiên 4:**
- Sheet nguồn cũ (Khach_Hang_Ban2_Updated) thiếu thông tin ngày tiếp cận chính xác
- Cột Sale chăm sóc: 13 dòng ghi "TA" thay vì "Tuấn Anh" → tracker không nhận đúng
- Bảng CRM chưa có màu sắc và định dạng chuyên nghiệp

**Đã hoàn thành:**
- Tạo `format_sheet.py` — định dạng bảng CRM chuyên nghiệp qua Google Sheets API batchUpdate:
  - Freeze header row 1
  - Header: xanh rừng đậm (#1B5E20), chữ trắng bold, cao 42px
  - Banding xen kẽ: ROW_ODD=#F1F8E9, ROW_EVEN=#FFFFFF
  - Conditional formatting toàn hàng theo Trạng thái: Chốt cọc=#C8E6C9, Hẹn xem đất=#FFE0B2, Đang chăm sóc=#FFF8E1, Từ chối=#EEEEEE, Mới=#E3F2FD
  - Border xanh lá (#388E3C ngoài, #A5D6A7 trong), độ rộng cột: [155,120,120,105,120,220,110,130]
- Tạo `check_data.py` — kiểm tra chất lượng data: phát hiện SĐT thiếu số, tên trống, sale trống
- Tạo `fix_sale_name.py` — quét cột D (Sale) tìm "TA" → đổi thành "Tuấn Anh"; đã fix 13 dòng
- Tạo `reimport_with_dates.py` — re-import toàn bộ từ sheet nguồn mới (1h279Q2...):
  - Source: `1h279Q2vg3krxnoO7vR3uq70KZHGilXQNdV4PZeouGLU` (Sheet1, gid=0)
  - Logic cột A: "Số Cá nhân" → blank; ô có ngày (vd "18/03") → parse → `2026-MM-DD`; ô trống từ R13 trở đi → forward-fill từ ngày gần nhất
  - Map 16 cột nguồn → 8 cột CRM: C→Tên, F→SĐT, G→Nguồn, J→Sale, I→Trạng thái, A→Ngày tiếp cận & Ngày tương tác cuối, D+E+H→Ghi chú
  - `batch_clear(['A2:H200'])` trước khi ghi (giữ nguyên định dạng)
  - Skip: dòng không có tên lẫn SĐT thật (R52 chỉ có phone, R57–R59 template trống)
- **Kết quả:** 54 khách hàng với ngày tiếp cận đầy đủ — Hiển:15, Sơn:14, Tuấn Anh:13, Đức:12
- Xác minh date logic: C Hường=2026-03-18 ✅, Anh Tuyến=blank ✅, Chú Quảng=forward-fill ✅

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| gspread DeprecationWarning: `ws.update(range, values)` | API mới đổi thứ tự tham số | Chỉ là cảnh báo, update vẫn thành công; không cần sửa ngay |
| `fix_sale_name.py`: ValueError sau khi batch_update | gspread trả về range có tên sheet đầy đủ (vd `'KhaSonGreenHome_CRM'!D4`), code parse int bị lỗi | Update đã thành công trước khi lỗi xảy ra; lỗi chỉ trong phần print report |

**Quyết định kiến trúc phiên 5:**

| Quyết định | Lý do |
|-----------|-------|
| `DATE_START_IDX = 10` (tương ứng R13 trong sheet nguồn) | Trước R13 là nhóm "Số Cá nhân" không có ngày xác định; từ R13 mới bắt đầu tracking ngày theo batch |
| `parse_date()` tự gán năm 2026 | Sheet nguồn không ghi năm (chỉ ghi DD/MM); năm 2026 là năm vận hành hiện tại |
| `map_sale()` lấy tên đầu tiên khi nhiều sale | "Sơn, TA" → Sơn là người phụ trách chính; tên đầu tiên = người chịu trách nhiệm |
| Script `reimport_with_dates.py` độc lập (không sửa script cũ) | Có thể chạy lại bất kỳ lúc nào nếu sheet nguồn cập nhật; script cũ vẫn còn để tham khảo |
| Conditional formatting dùng CUSTOM_FORMULA `=$E2="Trạng thái"` | Lock cột E, cho phép check từng hàng tự động khi thêm dòng mới vào sheet |

---

### Phiên 6 — 16/05/2026 — Định Dạng Chuyên Nghiệp & User Guide trong Google Sheet

**Vấn đề phát sinh sau phiên 5:**
- Bảng CRM chưa có khu vực hướng dẫn sử dụng → anh em sale mới nhìn vào không biết màu sắc nghĩa là gì, ai phụ trách gì, cần làm gì mỗi ngày
- Cần chuẩn bị sheet sẵn sàng để triển khai thực tế từ ngày 17/05/2026

**Đã hoàn thành:**
- Tạo `format_ban2_daks.py` — script tạo tab mới với định dạng navy + User Guide (script tổng quát, có thể tái dùng cho bất kỳ tab nào mới)
- Tạo `apply_format_crm.py` — script chính: áp định dạng navy (#0D47A1) lên `KhaSonGreenHome_CRM`, xóa conditional formatting cũ, thêm User Guide tại I56:L90, xóa tab rỗng
- **Định dạng mới áp lên CRM tab** (thay thế định dạng xanh rừng từ phiên 5):
  - Header navy đậm `#0D47A1`, chữ trắng bold, cao 44px
  - Banding xen kẽ `#E8F4FD` / `#FFFFFF` (200 hàng — dự phòng leads mới)
  - Conditional formatting 5 trạng thái theo cột E: Mới/Đang chăm sóc/Hẹn xem đất/Chốt cọc/Từ chối
  - Border navy 2px ngoài, `#90CAF9` 1px trong
  - Độ rộng cột: [160, 130, 120, 120, 130, 240, 120, 130]px
- **User Guide tại I56:L90** — khu vực hướng dẫn trực quan gồm 6 section:
  - Tiêu đề navy to, phụ đề xanh nhạt
  - Màu sắc trạng thái (có nền màu minh họa từng dòng)
  - Quy trình hàng ngày (sáng/chiều/tối)
  - Trạng thái hợp lệ
  - Phân công sale (Hiển/Đức/Sơn/Tuấn Anh)
  - Quy tắc chăm sóc khách + Lưu ý quan trọng
- Xóa tab rỗng "Khach_Hang_Ban2 DA KS" → sheet chỉ còn **1 tab duy nhất**
- Sửa deprecation warning gspread: `ws.update(range, values)` → `ws.update(values=..., range_name=...)`

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| Tab "Khach_Hang_Ban2 DA KS" không tồn tại | User nhầm tên tab — thực tế tab duy nhất là `KhaSonGreenHome_CRM` | Xác nhận với user → tạo tab mới → xác nhận lại → áp vào CRM tab rồi xóa tab nhầm |
| `gspread DeprecationWarning: ws.update(range, values)` | gspread mới đổi thứ tự tham số | Dùng named args: `ws.update(values=..., range_name=...)` |

**Quyết định kiến trúc phiên 6:**

| Quyết định | Lý do |
|-----------|-------|
| Đổi header từ xanh rừng (#1B5E20) sang navy (#0D47A1) | Navy nhận diện thương hiệu BĐS chuyên nghiệp hơn; xanh rừng dễ nhầm với nền trạng thái "Chốt cọc" |
| User Guide tại cột I hàng 56 (không phải tab riêng) | Cùng một sheet → sale mở lên là thấy ngay; không cần chuyển tab |
| Banding phủ 200 hàng (không phải chỉ 54 hàng hiện tại) | Leads mới thêm vào tự có màu nền ngay mà không cần chạy lại script |
| `apply_format_crm.py` xóa conditional formatting cũ trước khi thêm mới | Tránh trùng rule → tránh conflict màu nền khi có nhiều rule cùng match |
| Giữ `format_ban2_daks.py` không xóa | Script tổng quát tạo tab mới — có thể dùng lại nếu cần mở tab thứ 2 sau này |

---

### Phiên 7 — 17/05/2026 — Config Tập Trung & Quản Lý Team Động

**Vấn đề phát sinh sau phiên 6:**
- `SALE_TEAM` hardcode trong 5 file `.py` khác nhau → khi có nhân viên mới phải nhớ sửa đủ 5 chỗ, dễ bỏ sót
- KPI, hotline, thông tin dự án cũng hardcode trong từng file → thay đổi phải sửa nhiều nơi
- Không có cách nào thêm/bớt thành viên team mà không cần sửa code

**Đã hoàn thành:**
- Tạo `config.json` — nguồn cấu hình duy nhất cho toàn hệ thống:
  ```json
  {
    "sale_team": ["Hiển", "Đức", "Sơn", "Tuấn Anh"],
    "remind_days": 3,
    "sheet_id": "1syWcPK_...",
    "worksheet_name": "KhaSonGreenHome_CRM",
    "kpi": { "lead_moi_per_tuan": 20, "xem_dat_per_tuan": 5, "chot_coc_per_thang": 3, "cpl_max": 100000 },
    "project": { "ten_du_an": "Kha Sơn Green Home", "hotline": "0368.557.832", ... }
  }
  ```
- Sửa `sheets_connector.py` — thêm `load_config()` và `save_config()` (export ra toàn hệ thống); SHEET_ID & WORKSHEET_NAME đọc từ config
- Sửa `tracker.py` — SALE_TEAM và REMIND_DAYS đọc từ config; thêm `reload_team()` để refresh global sau khi ghi; thêm `quan_ly_team()` menu [7]:
  - `[a]` Thêm thành viên: validate tên không trống/trùng → append vào config.json → `reload_team()`
  - `[c]` Vô hiệu hóa: validate team còn ≥ 2 người → xác nhận "yes" → xóa khỏi config.json → `reload_team()`; cảnh báo dữ liệu cũ vẫn giữ trong Sheet
- Sửa `daily_report.py` — REMIND_DAYS và SALE_TEAM đọc từ config; fallback về danh sách từ Sheet nếu config trống
- Sửa `lich_ngay.py` — KPI đọc từ config qua `_load_kpi()` với fallback hardcode
- Sửa `content_helper.py` — project variables (DU_AN, HOTLINE, KHU_VUC, GIA_TU, DIEN_TICH, PHAP_LY) đọc từ config qua `_load_project()` — dùng file json trực tiếp, không import sheets_connector (bảo toàn offline capability)

**Xác minh sau phiên 7 (tất cả pass):**
```
sale_team: ['Hiển', 'Đức', 'Sơn', 'Tuấn Anh']   ✔
remind_days: 3                                      ✔
sheet_id OK: True                                   ✔
tracker.SALE_TEAM: ['Hiển', 'Đức', 'Sơn', 'Tuấn Anh']  ✔
daily_report.REMIND_DAYS: 3                         ✔
lich_ngay.KPI: ['Lead moi/tuan  : >= 20', ...]     ✔
content_helper.DU_AN: Kha Sơn Green Home            ✔
save/load roundtrip: ✔
```

**Quyết định kiến trúc phiên 7:**

| Quyết định | Lý do |
|-----------|-------|
| `config.json` là nguồn duy nhất | Thay đổi một chỗ → tất cả script cập nhật ngay; không bao giờ phải sửa `.py` khi thêm/xóa thành viên |
| `load_config()` / `save_config()` trong `sheets_connector.py` | Module này đã được import bởi tracker & daily_report; không cần tạo file helper mới |
| Fallback 3 lớp: config.json → _DEFAULTS → hardcode | Đảm bảo không script nào crash nếu config.json bị xóa hoặc hỏng |
| `content_helper.py` đọc config.json trực tiếp (không qua sheets_connector) | content_helper.py phải chạy offline (không cần internet); import sheets_connector sẽ kéo theo gspread dependency |
| `reload_team()` refresh global ngay sau save | Round-robin trong phiên làm việc hiện tại phản ánh team mới ngay lập tức, không cần khởi động lại script |
| Menu [7] yêu cầu "yes" khi vô hiệu hóa thành viên | Thao tác ảnh hưởng phân công lead từ đây về sau — cần barrier thủ công, tránh nhấn nhầm |

---

### Phiên 8 — 17/05/2026 — Sửa Lỗi GSpreadException & Kiểm Tra Luồng Thêm Lead

**Vấn đề phát sinh sau phiên 7:**
- Chạy `tracker.py` → crash ngay khi load dữ liệu với lỗi: `GSpreadException: the header row in the worksheet contains duplicates: ['']`
- Hệ thống hoàn toàn không dùng được

**Nguyên nhân gốc:**
- Phiên 6 đã thêm User Guide vào cột I-L (I56:L90) trong Google Sheet
- `ws.get_all_records()` đọc TOÀN BỘ cột của sheet → bao gồm cả I-L
- Row 1 của cột I-L không có header (trống) → gspread 6.x coi nhiều ô trống là "duplicate headers" → raise exception
- Conflict giữa tính năng phiên 6 (User Guide) và hành vi gspread 6.x (strict header validation)

**Đã hoàn thành:**
- Sửa `sheets_connector.py` — hàm `load_data()`:
  - **Trước:** `records = ws.get_all_records()` → đọc tất cả cột, bị crash vì User Guide
  - **Sau:** `rows = ws.get("A:H")` → chỉ đọc đúng 8 cột dữ liệu, bỏ qua User Guide hoàn toàn
  - Skip header row (row 1), dùng `COLUMNS` hardcode thay vì đọc từ sheet
  - Padding ngắn dòng: `[r + [""] * (8 - len(r)) for r in data_rows]`
- Xác minh luồng thêm lead [4]: user test nhập khách "Thuần" → hệ thống nhận SĐT `797933666` (9 số, không có số 0 đầu) mà không cảnh báo → xác nhận cần Tính năng 1D (validate SĐT) ngay

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `GSpreadException: duplicate headers ['']` | User Guide cột I-L (phiên 6) có header trống; `get_all_records()` đọc toàn bộ cột | Đổi sang `ws.get("A:H")` — chỉ đọc vùng dữ liệu thật, bỏ qua User Guide |

**Quyết định kiến trúc phiên 8:**

| Quyết định | Lý do |
|-----------|-------|
| `ws.get("A:H")` thay vì `get_all_records()` | Không phụ thuộc vào nội dung row 1; ít API bandwidth hơn (chỉ 8 cột); hoạt động độc lập với gspread version |
| Giữ `COLUMNS` hardcode thay vì đọc từ header row | Header row trong Sheet có thể bị sửa tay; hardcode đảm bảo thứ tự cột luôn đúng |
| Padding dòng ngắn hơn 8 ô | `ws.get()` trả về row ngắn nếu các ô cuối trống; padding tránh IndexError khi build DataFrame |

---

### Phiên 9 — 17/05/2026 — Validate SĐT, Tìm Kiếm & Tab Staging "SỐ MỚI KS"

**Vấn đề phát sinh sau phiên 8:**
- Phiên 8 xác nhận cần 1A (trùng SĐT), 1B (tìm kiếm), 1D (validate SĐT)
- User yêu cầu lead mới không đi thẳng vào CRM mà vào tab staging trước — sale xem, tích ✓ sau khi liên hệ lần đầu, hệ thống tự chuyển sang CRM → kiểm soát chất lượng đầu vào

**Đã hoàn thành:**

**A. Tính năng 1D — Validate SĐT (tracker.py)**
- `_validate_sdt()` dùng `re.match(r'^0\d{9}$', sdt)` — bắt đầu `0`, đúng 10 số
- Loop hỏi lại cho đến khi hợp lệ hoặc bỏ trống; không cho phép nhập "zalo", số 9 chữ số

**B. Tính năng 1A — Kiểm tra trùng SĐT mở rộng (tracker.py)**
- Kiểm tra song song cả CRM (`df`) lẫn staging (`load_staging_data()`)
- `pd.concat([dup_crm, dup_stg])` → hiện tên khách, sale đang giữ, trạng thái, nguồn ("SỐ MỚI KS" hoặc "hệ thống CRM")
- Hỏi y/N trước khi cho thêm

**C. Tính năng 1B — Tìm kiếm theo SĐT, menu [8] (tracker.py)**
- `tim_kiem_sdt()` — tìm partial match trong cột Số ĐT
- Nếu chỉ 1 kết quả → hỏi có muốn cập nhật trạng thái không (gọi `cap_nhat_trang_thai`)

**D. Tab Staging "SỐ MỚI KS" — tính năng chính (sheets_connector.py + tracker.py)**
- `sheets_connector.py` — thêm 2 hằng số + 4 hàm:
  - `STAGING_TAB = "SỐ MỚI KS"`, `STAGING_COLS = COLUMNS + ["✓ Đã xử lý"]`
  - `ensure_staging_tab()` — tạo tab nếu chưa có: header vàng nhạt #FFF9C4, bold, freeze row 1, checkbox BOOLEAN data validation cột I (I2:I200)
  - `append_staging_row(row_dict)` — thêm lead với checkbox FALSE
  - `load_staging_data()` — trả về (DataFrame 8 cột, list sheet_row_indices)
  - `transfer_checked_leads()` — tìm dòng TRUE, append vào CRM + `highlight_new_row()`, xóa khỏi staging (xóa ngược để tránh shift index)
- `tracker.py` — 4 thay đổi:
  - `them_lead_moi()`: gọi `append_staging_row()` thay vì `append_row()`; không reload CRM df sau khi thêm (CRM chưa thay đổi)
  - `_show_staging_banner()`: hiện số khách chờ xử lý trên màn hình chính
  - `xu_ly_so_moi(df)`: menu [9] — gọi `transfer_checked_leads()`, in tên khách đã chuyển, reload df
  - `main()` startup và `[6]` refresh: tự động gọi `transfer_checked_leads()` mỗi khi khởi động

**E. daily_report.py — Block 2b chi tiết tên khách**
- `build_per_sale()` trả thêm `ten_chuyen` (list khách Hẹn/Chốt hôm nay) và `ten_qua_han` (list khách quá hạn)
- `print_report()` Block 2b: in màu xanh (Hẹn/Chốt) và đỏ (Quá hạn) với tên cụ thể
- `save_report()` ghi phần CHI TIẾT ra file `.txt`

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| Tab "SỐ MỚI KS" không tạo ngay | `ensure_staging_tab()` chỉ chạy khi `tracker.py` được khởi động lần đầu sau khi cập nhật code | Chạy `python tracker.py` một lần — startup tự gọi `transfer_checked_leads()` → `ensure_staging_tab()` → tạo tab |
| 3 lead test cũ (Thuần, Hiển, hiển) còn trong CRM | Được thêm phiên 8 khi code còn dùng `append_row()` trực tiếp | Xóa thủ công trong Google Sheets |

**Quyết định kiến trúc phiên 9:**

| Quyết định | Lý do |
|-----------|-------|
| Lead mới → staging, không vào CRM trực tiếp | Kiểm soát chất lượng: sale xác nhận đã liên hệ trước khi vào CRM chính; tránh CRM bị "ô nhiễm" bởi lead chưa verify |
| Checkbox BOOLEAN native của Sheets (không phải dropdown) | Sale trên điện thoại tích một chạm; trực quan hơn; không cần hiểu dropdown |
| `ws.get("A:I")` đọc checkbox dưới dạng string "TRUE"/"FALSE" | Consistent với cách đọc CRM; `.strip().upper() == "TRUE"` robust với mọi casing |
| Xóa staging ngược thứ tự (highest index first) | Tránh index shift — xóa dòng thấp trước sẽ làm index các dòng cao hơn bị sai |
| `base_row = len(cdf) + 2` tính trước vòng lặp transfer | CRM data sạch, không có gap → công thức đơn giản và đúng |
| Bold (không phải background) cho dòng mới trong CRM | CF phiên 6 đã lock background theo Trạng thái; bold không conflict với CF, vẫn nổi bật |
| `_show_staging_banner()` hiện ở màn hình chính | Nhắc nhở passive — sale thấy số chờ xử lý mỗi lần mở menu, không cần check sheet thủ công |
| Auto-transfer khi startup và [6] refresh | Không cần sale nhớ nhấn [9] — hệ thống tự làm; [9] chỉ dùng khi muốn transfer chủ động |

---

### Phiên 10 — 17/05/2026 — Fix 3 Bug Staging & Dọn Dẹp Data Test

**Vấn đề phát sinh sau phiên 9:**
- Thêm lead A Đăng qua menu [4] → tracker báo thành công nhưng tab "SỐ MỚI KS" hoàn toàn trống
- SĐT bị mất số 0 đầu: `0978381911` → `978381911`

**Nguyên nhân gốc (3 bug liên quan):**

| Bug | Nguyên nhân |
|-----|------------|
| Lead ghi vào row 201, không nhìn thấy | BOOLEAN data validation I2:I200 tạo implicit FALSE trên 199 dòng → `append_row()` bị API tưởng bảng đầy đến row 200 → append vào row 201 |
| SĐT mất số 0 đầu | `USER_ENTERED` khiến Google Sheets xử lý `"0978..."` như số học → strip số 0 |
| `load_staging_data()` trả về 199 dòng giả | Đọc A:I không filter → checkbox data validation tạo 199 dòng "có dữ liệu" ảo |

**Đã hoàn thành:**
- Sửa `append_staging_row()` trong `sheets_connector.py`:
  - Dùng `col_values(1)` đếm dòng thật trong cột A → tính `next_row` chính xác (tránh bị checkbox đánh lừa)
  - Đổi sang `ws.update(..., value_input_option="RAW")` cho cột A:H → giữ nguyên số 0 đầu SĐT
  - Không ghi cột I (để trống) → checkbox tự hiện unchecked do BOOLEAN data validation
- Sửa `load_staging_data()` trong `sheets_connector.py`:
  - Thêm filter `if not padded[0].strip(): continue` → bỏ qua dòng trống (checkbox ảo)
- Di chuyển A Đăng từ row 201 về row 2 đúng vị trí + fix SĐT thành `0978381911`
- **Trạng thái SỐ MỚI KS:** 1 lead thật (A Đặng / 0978381911 / Sơn)

**Quyết định kiến trúc phiên 10:**

| Quyết định | Lý do |
|-----------|-------|
| `col_values(1)` thay vì `append_row` cho staging | `col_values` chỉ đọc cột A (Tên khách), không bị ảnh hưởng bởi checkbox ở cột I; luôn trả đúng next empty row |
| `RAW` thay vì `USER_ENTERED` cho data A:H | Giữ nguyên chuỗi số (SĐT bắt đầu 0); USER_ENTERED parse như formula → strip leading zero |
| Không ghi FALSE vào cột I | Checkbox với BOOLEAN validation mặc định unchecked khi ô trống; ghi FALSE thêm với USER_ENTERED không cần thiết |
| Filter dòng trống trong `load_staging_data` | Checkbox validation tạo 199 dòng FALSE ảo → phải filter theo cột A để chỉ lấy lead thật |

---

### Phiên 11 — 17/05/2026 — Giai Đoạn 2: Nhu Cầu + Phễu ASCII + Leaderboard + Báo cáo tuần

**Đã hoàn thành:**

**A. Cột "Nhu cầu" (sheets_connector.py + tracker.py + daily_report.py)**
- `migrate_user_guide()`: chuyển User Guide từ `I56:L90` → `M56:P90`; ghi header "Nhu cầu" vào `I1`
- `COLUMNS` mở rộng 8→9 cột; `load_data()` đọc A:I, filter dòng trống col A
- `update_row()` / `highlight` / `unhighlight`: mở rộng range A:I
- `tracker.py`: menu [5] hỏi "Nhu cầu?" sau khi cập nhật trạng thái; menu [8] hiển thị Nhu cầu; banner đỏ `_show_nhu_cau_banner()` ở startup + refresh [6]
- `daily_report.py`: Block 3 liệt kê khách "Không còn nhu cầu" (màu đỏ)

**B. Phễu Chuyển Đổi ASCII (daily_report.py — Block 4)**
- `build_funnel()`: đếm 4 bước Mới/Chăm/Hẹn/Chốt, tính conversion rate từng bước, xác định THẮT CỔ CHAI
- `print_report()` Block 4: thanh `█` scale theo count, tỷ lệ % giữa các bước, label đỏ cho bottleneck

**C. Leaderboard Tháng (daily_report.py — Block 5)**
- `build_leaderboard()`: Chốt=10đ, Hẹn=3đ, 0 quá hạn=+2đ bonus; tính theo tháng hiện tại
- Block 5 in bảng xếp hạng với thanh bar + điểm số + chi tiết

**D. weekly_report.py (tạo mới)**
- `build_weekly_summary()`: thống kê 7 ngày, so sánh tuần trước (delta +/-/=)
- `build_source_analysis()`: group by Nguồn, tỷ lệ chốt từng nguồn, xếp hạng ★
- `Bao Cao Tuan.bat`: double-click để chạy; lưu `bao_cao_tuan_W{N}_2026.txt`

**Quyết định kiến trúc phiên 11:**

| Quyết định | Lý do |
|-----------|-------|
| `migrate_user_guide()` chuyển sang M56:P90 | Column I vừa được thêm cho Nhu cầu; User Guide tại I56 sẽ conflict khi lead thứ 55 vào CRM |
| `load_data()` filter `if not row[0].strip()` | Sau khi thêm col I, User Guide cũ tại I56+ có A trống → phải filter để tránh đọc nhầm |
| Phễu dùng count tuyệt đối, không phải ngày | Pipeline BĐS không phải linear funnel theo thời gian; count theo trạng thái thực tế đang có |
| Leaderboard chỉ tính tháng hiện tại | Tránh tích lũy điểm từ tháng cũ; reset mỗi tháng tạo động lực thi đua mới |
| `in_week.astype(bool)` trong weekly_report | Pandas 4.x không cho phép `boolean_series & object_series`; cần ép kiểu rõ ràng |

---

### Phiên 12 — 17/05/2026 — Giai Đoạn 3: Tự Động Hóa Nhắc Nhở & Dọn Dẹp

**Đã hoàn thành:**

**A. nhac_sang.py + Windows Task Scheduler**
- `get_overdue(df, remind_days)` → dict `{sale: [(days, row), ...]}` — chỉ ACTIVE_STATUS, sắp xếp ngày giảm dần
- `days_since()` copy từ tracker.py:40-49; import `load_data`, `load_config` từ sheets_connector
- Banner đỏ ASCII (╔═╗), bảng chi tiết theo từng sale; đỏ đậm nếu ≥ 5 ngày
- Nếu không có khách quá hạn → thoát luôn `sys.exit(0)` (không làm phiền)
- `Nhac Sang.bat` — double-click test thủ công
- `setup_task_scheduler.py` — tạo task `KhaSon_NhacNhoSang` bằng `schtasks.exe`, T2-T7 lúc 08:00; hướng dẫn thủ công nếu thiếu quyền Admin

**B. cleanup_reports.py**
- `get_report_month()` — regex parse tên file daily (`bao_cao_YYYY-MM-DD.txt`) và weekly (`bao_cao_tuan_W{N}_YYYY.txt`) → `YYYY-MM`
- Bỏ qua tháng hiện tại; chỉ zip và xóa file tháng cũ (`m < current_month`)
- Preview danh sách file + xác nhận "yes" trước khi xóa; tạo `archive/` nếu chưa tồn tại
- `Don Dep Bao Cao.bat` — double-click để chạy

**Xác minh sau phiên 12:**
- `nhac_sang.py` → hiện 29 khách quá hạn theo 4 sale; format banner ✅
- `cleanup_reports.py` → "Khong co file cu nao can don dep" (tất cả file thuộc tháng 05 hiện tại) ✅

**Quyết định kiến trúc phiên 12:**

| Quyết định | Lý do |
|-----------|-------|
| `sys.exit(0)` khi không có khách quá hạn | Task Scheduler chạy tự động 8:00; cần silent nếu không có gì quan trọng — không spam pop-up vô ích |
| `days_since()` copy (không import từ tracker) | tracker.py không phải module; import nó sẽ kéo theo toàn bộ logic UI/menu không cần thiết |
| Sắp xếp overdue theo ngày giảm dần | Sale thấy khách khẩn nhất (nhiều ngày nhất) ở đầu danh sách → ưu tiên gọi đúng chỗ |
| `m < current_month` thay vì `!=` | So sánh string `YYYY-MM` hoạt động đúng thứ tự thời gian; tránh xóa nhầm file tháng tương lai |
| Xác nhận "yes" trước khi xóa | Xóa file không phục hồi được; barrier thủ công bắt buộc dù script có vẻ an toàn |

---

### Phiên 13 — 17/05/2026 — Tài Liệu Hướng Dẫn Vận Hành (Word)

**Vấn đề phát sinh sau phiên 12:**
- Chưa có tài liệu hướng dẫn dành riêng cho 2 đối tượng khác nhau: trưởng nhóm (cần nắm toàn bộ kỹ thuật) và nhân sự mới (chỉ cần biết quy trình hàng ngày + kịch bản giao tiếp)
- File cũ `Huong_Dan_Van_Hanh_CRM.docx` (một file duy nhất) không phân biệt được hai đối tượng này
- Team tăng từ 5 → 6 người (thêm Nam và Tiến vào config.json)

**Đã hoàn thành:**

**A. Huong_Dan_Truong_Nhom.docx** — 10 chương, dành cho Hiển (trưởng nhóm)
- Chương 1: Tổng quan hệ thống — cấu trúc nhân sự 6 người, KPI tháng, Google Sheets tabs, màu sắc trạng thái
- Chương 2: Các file vận hành — bảng 7 file .bat + vai trò từng file, file cấu hình quan trọng
- Chương 3: Quy trình vận hành hàng ngày — sáng/chiều/tối/thứ Hai/đầu tháng với từng bước cụ thể
- Chương 4: Hướng dẫn chi tiết tracker.py — menu [1]–[9] đầy đủ
- Chương 5: Luồng xử lý lead mới — bảng 5 bước (ai làm gì, hệ thống ghi nhận gì)
- Chương 6: Hệ thống báo cáo — báo cáo ngày (5 block), tuần, dọn dẹp
- Chương 7: Hệ thống nhắc nhở tự động — cách hoạt động, kích hoạt Task Scheduler, test thủ công
- Chương 8: Quản lý team — thêm/vô hiệu hóa thành viên, round-robin
- Chương 9: Xử lý sự cố thường gặp — bảng 6 triệu chứng + cách fix
- Chương 10: Quy tắc vàng + Phụ lục cấu trúc thư mục

**B. Huong_Dan_Nhan_Su.docx** — 9 chương, dành cho nhân viên mới
- Chương 1: Chào mừng — thông tin dự án, bảng đội ngũ 6 người
- Chương 2: Các trạng thái khách hàng (5 trạng thái bắt buộc nắm vững + hành động tiếp theo)
- Chương 3: Việc cần làm mỗi ngày — sáng/trong ngày/chiều (không cần biết terminal)
- Chương 4: Cách dùng Google Sheets — truy cập, 9 cột CRM, tab SỐ MỚI KS, thao tác điện thoại
- Chương 5: Quy tắc chăm sóc khách hàng — bảng 7 tình huống + hành động
- Chương 6: KPI cá nhân — chỉ tiêu + hệ thống điểm Leaderboard
- Chương 7: 3 kịch bản telesale mẫu (A: FB Ads mới, B: gọi lại, C: mời xem đất)
- Chương 8: CẦN LÀM / KHÔNG được làm — 2 hộp nổi bật xanh/đỏ
- Chương 9: Liên hệ hỗ trợ — bảng 5 loại vấn đề + người liên hệ

**C. Dọn dẹp file cũ**
- Xóa `Huong_Dan_Van_Hanh_CRM.docx` (file cũ, 1 tài liệu cho cả 2 đối tượng)
- Xóa `make_huong_dan.py` (script cũ)
- Thay bằng: `Huong_Dan_Truong_Nhom.docx`, `Huong_Dan_Nhan_Su.docx`, `make_huong_dan_v2.py`

**Xác minh sau phiên 13:**
- `python make_huong_dan_v2.py` → `[OK] Huong_Dan_Truong_Nhom.docx` + `[OK] Huong_Dan_Nhan_Su.docx` ✅

**Quyết định kiến trúc phiên 13:**

| Quyết định | Lý do |
|-----------|-------|
| Tách thành 2 file riêng biệt (không phải 1 file chung) | Trưởng nhóm cần nắm toàn bộ kỹ thuật + admin; nhân viên mới chỉ cần quy trình + kịch bản — nội dung quá khác nhau để gộp vào 1 file |
| Giữ `make_huong_dan_v2.py` (không xóa script) | Khi thêm nhân sự mới hoặc thay đổi quy trình, chỉ cần sửa script và chạy lại để cập nhật cả 2 file Word — không cần chỉnh sửa .docx thủ công |
| Định dạng navy + hộp màu (không phải plain text) | Tài liệu Word chuyên nghiệp → ấn tượng khi onboard nhân viên mới; màu sắc giúp phân biệt cảnh báo/quan trọng/OK ngay tức thì |
| Kịch bản telesale trong tài liệu nhân sự (không chỉ để trong content_helper.py) | Nhân sự mới cần đọc được ngay khi chưa mở máy tính; tài liệu in ra để trên bàn là đủ dùng |
| Cập nhật team 5→6 người trong CLAUDE.md | config.json đã có Nam và Tiến; CLAUDE.md phải nhất quán để tránh nhầm lẫn khi đọc lại |

---

### Phiên 14 — 18/05/2026 — Sửa Lỗi append_staging_row (APIError 400)

**Vấn đề phát sinh sau phiên 13:**
- Chạy tracker.py → menu [4] Thêm lead mới → nhập đầy đủ thông tin → crash với lỗi:
  `gspread.exceptions.APIError: [400]: Requested writing within range ['SỐ MỚI KS'!A2:H2], but tried to write to column [I]`
- Không thể thêm lead mới vào hệ thống

**Nguyên nhân gốc:**
- Phiên 11 mở rộng `COLUMNS` từ 8 → 9 phần tử (thêm `"Nhu cầu"` ở vị trí cuối)
- Hàm `append_staging_row()` dùng toàn bộ `COLUMNS` để tạo `data_row` → tạo ra **9 giá trị**
- Nhưng range ghi vào staging vẫn hardcode `A{next_row}:H{next_row}` (chỉ 8 cột)
- Google Sheets API phát hiện mismatch: 9 giá trị vs 8 cột → trả về lỗi 400
- Comment trong code `# A:H, không ghi cột I` đúng ý định nhưng không đúng thực tế sau phiên 11

**Đã hoàn thành:**
- Sửa `sheets_connector.py` dòng 164 — `append_staging_row()`:
  - **Trước:** `data_row = [str(row_dict.get(c, "")) for c in COLUMNS]` — 9 giá trị
  - **Sau:** `data_row = [str(row_dict.get(c, "")) for c in COLUMNS[:8]]` — đúng 8 giá trị (A–H)
- Staging tab không có cột "Nhu cầu"; cột I của staging là checkbox "✓ Đã xử lý" — để trống như thiết kế

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `APIError [400]: tried to write to column [I]` | `COLUMNS` mở rộng 8→9 phiên 11 nhưng range staging vẫn A:H (8 cột) — data dư 1 phần tử | Dùng `COLUMNS[:8]` thay vì `COLUMNS` trong `append_staging_row()` |

**Quyết định kiến trúc phiên 14:**

| Quyết định | Lý do |
|-----------|-------|
| `COLUMNS[:8]` thay vì tạo hằng số `STAGING_DATA_COLS` riêng | Fix tối thiểu, không tạo thêm abstraction — staging chỉ cần 8 cột đầu, dùng slice là đủ rõ |
| Không sửa comment thành cảnh báo dài | Rule bất biến: staging luôn ghi A:H, cột I luôn là checkbox — không phụ thuộc vào số cột trong `COLUMNS` |

---

### Phiên 15 — 18/05/2026 — Fix Vị Trí Transfer & Tính Năng Đảo Số Random

**Vấn đề phát sinh sau phiên 14:**
- Lead tích ✓ trong tab "SỐ MỚI KS" khi dùng menu [9] bị ghi vào vùng sai (I92:P93) thay vì vị trí liền kề cuối bảng CRM
- Chưa có tính năng phân công lead ngẫu nhiên — chỉ có round-robin cố định

**Đã hoàn thành:**

**A. Fix `append_row()` — sheets_connector.py dòng 77-82**
- **Nguyên nhân:** `ws.append_row()` dùng Google Sheets API auto-detect table extent. User Guide tại M56:P90 khiến API thấy bảng trải đến cột P row 90 → append vào vùng sai (I92:P93)
- **Fix:** Đổi sang `col_values(1)` đếm dòng thật trong cột A → tính `next_row` chính xác → ghi bằng `ws.update()` với explicit range `A{next_row}:I{next_row}` và `value_input_option="RAW"`
- Cùng pattern với fix staging phiên 10; RAW giữ nguyên số 0 đầu SĐT

**B. Tính năng đảo số random — config.json + tracker.py**
- `config.json`: thêm `"assign_mode": "roundrobin"` (mặc định) — hiện đã đổi sang `"random"` theo yêu cầu
- `tracker.py` `_next_sale()`: đọc `assign_mode` → nếu `"random"` thì `random.choice(SALE_TEAM)`, ngược lại round-robin như cũ
- Menu [7] thêm `[d] Đổi chế độ phân công` — toggle qua lại, lưu vào config.json ngay lập tức
- Menu chính hiển thị `Tổng leads: X  |  Phân công: 🔄 Round-robin` hoặc `🎲 Random`

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| Lead transfer vào I92:P93 thay vì A74:I75 | `ws.append_row()` bị User Guide M56:P90 đánh lừa → append sai vị trí | Dùng `col_values(1)` + `ws.update()` explicit range, tương tự fix staging phiên 10 |

**Quyết định kiến trúc phiên 15:**

| Quyết định | Lý do |
|-----------|-------|
| `col_values(1)` thay `ws.append_row()` trong `append_row()` | Đọc cột A không bị ảnh hưởng bởi dữ liệu cột khác (User Guide); luôn trả đúng next empty row |
| `assign_mode` lưu trong config.json (không hardcode) | Có thể toggle từ menu [7][d] mà không cần sửa code; persistent qua các phiên làm việc |
| `random.choice(SALE_TEAM)` — random thuần (không weighted) | Đơn giản, đủ dùng cho team nhỏ; không cần theo dõi trạng thái giữa các lần gọi |
| Hiển thị chế độ ở menu chính (không chỉ menu [7]) | Sale leader thấy ngay chế độ hiện tại mỗi khi mở menu — không cần vào [7] để kiểm tra |

---

### Phiên 16 — 18/05/2026 — Phân Công Sale Chỉ Định Khi Thêm Lead

**Vấn đề phát sinh sau phiên 15:**
- Menu [4] luôn tự động chia sale theo round-robin/random — không có cách giao lead cho một sale cụ thể ngay khi nhập (VD: khách gọi thẳng cho Đức → vẫn phải để hệ thống tự chia rồi sửa lại thủ công)

**Đã hoàn thành:**

**A. Bước chọn sale trong `them_lead_moi()` — tracker.py dòng 109**
- Sau khi nhập nguồn + ghi chú, hệ thống hiển thị danh sách sale có đánh số:
  ```
  Phân công sale:
  [0] Tự động (round-robin / random)
  [1] Hiển   [2] Đức   [3] Sơn  ...
  Chọn (Enter = tự động):
  ```
- Nhập số → chỉ định đúng sale đó; Enter/0/chữ → gọi `_next_sale(df)` như cũ
- In xác nhận: `→ Chỉ định: Đức` hoặc `→ Tự động: Sơn`

**B. Cập nhật text menu chính**
- Dòng [4] đổi từ `"(auto chia sale)"` → `"(tự động / chỉ định sale)"`

**Lỗi phát sinh và cách xử lý:** Không có lỗi.

**Quyết định kiến trúc phiên 16:**

| Quyết định | Lý do |
|-----------|-------|
| Prompt chọn sale nằm trong `them_lead_moi()`, không tạo hàm mới | Thay đổi tối thiểu, không phá vỡ luồng hiện tại; logic gọn trong 8 dòng |
| `_next_sale()` giữ nguyên hoàn toàn | Hàm này vẫn là engine cho auto-assign; không cần biết về chế độ manual |
| Danh sách sale lấy từ `SALE_TEAM` (không hardcode) | Khi thêm/xóa thành viên qua menu [7], danh sách chọn tự cập nhật — không cần sửa code |
| Fallback về tự động khi nhập sai/chữ | Tránh crash; người dùng bấm nhầm không mất lead |
| `config.json` và `assign_mode` không thay đổi | Tính năng mới độc lập hoàn toàn với chế độ round-robin/random toàn cục |

---

### Phiên 16 — 18/05/2026 — Date Picker & Tách Logic Quá Hạn / Giữ Tương Tác

**Vấn đề phát sinh sau phiên 15:**
- Cột Ngày tiếp cận (G) và Ngày tương tác cuối (H) chưa có date picker → sale nhập tay dễ sai định dạng
- Logic "quá hạn" không phân biệt khách *còn muốn mua* vs khách *đã từ chối* → sale bị cảnh báo sai đối tượng; bỏ sót nhắc re-engage khách tiềm năng

**Đã hoàn thành:**

**A. Date Picker cột G và H — fix_and_validate_crm.py**
- Thêm `DATE_IS_VALID` data validation với `showCustomUi: True`, `strict: False` cho G2:G300 và H2:H300
- Sale click ô ngày → calendar picker xuất hiện tự động; không cần nhập tay định dạng ngày
- `strict: False` → không xóa ngày cũ đã có; chỉ cảnh báo nếu nhập text không hợp lệ

**B. config.json — thêm `nurture_days`**
- Thêm `"nurture_days": 14` — ngưỡng ngày để nhắc re-engage khách "Không còn nhu cầu"

**C. tracker.py — tách logic quá hạn + giữ tương tác**
- Thêm hằng số `NURTURE_DAYS = _cfg.get("nurture_days", 14)`
- `kiem_tra_quen_khach()`: skip khách "Không còn nhu cầu" (không báo quá hạn)
- Thêm hàm `kiem_tra_giu_tuong_tac(df)`: liệt kê khách KNC chưa liên hệ ≥ 14 ngày (section vàng)
- `_print_table()`: ô màu vàng cho KNC ≥ NURTURE_DAYS; chỉ đỏ khi ACTIVE + còn nhu cầu + ≥ REMIND_DAYS
- `overdue_count` ở màn hình chính: loại trừ KNC
- Menu [3]: gọi cả `kiem_tra_quen_khach()` và `kiem_tra_giu_tuong_tac()`

**D. nhac_sang.py — 2 section riêng (đỏ + vàng)**
- `get_overdue()`: thêm skip "Không còn nhu cầu"
- Thêm hàm `get_nurture(df, nurture_days)`: KNC + chưa liên hệ ≥ nurture_days
- `main()`: thoát `sys.exit(0)` chỉ khi CẢ HAI danh sách trống; in section đỏ trước, vàng sau

**E. daily_report.py — phản ánh logic mới**
- Thêm `NURTURE_DAYS = _cfg.get("nurture_days", 14)`
- `build_per_sale()`: tính `giu_tt` (KNC ≥ NURTURE_DAYS) tách riêng `qua_han` (loại KNC)
- `build_leaderboard()`: số quá hạn loại trừ KNC → điểm Leaderboard chính xác hơn
- Block 2b: thêm dòng vàng "Giữ TT" với tên khách và số ngày
- `build_nhu_cau()` / Block 3: thêm field `days` → hiển thị số ngày chưa liên hệ

**Xác minh sau phiên 16:**
- `nhac_sang.py`: section đỏ (Sơn 9, Tuấn Anh 8, Đức 13) + section vàng (Hiển 13 khách KNC) ✅
- `daily_report.py`: Hiển 0 quá hạn + dòng "Giữ TT: C Hường (61 ngày), ..." ✅
- Không có Pandas4Warning ✅

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `Pandas4Warning: 'and' between bool and str` | Pandas 4.x strict về dtype khi dùng `&` | Thêm `.astype(bool)` cho tất cả mask trước khi combine |

**Quyết định kiến trúc phiên 16:**

| Quyết định | Lý do |
|-----------|-------|
| Tách `qua_han` và `giu_tt` thành 2 dict riêng | Khách KNC không phải "quá hạn" — gộp chung sẽ tạo áp lực sai cho sale; 2 section riêng cho phép hành động khác nhau |
| `nurture_days: 14` trong config (không hardcode) | Dễ điều chỉnh theo chiến lược team mà không cần sửa code |
| `strict: False` cho date picker | Không xóa dữ liệu cũ; chỉ guide nhập mới — an toàn khi triển khai lên sheet đang có data |
| `sys.exit(0)` chỉ khi cả 2 list trống | Nhắc sang cần báo cả 2 loại; nếu chỉ có nurture mà không có overdue thì vẫn cần hiện |

---

### Phiên 17 — 19/05/2026 — Fix Crash `load_staging_data()` Khi Staging Có Dữ Liệu

**Vấn đề phát sinh sau phiên 16:**
- Chạy `tracker.py` → crash ngay khi khởi động với lỗi:
  `ValueError: 9 columns passed, passed data had 8 columns`
- Traceback: `main()` → `_show_staging_banner()` → `load_staging_data()` → `pd.DataFrame(records, columns=COLUMNS)`

**Nguyên nhân gốc:**
- Phiên 11 mở rộng `COLUMNS` từ 8 → 9 phần tử (thêm `"Nhu cầu"`)
- `load_staging_data()` đã đúng khi build `records`: chỉ lấy `padded[:8]` (8 giá trị/dòng) vì staging không có cột "Nhu cầu" (cột I staging là checkbox "✓ Đã xử lý")
- Nhưng khi tạo DataFrame lại dùng `columns=COLUMNS` (9 tên cột) → mismatch 8 vs 9 → crash
- Bug tiềm ẩn từ phiên 11, chỉ bộc lộ khi staging có lead thật (khi staging trống → nhánh `else pd.DataFrame(columns=COLUMNS)` → không crash)
- Phiên 14 đã fix `append_staging_row()` dùng `COLUMNS[:8]` nhưng **bỏ sót `load_staging_data()`**

**Đã hoàn thành:**
- Sửa `sheets_connector.py` dòng 195 — `load_staging_data()`:
  - **Trước:** `pd.DataFrame(records, columns=COLUMNS).fillna("") if records else pd.DataFrame(columns=COLUMNS)`
  - **Sau:** `pd.DataFrame(records, columns=COLUMNS[:8]).fillna("") if records else pd.DataFrame(columns=COLUMNS[:8])`

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `ValueError: 9 columns passed, passed data had 8 columns` | `COLUMNS` (9) mở rộng phiên 11 nhưng staging chỉ có 8 cột dữ liệu; `load_staging_data()` bị bỏ sót khi fix phiên 14 | Dùng `COLUMNS[:8]` thay `COLUMNS` trong cả 2 nhánh if/else của `load_staging_data()` |

**Quyết định kiến trúc phiên 17:**

| Quyết định | Lý do |
|-----------|-------|
| `COLUMNS[:8]` (không tạo hằng số `STAGING_DATA_COLS` riêng) | Fix tối thiểu, nhất quán với `append_staging_row()` đã dùng `COLUMNS[:8]` từ phiên 14; không thêm abstraction không cần thiết |
| Không sửa thêm file nào khác | Chỉ `load_staging_data()` bị ảnh hưởng; `append_staging_row()` và `transfer_checked_leads()` không cần thay đổi |

**Quy tắc bất biến sau phiên 17:**
> Tab staging "SỐ MỚI KS" chỉ có 8 cột dữ liệu (A:H). Cột I staging là checkbox, không phải "Nhu cầu". Bất kỳ hàm nào đọc/ghi staging đều phải dùng `COLUMNS[:8]`, không phải `COLUMNS`. Nếu thêm cột mới vào `COLUMNS` trong tương lai, phải kiểm tra lại CẢ HAI: `append_staging_row()` VÀ `load_staging_data()`.

---

### Phiên 18 — 19/05/2026 — Lịch Sử Sale Khi Chuyển Lead

**Vấn đề phát sinh sau phiên 17:**
- Khi dùng menu [7][e] chuyển lead từ sale này sang sale khác, không có ghi nhận nào về việc ai đã cầm số trước → mất dấu lịch sử chăm sóc
- User muốn: "số bắn sang cho ai thì người đó chăm, và có lịch sử người chăm trước"

**Đã hoàn thành:**
- Sửa `chuyen_leads_giua_sale()` trong `tracker.py` — thêm 4 dòng vào Bước 6 (dòng 421):
  - Trước mỗi `append_staging_row()`, tính `log_entry = f"[{today_str} Sale: {nguon_sale}→{dich_sale}]"`
  - Append vào Ghi chú hiện tại của lead (không ghi đè — giữ nguyên ghi chú cũ)
  - Kết quả trong CRM: cột Ghi chú sẽ có `[19/05 Sale: Hiển→Chị Dung]`, và tích lũy thêm nếu chuyển tiếp

**Ví dụ lịch sử:**
```
Lần 1: [19/05 Sale: Hiển→Chị Dung]
Lần 2: [19/05 Sale: Hiển→Chị Dung] [20/05 Sale: Chị Dung→Đức]
```

**Lỗi phát sinh và cách xử lý:** Không có lỗi.

**Quyết định kiến trúc phiên 18:**

| Quyết định | Lý do |
|-----------|-------|
| Ghi vào Ghi chú (không tạo cột mới) | Không thay đổi schema; Ghi chú đã hiện trong [8] tìm kiếm → sale thấy ngay lịch sử mà không cần mở tab khác |
| Dùng `old_note + log_entry` (append, không ghi đè) | Bảo toàn ghi chú gốc; lịch sử tích lũy sau nhiều lần chuyển |
| Format `[DD/MM Sale: Cũ→Mới]` | Ngắn gọn, nhận diện nhanh, phân biệt với ghi chú bình thường bằng dấu `[` |

---

### Phiên 19 — 19/05/2026 — Fix Bug Row-Index & Dọn Dẹp Data

**Vấn đề phát sinh sau phiên 18:**
- User chuyển 17 leads từ Hiển → Chị Dung qua [7][e], Chị Dung tích ✓, transfer chạy → nhưng CRM chỉ hiện 2 leads của Chị Dung thay vì 17
- Điều tra phát hiện: 13/17 leads biến mất hoàn toàn khỏi hệ thống; 3 leads còn kẹt dưới tên Hiển

**Nguyên nhân gốc — Bug `pandas_idx + 2`:**
- `load_data()` bỏ qua các hàng có col A trống (thiết kế đúng), nhưng tạo DataFrame với index 0-based
- Trong sheet thực tế có 1 hàng không có tên (SĐT 0398891398, Sale Sơn) → hàng này bị skip → các hàng sau đó có pandas index thấp hơn sheet row 1 đơn vị
- `chuyen_leads_giua_sale()` dùng `pidx + 2` để tính sheet row → SAI 1 đơn vị cho mọi hàng sau hàng không tên
- Kết quả: xóa sai hàng (xóa nhầm lead của sale khác hoặc hàng trống), 13 leads bị mất vĩnh viễn
- Tương tự: `cap_nhat_trang_thai()` cũng dùng `pandas_idx + 2` → cập nhật sai hàng khi có hàng không tên

**Đã hoàn thành:**
- Sửa `sheets_connector.py` — `load_data()`: thêm `sheet_row_indices` tracking, dùng làm DataFrame index thay vì 0-based → `df.index` = sheet row thực tế [2, 3, ..., 36, 38, 39, ...]
- Sửa `sheets_connector.py` — `transfer_checked_leads()`: `base_row = max(cdf.index) + 1 if not cdf.empty else 2` thay cho `len(cdf) + 2`
- Sửa `tracker.py` — `cap_nhat_trang_thai()`: `row_idx = pandas_idx` (bỏ `+ 2`)
- Sửa `tracker.py` — `chuyen_leads_giua_sale()`: `sorted(selected_indices, reverse=True)` (bỏ `+ 2`)
- Dọn dẹp CRM: đổi c Hường + Anh Đặng từ Hiển → Chị Dung; xóa bản trùng A Hiếu dưới Hiển; thêm tên cho lead không tên (SĐT 0398891398)
- **Thiệt hại không phục hồi được**: 13 leads bị mất vĩnh viễn (C Hường, a duy, Chú Quảng, Anh Hậu, A Thắng, Cường, Thái, A trọng, Từ, Hạo, Dương, A Tam, C Luyến) — user cần nhập lại từ nguồn gốc

**Quyết định kiến trúc phiên 19:**

| Quyết định | Lý do |
|-----------|-------|
| DataFrame index = sheet row (không phải 0-based) | Loại bỏ hoàn toàn lỗi `pidx + 2` — index trực tiếp là sheet row nên không cần tính thêm gì |
| `max(cdf.index) + 1` cho base_row | Đúng kể cả khi có hàng trống — lấy sheet row cuối cùng thực tế thay vì đếm số hàng |
| Không xóa hàng không tên (row 37) | Hàng đó có lead thực (SĐT 0398891398, Sơn); thêm tên placeholder thay vì xóa |

**Quy tắc bất biến sau phiên 19:**
> `df.index` của `load_data()` = sheet row thực tế (2, 3, ..., không bao giờ là 0-based). Mọi thao tác xóa/update qua `delete_crm_row(idx)` / `update_row(idx, ...)` dùng trực tiếp giá trị trong `df.index` — không cộng thêm gì. Nếu thêm bất kỳ tính toán `idx + N` nào trong tương lai, PHẢI đặt câu hỏi: idx ở đây là sheet row hay pandas 0-based?

---

### Phiên 23 — 20/05/2026 — Deploy Dashboard lên Streamlit Community Cloud & Đổi Tên App

**Vấn đề phát sinh & Yêu cầu mới:**
- `dashboard.py` chỉ chạy được trên máy Hiển (`D:\QuanLyBKD2`) — cả team không truy cập được từ điện thoại
- Cần deploy lên cloud miễn phí để team dùng như app thật, thêm vào màn hình chính điện thoại

**Đã hoàn thành:**

**A. Chuẩn bị Deploy**
- Sửa `sheets_connector.py` — thêm `_get_credentials()` hỗ trợ 2 môi trường: thử `st.secrets["google_credentials"]` trước (Streamlit Cloud), fallback về `data/google_creds.json` (local). Ba hàm `_get_ws()`, `migrate_user_guide()`, `ensure_staging_tab()` đều dùng hàm mới này. Local system (tracker.py, Mo Dashboard.bat) **hoàn toàn không bị ảnh hưởng**.
- Tạo `.streamlit/secrets.toml` — local only, gitignored — chứa toàn bộ Google Service Account credentials dạng TOML `[google_credentials]`
- Cập nhật `.gitignore` — thêm `.streamlit/secrets.toml`
- `requirements.txt` và `.streamlit/config.toml` đã có từ phiên 22, không cần tạo thêm

**B. Git & GitHub**
- `git init` → commit 44 files → commit hash `855ea9f` "Initial commit: Kha Son Green Home CRM"
- Tạo repo `kha-son-crm` trên GitHub tại `https://github.com/mhien588-arch/kha-son-crm.git`
- Push thành công toàn bộ codebase (trừ các file gitignored)

**C. Deploy Streamlit Community Cloud**
- Vào `share.streamlit.io` → New app → chọn repo `kha-son-crm` → branch `main` → main file: `dashboard.py`
- Advanced settings → Secrets → paste nội dung `.streamlit/secrets.toml`
- **Lỗi "This repository does not exist"**: Streamlit OAuth chỉ có quyền `Access public repositories`, không truy cập được private repo
- **Fix**: Đổi repo từ **private → public** (an toàn: credentials gitignored, code không nhạy cảm)
- **App live**: `https://kha-son-crm-k3tfrnb488ckvq4nb5xsm7.streamlit.app`
- Xác minh: Dashboard load đúng, hiện 65 khách hàng, phễu + leaderboard hoạt động

**D. Đổi Tên App**
- Sửa `dashboard.py` dòng 20: `page_title="CRM BKD2"` (trước: "Kha Sơn Green Home — CRM Dashboard")
- Push commit `6a56ef8` → Streamlit Cloud tự động deploy lại

**E. Hướng dẫn Thêm vào Màn Hình Chính**
- **Android (Chrome)**: Menu 3 chấm → "Thêm vào màn hình chính"
- **iPhone**: Phải dùng **Safari** (không phải Chrome — Chrome iOS không có tính năng này) → nút Share ↑ → "Thêm vào màn hình chính"
- Xác nhận: Hiển đã cài thành công trên iPhone qua Safari

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| "This repository does not exist" trên Streamlit | Repo private; Streamlit OAuth app chỉ có quyền `public_repo` | Đổi repo thành public — credentials đã gitignored nên không có rủi ro |
| Chrome iOS không có "Thêm vào màn hình chính" | Apple/Chrome iOS giới hạn tính năng PWA — chỉ Safari được phép | Dùng Safari thay Chrome trên iPhone/iPad |
| Git không nhận lệnh trong PowerShell | PATH chưa refresh sau khi cài Git for Windows | Dùng đường dẫn đầy đủ `C:\Program Files\Git\cmd\git.exe` |

**Quyết định kiến trúc phiên 23:**

| Quyết định | Lý do |
|-----------|-------|
| Đổi repo từ private → public | Streamlit Community Cloud free tier chỉ hỗ trợ public repo; credentials đã gitignored, code không chứa thông tin nhạy cảm |
| `_get_credentials()` backward-compatible | Local system hoàn toàn không bị ảnh hưởng; chỉ cloud path mới dùng Streamlit Secrets — không cần sửa gì ở tracker.py hay các script khác |
| `page_title="CRM BKD2"` | Tên ngắn gọn, phù hợp icon màn hình điện thoại; "Kha Sơn Green Home — CRM Dashboard" quá dài, bị cắt bớt khi hiện icon |
| Dùng Safari thay Chrome trên iPhone | Giới hạn của Apple/Chrome iOS — đây là yêu cầu hệ thống, không phải lựa chọn |
| Không dùng GitHub App (chỉ OAuth) | Đơn giản hơn; public repo đủ cho nhu cầu; không cần cấp quyền rộng hơn |

**Giới hạn của Streamlit Community Cloud (cần lưu ý):**
- App **ngủ sau 7 ngày** không dùng → lần mở đầu sau khi ngủ chậm ~30 giây (tự thức dậy)
- **Filesystem không persistent** → backup CSV cục bộ (`backup_to_csv()`) không hoạt động trên cloud — chỉ chạy trên máy tính
- Mọi thay đổi `config.json` (sale team, remind days) vẫn phải thực hiện qua `tracker.py` trên máy tính → commit → push → Streamlit Cloud tự deploy lại

---

## BƯỚC TIẾP THEO (phiên làm việc sau)

### Giai đoạn 1 — Hoàn thành ✅ (phiên 10)

Tất cả tính năng vá lỗ hổng đã được triển khai và xác minh thực tế:
- ✅ **1A** — Kiểm tra trùng SĐT (cả CRM lẫn staging)
- ✅ **1B** — Tìm kiếm theo SĐT, menu [8]
- ✅ **1D** — Validate SĐT regex `^0\d{9}$`
- ✅ **Staging tab "SỐ MỚI KS"** — lead inbox, checkbox, auto-transfer
- ✅ **Staging bug fixes** — append đúng row, giữ số 0 SĐT, load lọc dòng giả (phiên 10)
### Tài Liệu — Hoàn thành ✅ (phiên 13)

- ✅ Huong_Dan_Truong_Nhom.docx — 10 chương, vận hành tổng hợp cho Hiển
- ✅ Huong_Dan_Nhan_Su.docx — 9 chương, onboarding nhân viên mới (+ kịch bản telesale)
- ✅ make_huong_dan_v2.py — script tái tạo lại 2 file Word bất cứ lúc nào
- ✅ Xóa Huong_Dan_Van_Hanh_CRM.docx + make_huong_dan.py (file cũ)

**Bước tiếp theo cần làm (phiên sau):**
- ✅ **Bug menu [4]**: Đã fix phiên 14 — thêm lead mới hoạt động bình thường
- ✅ **Bug transfer vị trí sai (I92:P93)**: Đã fix phiên 15 — lead chuyển từ SỐ MỚI KS vào đúng dòng tiếp theo của bảng CRM
- ✅ **Tính năng đảo số random**: Đã thêm phiên 15 — menu [7][d] toggle, hiện tại đang bật chế độ `random`
- ✅ **Date picker cột G, H**: Đã thêm phiên 16 — calendar picker tự động khi click vào ô ngày
- ✅ **Logic quá hạn / giữ tương tác**: Đã tách phiên 16 — khách KNC không còn bị báo quá hạn; section vàng nhắc re-engage sau 14 ngày
- ✅ **Bug crash tracker.py khi staging có dữ liệu**: Đã fix phiên 17 — `load_staging_data()` dùng `COLUMNS[:8]`; hệ thống khởi động bình thường
- ✅ **Lịch sử sale khi chuyển lead**: Đã thêm phiên 18 — [7][e] tự ghi `[DD/MM Sale: Cũ→Mới]` vào Ghi chú, tích lũy qua nhiều lần chuyển
- ✅ **Bug row-index trong `chuyen_leads_giua_sale()` và `cap_nhat_trang_thai()`**: Đã fix phiên 19 — `load_data()` dùng sheet-row thực tế làm index; không còn xóa/update sai hàng khi CRM có hàng không tên
- ✅ **13 leads bị mất đã được khôi phục (phiên 20)**: Dùng ảnh chụp tab SỐ MỚI KS làm nguồn → reimport 14 leads vào CRM trực tiếp qua script `_reimport_chi_dung.py` (đã xóa sau khi dùng). CRM hiện có **72 leads**, Chị Dung: 18 leads.
- ✅ **Hướng dẫn tổng quan PDF (phiên 20)**: Tạo `Huong_Dan_Toan_Dien_CRM.docx` + `.pdf` — 8 phần đầy đủ bao gồm 10 lỗi thường gặp, hướng dẫn sửa thủ công và checklist xử lý sự cố.
- ✅ **Bug TypeError int64 khi chuyển lead (phiên 21)**: Đã fix `sheets_connector.py:98` — `delete_crm_row()` dùng `int()` convert numpy.int64 → Python int; menu [7][e] hoạt động bình thường.
- ✅ **Deploy Dashboard lên Streamlit Cloud (phiên 23)**: App live tại `https://kha-son-crm-k3tfrnb488ckvq4nb5xsm7.streamlit.app` — team truy cập từ điện thoại.
- ✅ **Đổi tên app thành CRM BKD2 (phiên 23)**: `page_title="CRM BKD2"` trong `dashboard.py`, push lên GitHub, Streamlit Cloud auto-deploy.
- ✅ **Hiển đã cài app vào màn hình iPhone (phiên 23)**: Dùng Safari → Share → Thêm vào màn hình chính.
- ✅ **Tab DATA TELESALE (phiên 24)**: Tạo tab mới trong Sheets + Dashboard + tracker với 4 hàm sheets_connector mới; import 1125 số từ `Danh_sach_KD_chuyen_doi.md` → 1111 hàng hợp lệ, phân công đúng team theo config.json
- ✅ **Fix phân công sai team (phiên 24)**: Lần import đầu dùng Sơn/Tiến thay vì Chị Dung/Chương → tạo script `_fix_telesale_sale.py` đọc config.json, ghi lại cột D đúng team; đã xóa script temp sau khi dùng
- ✅ **Fix 6 bug sheets_connector.py (phiên 26)**: Đặc biệt bug `append_row()` `if v` filter gây mất dữ liệu; phục hồi 11/11 leads mất; CRM hiện 75 leads
- ⏳ **Hướng dẫn 5 thành viên còn lại cài app vào màn hình điện thoại**: Đức, Tuấn Anh, Nam, Chị Dung, Chương — Android dùng Chrome, iPhone dùng Safari → Share → Thêm vào màn hình chính. URL: `https://kha-son-crm-k3tfrnb488ckvq4nb5xsm7.streamlit.app`
- ⏳ **Team mở Google Sheets tab DATA TELESALE**: Mỗi sale lọc tên mình ở cột D → gọi từng số → tích ✓ cột I khi khách có nhu cầu → Hiển mở Dashboard tab 📞 hoặc nhấn [T] trong tracker để chuyển vào CRM
- ⏳ **Kích hoạt Task Scheduler**: Chạy `setup_task_scheduler.py` với quyền Admin trên máy Hiển → đăng ký task `KhaSon_NhacNhoSang` (nhắc nhở tự động 8:00 sáng T2–T7)
- ⏳ **In hoặc gửi file Word**: Gửi `Huong_Dan_Nhan_Su.docx` cho Chương và Chị Dung khi onboard; `Huong_Dan_Toan_Dien_CRM.pdf` cho Hiển tham khảo kỹ thuật
- ⏳ **Push config.json lên GitHub**: config.json hiện bị gitignore (bảo mật) — Streamlit Cloud dùng secrets.toml riêng, không cần push; nhưng khi team thay đổi cần cập nhật secrets.toml trên Streamlit Cloud portal
- ⏳ **zalo_notify.py**: Triển khai khi có Zalo OA Access Token từ business.zalo.me
- ⚠️ **Quy tắc bất biến TELESALE tab**: Tab DATA TELESALE chỉ có 8 cột dữ liệu A:H, cột I là checkbox. `append_telesale_rows()` dùng `COLUMNS[:8]`, `load_telesale_data()` dùng `COLUMNS[:8]`. Nếu thêm cột vào COLUMNS phải kiểm tra cả staging lẫn telesale.
- ⚠️ **KHÔNG bao giờ hardcode tên sale**: Luôn đọc từ `config.json` (lesson từ phiên 24 khi dùng Sơn/Tiến thay vì Chị Dung/Chương trong script import).
- ⚠️ **Quy tắc bất biến staging**: Nếu thêm cột mới vào `COLUMNS` trong tương lai, phải kiểm tra lại CẢ HAI `append_staging_row()` VÀ `load_staging_data()` — cả 2 đều phải dùng `COLUMNS[:8]`
- ⚠️ **Quy tắc bất biến int64**: Mọi hàm truyền DataFrame index vào gspread API phải wrap bằng `int()`. DataFrame index từ pandas luôn là `numpy.int64`, không phải Python `int`.
- ⚠️ **Quy tắc bất biến Streamlit Cloud**: Filesystem cloud không persistent → backup CSV chỉ chạy trên máy tính. Mọi thay đổi config vẫn phải qua tracker.py trên máy → commit → push.
- ⚠️ **Streamlit Cloud ngủ sau 7 ngày**: Nếu không ai dùng 7 ngày, lần mở tiếp theo chậm ~30 giây. Tự thức dậy, không mất data.

---

### Phiên 20 — 19/05/2026 — Khôi Phục 14 Leads & Tạo Hướng Dẫn PDF Tổng Quan

**Vấn đề phát sinh sau phiên 19:**
- 13 leads của Chị Dung bị mất vĩnh viễn do bug row-index (phiên 19 đã fix bug nhưng data đã mất)
- User chụp ảnh màn hình tab "SỐ MỚI KS" (gid=392590522) khi 17 leads còn trong staging → dùng làm nguồn khôi phục
- Chưa có tài liệu kỹ thuật tổng quan dành cho người vận hành: bao gồm lỗi thường gặp, cách sửa thủ công khi hệ thống hỏng

**Đã hoàn thành:**

**A. Khôi phục 14 leads Chị Dung — script `_reimport_chi_dung.py` (đã xóa)**
- Parse 17 dòng từ ảnh chụp staging tab → loại 3 leads đã có trong CRM (c Hường/0988472309, Anh Đặng/0978381911, A Hiếu/0385025848) → thêm 14 leads mới
- Xử lý chuẩn hóa Trạng thái không hợp lệ từ ảnh: `"Không có nhu cầu"` trong cột E → `Trạng thái="Đang chăm sóc"` + `Nhu cầu="Không còn nhu cầu"` cho A Thắng (0963147991) và Cường (0965238891)
- Append lịch sử `[19/05 Sale: Hien->Chi Dung]` vào Ghi chú của từng lead
- Gặp API rate limit (429) sau 12 leads — đợi 40 giây, chạy lại 2 leads còn lại thành công
- `highlight_new_row()` cho từng lead mới → in đậm trong Sheets
- **Kết quả: CRM 72 leads, Chị Dung 18 leads (4 cũ + 14 khôi phục)**

**B. Tạo hướng dẫn kỹ thuật tổng quan — `_make_guide_pdf.py` (đã xóa)**
- `Huong_Dan_Toan_Dien_CRM.docx` + `Huong_Dan_Toan_Dien_CRM.pdf` (192KB)
- **8 phần đầy đủ:**
  - Phần 1: Tổng quan (thư mục, Sheets, trạng thái hợp lệ)
  - Phần 2: Vận hành hàng ngày (sáng/chiều/tối/đầu tuần)
  - Phần 3: Menu [1]-[9] tracker.py — mục đích + lưu ý cho từng menu
  - Phần 4: Luồng lead mới 5 bước
  - Phần 5: **10 lỗi thường gặp** — UnicodeError, GSpreadException, APIError 400/429, ValueError, transfer sai vị trí, bug row-index, SĐT mất số 0, lead vào row 201, module not found
  - Phần 6: Hướng dẫn sửa thủ công trong Google Sheets (xóa/thêm/sửa dòng, backup, kiểm tra cột lệch)
  - Phần 7: 5 Quy tắc bất biến (không xóa creds, không cộng +2, COLUMNS[:8], SĐT regex, không thêm cột tùy tiện)
  - Phần 8: Checklist xử lý sự cố + thông tin liên hệ
- Convert PDF dùng PowerShell Word COM automation (`SaveAs wdFormatPDF=17`) — Word crash ở bước `Quit()` nhưng PDF đã lưu thành công trước đó

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `APIError [429] Quota exceeded` | Script gọi `append_row()` + `highlight_new_row()` liên tiếp cho 12 leads — vượt rate limit Google | Tách thành 2 batch, đợi 40 giây giữa 2 batch |
| `docx2pdf` không dùng được — `No module named pywintypes` | `docx2pdf` cần `pywin32` nhưng chưa cài | Dùng PowerShell COM trực tiếp: `$word.Documents.Open()` + `SaveAs([ref]$pdf, [ref]17)` |
| Word COM lỗi `Quit()` (HRESULT 0x800706BE) | Word crash khi đóng sau khi SaveAs — do COM automation trên Python session | PDF đã được lưu trước lỗi; lỗi chỉ ở bước `Quit()` — ignore an toàn |

**Quyết định kiến trúc phiên 20:**

| Quyết định | Lý do |
|-----------|-------|
| Dùng ảnh chụp staging tab làm nguồn reimport (không nhập tay từng số) | Ảnh chứa đủ 17 leads với SĐT, Nguồn, Trạng thái, Ghi chú, ngày — parse 1 lần thay vì nhập 14 lần qua menu [4] |
| Thêm trực tiếp vào CRM qua `append_row()` (không qua staging) | Chị Dung đã gọi tất cả leads rồi (đây là khôi phục, không phải leads mới) → không cần bước xác nhận staging |
| Ghi lịch sử `[Hien->Chi Dung]` vào Ghi chú của leads khôi phục | Nhất quán với cơ chế phiên 18; sale biết leads này từ Hiển chuyển sang; không mất dấu lịch sử |
| Tạo guide mới `Huong_Dan_Toan_Dien_CRM` riêng (không cập nhật 2 file cũ) | File mới tập trung vào kỹ thuật + lỗi thường gặp — đối tượng khác với Huong_Dan_Truong_Nhom (quy trình) và Huong_Dan_Nhan_Su (onboarding). 3 file phục vụ 3 mục đích khác nhau. |
| Tạo cả .docx lẫn .pdf | PDF dễ đọc + in ấn cho người không cần sửa; .docx để cập nhật khi phiên sau có thêm lỗi mới |

---

### Phiên 21 — 20/05/2026 — Fix Bug TypeError int64 khi Chuyển Lead

**Vấn đề phát sinh sau phiên 20:**
- Chạy tracker.py → menu [7][e] Chuyển lead giữa sale → crash với lỗi:
  `TypeError: Object of type int64 is not JSON serializable`
- Traceback: `chuyen_leads_giua_sale()` → `delete_crm_row(sr)` → `ws.delete_rows(sheet_row_index)` → gspread serialize JSON body → crash

**Nguyên nhân gốc:**
- `load_data()` tạo DataFrame với `index=sheet_row_indices` (list Python `int` thông thường từ `enumerate`)
- Pandas tự động cast list đó thành `numpy.int64` khi làm DataFrame index — đây là hành vi mặc định của pandas
- Khi lọc `sale_df = df[df["Sale chăm sóc"] == nguon_sale]`, index của kết quả vẫn là `numpy.int64`
- `selected_indices` lấy từ `sale_df.index` → mỗi `sr` là `numpy.int64`
- Gspread truyền thẳng vào `json.dumps()` → `numpy.int64` không phải JSON-serializable → crash
- Hàm `update_row()` không bị: dùng f-string `f"A{sheet_row_index}:I{sheet_row_index}"` → Python tự convert; chỉ `delete_rows()` bị vì nhận argument trực tiếp vào hàm gspread

**Đã hoàn thành:**
- Sửa `sheets_connector.py` dòng 98 — `delete_crm_row()`:
  - **Trước:** `ws.delete_rows(sheet_row_index)`
  - **Sau:** `ws.delete_rows(int(sheet_row_index))`
- `int()` convert `numpy.int64` → Python native `int` → JSON serializable; không ảnh hưởng nếu argument đã là `int` thông thường (no-op)
- Sửa tại boundary function (không sửa caller): bảo vệ tập trung 1 chỗ, mọi caller tương lai đều được bảo vệ tự động
- Cập nhật `Huong_Dan_Toan_Dien_CRM.docx` + `.pdf` — bổ sung lỗi int64 vào Phần 5

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `TypeError: Object of type int64 is not JSON serializable` | Pandas DataFrame index → `numpy.int64`; gspread không serialize được khi gọi `ws.delete_rows()` | Thêm `int()` trong `delete_crm_row()` để convert sang Python native int |

**Quyết định kiến trúc phiên 21:**

| Quyết định | Lý do |
|-----------|-------|
| Sửa tại `delete_crm_row()` (không sửa caller `chuyen_leads_giua_sale()`) | `delete_crm_row()` là interface function — bảo vệ tại đây đảm bảo mọi caller đều an toàn, kể cả caller tương lai được thêm vào |
| Dùng `int()` (không dùng `.item()` hay `.astype(int)`) | `int()` là Python built-in, rõ ràng, hoạt động với cả `numpy.int64` lẫn `int` thông thường (no-op); `.item()` chỉ có trên numpy array, dễ gây nhầm |

**Quy tắc bất biến sau phiên 21:**
> Mọi hàm nhận DataFrame index và truyền vào gspread API phải wrap bằng `int()`. Pandas index luôn là `numpy.int64`, không phải Python `int`. Hiện tại chỉ `delete_crm_row()` cần; nếu thêm hàm mới dùng `.delete_rows()` hoặc `.delete_columns()` trong tương lai, phải áp dụng cùng pattern.

---

### Phiên 22 — 20/05/2026 — Bảo mật, Tự Động Sao Lưu CSV, Kết Nối Retry, Web Dashboard Streamlit Chuẩn Navy & Fix Định Dạng SĐT

**Vấn đề phát sinh & Yêu cầu mới:**
- Cần bảo mật file credentials nhạy cảm (`google_creds.json`, `config.json`) và các bản sao lưu.
- Khắc phục triệt để lỗi Google Sheets API 429 Quota Exceeded (giới hạn tần suất gọi).
- Thiết lập quy trình tự động sao lưu dữ liệu CRM hàng ngày sang file CSV cục bộ để dự phòng.
- Xây dựng giao diện Web Dashboard sang trọng chuẩn Navy `#0D47A1` thay thế/bổ sung cho giao diện Tracker terminal cũ.
- Khắc phục lỗi định dạng SĐT trong Sheets khi ghi hoặc cập nhật (mất số 0 ở đầu) và lỗi hiển thị thô (indented code block do thừa khoảng trắng HTML trong Streamlit).

**Đã hoàn thành:**

**A. Bảo mật & Resiliency (Giai đoạn 1)**
- Tạo `.gitignore` bảo vệ `data/google_creds.json`, `config.json`, và thư mục sao lưu `data/backups/`.
- Thiết lập `@retry_api_call` decorator với thuật toán **Exponential Backoff** tự động bắt lỗi API 429 và thử lại (ngủ 2s, 4s, 8s...).
- Tạo cơ chế tự động sao lưu `backup_to_csv()` ghi dữ liệu thành file CSV có UTF-8-BOM (`utf-8-sig`) hàng ngày tại `data/backups/`. Tích hợp trực tiếp vào đầu quy trình chạy báo cáo của `daily_report.py` và `nhac_sang.py`.

**B. Web Dashboard CRM Đa Năng (Giai đoạn 3 / 4)**
- Phát triển `dashboard.py` sử dụng Streamlit & Plotly với 5 tab chức năng:
  - **Tab 1: Báo cáo & Tổng quan**: KPI cards, biểu đồ phễu Plotly mượt mà, bảng xếp hạng Leaderboard, cảnh báo quá hạn.
  - **Tab 2: Danh sách Leads CRM**: Bộ lọc nâng cao, tìm kiếm thông minh, biểu mẫu Chỉnh sửa nhanh đồng bộ Sheets thời gian thực, Form thêm lead mới có kiểm tra trùng SĐT.
  - **Tab 3: Số mới chờ duyệt (Staging)**: Xem danh sách leads từ marketing đẩy vào, duyệt và chuyển tự động vào CRM chính.
  - **Tab 4: Nhập số hàng loạt & Chia Sale**: Hỗ trợ nhập thô dạng `Tên - SĐT`, `Tên, SĐT`, hoặc SĐT đơn lẻ; tự động lọc trùng chéo và chia Sale ngẫu nhiên/xoay vòng.
  - **Tab 5: Cấu hình hệ thống**: Quản lý Sale roster, tùy chỉnh ngày nhắc nhở chăm sóc, chuyển giao leads số lượng lớn giữa các sale.

**C. Sửa Lỗi Định Dạng Số Điện Thoại & Hiển Thị Bảng HTML**
- Thêm định dạng hiển thị khoảng cách thân thiện cho SĐT: `0982 287 863`.
- Ép thuộc tính `value_input_option="RAW"` ở **TẤT CẢ** các hàm cập nhật sheets (`append_row()`, `append_staging_row()`, `update_row()`) trong `sheets_connector.py` để ngăn Sheets tự ý đổi SĐT thành dạng số (làm mất số 0 hoặc biến dạng số mũ).
- Tạo bộ dọn HTML `clean_html()` để loại bỏ hoàn toàn khoảng trắng thụt lề dòng đầu trong chuỗi HTML, tránh lỗi Streamlit hiểu nhầm thành khối code Markdown.

**D. Shortcuts & Launchers Tiện Lợi**
- Tạo shortcut Desktop `C:\Users\PC\Desktop\Mo CRM Kha Son.bat` tự động kiểm tra cổng 8501. Nếu đã chạy thì mở ngay trình duyệt, nếu chưa thì kích hoạt Streamlit bằng Python 3.13.

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `APIError 429 RESOURCE_EXHAUSTED` | Gọi API Google quá nhiều lần liên tiếp khi đồng bộ dữ liệu | Sử dụng decorator `@retry_api_call` để tự động nghỉ và thử lại với thời gian tăng dần |
| SĐT mất số 0 ở đầu khi update/save | API Sheets tự động chuyển chuỗi số thành kiểu Numeric khi dùng USER_ENTERED mặc định | Đổi tham số thành `value_input_option="RAW"` trong cả `append_row()` và `update_row()` |
| Streamlit hiển thị mã nguồn bảng HTML thay vì render bảng | Khoảng trắng thụt dòng (indentation) trong chuỗi HTML đa dòng khiến Streamlit render thành Code Block | Sử dụng hàm `clean_html()` dọn dẹp triệt để `line.lstrip()` trước khi ghi ra Streamlit |

**Quyết định kiến trúc phiên 22:**

| Quyết định | Lý do |
|-----------|-------|
| Dùng Python 3.13 cho Streamlit Dashboard | Python 3.14 (mặc định máy) chưa hỗ trợ đầy đủ thư viện Streamlit/Plotly, Python 3.13 đã được cài đặt đầy đủ các package |
| Ép cứng RAW cho `update_row()` | Đảm bảo ngay cả khi chỉnh sửa thông tin khác của khách, SĐT của họ trong Sheet cũng không bao giờ bị biến đổi thành số thường |
| Tách biệt `.gitignore` | Bảo vệ an toàn dữ liệu khách hàng và key API nhạy cảm khi đưa lên mã nguồn mở |

**Quy tắc bất biến sau phiên 22:**
> 1. Luôn sử dụng `value_input_option="RAW"` cho mọi thao tác ghi/cập nhật SĐT trên Google Sheets để bảo toàn số 0 ở đầu.
> 2. Mọi HTML render trên Streamlit phải đi qua bộ lọc `clean_html()` để loại bỏ thụt đầu dòng, tránh kích hoạt bộ render code block của Markdown.
> 3. Streamlit App được vận hành trên Python 3.13 (gọi trực tiếp `python3.13 -m streamlit...` hoặc chạy qua file `.bat`).

---

### Giai đoạn 4 — Mở rộng (tháng 6+)

12. **Facebook Lead Ads tự động** — Lead Ads → Zapier/Make → Google Sheets append tự động, không cần nhập tay (~$20/tháng, khi > 50 lead/tuần)
13. **Multi-project** — Chọn dự án khi khởi động tracker (khi có dự án BĐS thứ 2)

---

### Phiên 24 — 21/05/2026 — Tab DATA TELESALE & Import 1111 Số Cold-call

**Vấn đề phát sinh & Yêu cầu mới:**
- Team cần gọi điện cold-call từ danh sách số bên ngoài (không phải từ Ads Facebook)
- Hiển cung cấp file `Danh_sach_KD_chuyen_doi.md` chứa 3 danh sách KD1/KD2/KD3 (~1173 số)
- Cần: hệ thống phân công sale → sale gọi → tích ✓ số có nhu cầu → tự động chuyển vào CRM với trạng thái "Đang chăm sóc"

**Đã hoàn thành:**

**A. Tính năng DATA TELESALE — 3 file (xây dựng từ kế hoạch phiên trước)**

`sheets_connector.py` — 4 hàm mới + 1 hằng số:
- `TELESALE_TAB = "DATA TELESALE"`
- `ensure_telesale_tab()` — tạo tab với header cam `#E65100`, freeze row 1, BOOLEAN checkbox cột I rows 2-200; tái dùng pattern `ensure_staging_tab()`
- `append_telesale_rows(rows_list)` — ghi nhiều dòng cùng lúc; dùng `col_values(1)` tính next_row (tránh checkbox phantom), `RAW` mode giữ số 0 SĐT, chỉ ghi `COLUMNS[:8]`
- `load_telesale_data()` — đọc A:I, filter dòng trống col A, trả DataFrame COLUMNS[:8] + sheet_row_indices
- `transfer_telesale_checked()` — tìm col I == "TRUE" → append CRM với "Đang chăm sóc" + today date → highlight_new_row() → xóa ngược thứ tự từ telesale

`dashboard.py` — tab "📞 Data Telesale" (thứ 4 trong menu):
- Section A: nhập số mới (text_area, validate SĐT, lọc trùng 3 cấp: lô + CRM + telesale, preview bảng, chọn sale)
- Section B: danh sách đang chờ + button "Chuyển leads đã tích ✓ vào CRM"

`tracker.py` — tích hợp telesale:
- `_show_telesale_banner()` — banner magenta "📞 DATA TELESALE: X số chờ gọi" ở startup
- `xu_ly_data_telesale()` — menu `[T]`: gọi `transfer_telesale_checked()`, in tên đã chuyển, reload df

**B. Import 1125 số từ `Danh_sach_KD_chuyen_doi.md`**
- Parse 3 danh sách KD1/KD2/KD3 từ file markdown (pipe-delimited table)
- Chuẩn hóa SĐT: extract digits → strip prefix 84 → pad 9-digit → validate 10-digit bắt đầu 0
- Lọc trùng 3 cấp: 27 số trùng trong lô, 2 số trùng CRM → còn 1125 số hợp lệ
- Phân công round-robin cho 5 sale (trừ Hiển)
- Batch write 100 dòng/lần + delay 2 giây → tránh API 429
- Tab tự resize từ 200 → 1175 rows để chứa đủ dữ liệu

**C. Fix lỗi phân công sai — script `_fix_telesale_sale.py` (đã xóa)**
- Lỗi: script import dùng `SALE_TEAM = ["Đức", "Sơn", "Tuấn Anh", "Nam", "Tiến"]` hardcode — Sơn và Tiến không còn trong team (config.json có Chị Dung và Chương)
- Fix: đọc `config.json`, lọc Hiển → `['Đức', 'Tuấn Anh', 'Nam', 'Chị Dung', 'Chương']`
- Đọc lại 1111 dòng có tên trong col A (1125 - 14 dòng chỉ có SĐT không tên)
- Ghi lại cột D toàn bộ trong 3 batch 500 dòng
- **Kết quả cuối: Đức:223 / Tuấn Anh:222 / Nam:222 / Chị Dung:222 / Chương:222**

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| Phân công sai Sơn/Tiến thay vì Chị Dung/Chương | Script import hardcode tên sale, không đọc config.json | Tạo `_fix_telesale_sale.py` đọc config.json, ghi lại cột D |
| `UnicodeEncodeError` khi chạy Python trong Bash/PowerShell | Terminal mặc định CP1252 | Dùng `$env:PYTHONIOENCODING = "utf-8"` trước lệnh python |

**Quyết định kiến trúc phiên 24:**

| Quyết định | Lý do |
|-----------|-------|
| **LUÔN đọc sale_team từ config.json** (không hardcode) | Lesson học xương máu: hardcode tên sale dẫn đến phân công sai toàn bộ; config.json là nguồn duy nhất cho team |
| `col_values(1)` đếm next_row cho telesale | Tái dùng pattern phiên 10 — checkbox BOOLEAN cột I tạo phantom rows nếu dùng `append_rows()` |
| `COLUMNS[:8]` cho telesale | Tab DATA TELESALE có cấu trúc giống staging: 8 cột data, cột I là checkbox; nhất quán với `append_staging_row()` |
| Header cam `#E65100` cho DATA TELESALE | Phân biệt rõ: CRM navy `#0D47A1`, staging vàng `#FFF9C4`, telesale cam `#E65100` |
| Batch 100 rows + delay 2s khi import hàng nghìn dòng | Google Sheets API có quota 300 requests/60s; batch nhỏ + delay tránh 429 RESOURCE_EXHAUSTED |
| Xóa script temp sau khi dùng | `_import_telesale_kd.py` và `_fix_telesale_sale.py` là one-time use; giữ lại làm rác repo |

**Quy tắc bất biến sau phiên 24:**
> `DATA TELESALE` tab có cấu trúc tương tự `SỐ MỚI KS`: 8 cột data (A:H), cột I là checkbox (✓ Chuyển CRM). Tất cả hàm đọc/ghi đều dùng `COLUMNS[:8]`. Khi thêm cột mới vào `COLUMNS`, kiểm tra ĐỦ 3 chỗ: `append_staging_row()`, `load_staging_data()`, `append_telesale_rows()`, `load_telesale_data()`.
> KHÔNG bao giờ hardcode tên sale trong script — luôn đọc `config.json`.

### Phiên 25 — 21/05/2026 — Bộ công cụ Hỗ trợ Tư vấn Khách hàng (Tích hợp YAML, CLI & Streamlit)

**A. Thiết kế Gói `consultation/` Độc Lập**
- `templates.yaml` — 4 nhóm chủ đề thực chiến đầy đủ:
  - Telesale gọi lần đầu: A (Khơi gợi), B (Tạo khan hiếm), C (Tích sản).
  - Nhắn tin Zalo: A (Sau khi xem đất), B (Tiến độ hạ tầng), C (Sắp tăng giá).
  - Xử lý từ chối đối thoại ngắn "Khách nói -> Sale đáp" (Chê đắt, Lo pháp lý, Chê xa, Suy nghĩ thêm).
  - Quy trình 4 bước chinh phục khách hàng thực chiến.
- `loader.py` — đọc YAML và nạp `project` config từ `config.json`. Thế placeholders ({du_an}, {hotline}, v.v.) và tự động cá nhân hóa `{ten_sale}`. Có sử dụng bộ nhớ đệm `@lru_cache(maxsize=1)` tối ưu hóa đọc đĩa.
- `cli.py` — console CLI tương tác cực đẹp bằng colorama, hỗ trợ chạy nhanh qua phím tắt hoặc tham số dòng lệnh.

**B. Tích Hợp Web Dashboard Streamlit (`dashboard.py`)**
- Tab "💡 Kịch Bản Tư Vấn" (thứ 6 trong menu Sidebar).
- Layout 2 cột: Cột trái thiết lập (Chọn Sale hoạt động, Chọn chủ đề, Chọn kịch bản mẫu); Cột phải hiển thị kết quả.
- Tự động lấy tên Sale đã chọn điền vào `{ten_sale}` trong mẫu kịch bản.
- Render trực quan dạng Markdown trong thẻ `.premium-card` màu Navy sang trọng.
- Tích hợp hộp `st.code` sao chép nhanh kịch bản 1 chạm (One-click copy).

**C. Liên Kết Hệ Thống & Shortcut Bat**
- Thêm Lựa chọn `[4]` vào `content_helper.py` để kết nối trực tiếp đến CLI tư vấn.
- Tạo `Tư Vấn Mẫu Câu.bat` trên Windows chạy siêu tốc CLI với thiết lập mã hóa UTF-8 chống lỗi font.
- Cập nhật `Viet Content.bat` với bảng mã UTF-8 nhất quán.

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| `ModuleNotFoundError: No module named 'yaml'` | Thiếu thư viện PyYAML trong môi trường chạy | Chạy lệnh `pip install pyyaml` cho cả Python 3.13 và 3.14. Thêm `pyyaml` vào `requirements.txt`. |
| `UnicodeEncodeError` khi in emoji trong topic name | Python in unicode ra Terminal CP1252 của Windows | Gán env `set PYTHONIOENCODING=utf-8` trong file BAT và hướng dẫn người dùng. |

**Quyết định kiến trúc phiên 25:**

| Quyết định | Lý do |
|-----------|-------|
| Lưu kịch bản trong file YAML tách biệt | Dễ bảo trì, quản trị viên có thể tự thêm bớt kịch bản trong templates.yaml mà không cần biết lập trình Python. |
| Dùng `st.code` làm hộp copy | Tính năng copy gốc của Streamlit vô cùng ổn định, hỗ trợ đa nền tảng tốt hơn JS hack. |
| Cá nhân hóa dựa trên `sale_team` đã cấu hình | Đảm bảo nhanh gọn, đồng bộ thông tin và tránh lỗi gõ sai tên Sale. |

---

### Phiên 26 — 21/05/2026 — Fix 6 Bug sheets_connector.py & Phục Hồi 11 Leads Mất

**Vấn đề phát sinh sau phiên 25:**
- Sau khi team tích ✓ 10 số trong DATA TELESALE và chạy transfer: CRM giảm từ 65 → 64 (mất 1), chỉ 1/10 leads telesale thực sự vào CRM (Nhiên Kiệt 0983863869)
- 2 leads CRM gốc bị mất: thạch thảo (0374693102, Chị Dung) và Bích Hân (0975504447, Tuấn Anh)
- 9/10 leads telesale (Đức) bị xóa khỏi telesale nhưng không vào được CRM

**Nguyên nhân gốc — Bug `append_row()` (CRITICAL):**
- `next_row = len([v for v in ws.col_values(1) if v]) + 1` — filter `if v` bỏ qua gap rows (hàng có cột A trống trong vùng data)
- CRM có 1 hàng gap (ở giữa, không phải cuối) → undercount 1 → `next_row` trỏ vào hàng đã có data
- Cả 10 lần `append_row()` trong transfer đều ghi vào cùng 1 row (row 67) → ghi đè nhau + ghi đè lead gốc
- Kết quả: thạch thảo và Bích Hân mất; 9/10 telesale leads mất; chỉ Nhiên Kiệt (ghi cuối cùng) còn lại

**Đã hoàn thành — 6 Fix trong sheets_connector.py:**

| Fix | Hàm | Thay đổi |
|-----|-----|---------|
| **1 (CRITICAL)** | `append_row()` | Đổi `len([v for v in col_values(1) if v])` → `len(col_values(1))` — KHÔNG filter `if v`, tính đủ kể cả gaps |
| 2 | `load_data()` | Đổi filter chỉ cột A → cả A lẫn B: skip chỉ khi CẢ HAI trống; lead không có tên nhưng có SĐT vẫn được tải |
| 3 | `load_telesale_data()` | Đổi filter chỉ cột A → cả A lẫn B (14 rows import không tên bị ẩn khỏi dashboard) |
| 4 | `append_telesale_rows()` | Thêm batch writes 50 dòng + 1s delay để tránh API 429 |
| 5 | `transfer_telesale_checked()` | Xóa `@retry_api_call` cấp function — nếu delete phase 429 và retry, `append_row` chạy lại → duplicate CRM; thêm helper `_delete_ws_row()` có retry riêng |
| 6 | `ensure_telesale_tab()` | Tạo tab mới với 1500 rows (không phải 200) + checkbox toàn range rows 2-1500 |

**Phục hồi dữ liệu:**
- 2 leads CRM từ backup `crm_backup_2026-05-21.csv`: thạch thảo (Chị Dung) + Bích Hân (Tuấn Anh)
- 9 leads telesale (Đức): ghép tên theo thứ tự task output với SĐTs từ kiểm tra telesale tab; phân công Đức, Trạng thái "Đang chăm sóc"
- 1 lead không tên (0986679891): cập nhật tên placeholder "(Không rõ tên)" trong col A để `load_data()` không bỏ qua
- **Kết quả: CRM 64 → 75 leads; tất cả 11/11 leads phục hồi thành công**

**Lỗi phát sinh và cách xử lý:**

| Lỗi | Nguyên nhân | Cách fix |
|-----|------------|----------|
| CRM -1 lead sau transfer 10 rows | `append_row()` `if v` filter gây ghi đè data — phát hiện nhờ so sánh backup vs current | Fix 1: bỏ filter `if v` trong `col_values(1)` |
| 14 rows telesale ẩn khỏi dashboard | `load_telesale_data()` filter chỉ col A → bỏ qua rows có SĐT nhưng không tên | Fix 3: filter cả 2 cột |
| Potential duplicate CRM khi transfer bị 429 | `@retry_api_call` ở toàn hàm `transfer_telesale_checked()` → retry = append lại | Fix 5: tách retry xuống từng thao tác |

**Quyết định kiến trúc phiên 26:**

| Quyết định | Lý do |
|-----------|-------|
| `len(col_values(1))` KHÔNG filter | `col_values(1)` đã xử lý trailing empty cells — chỉ trả về đến row cuối có data; filter `if v` nguy hiểm khi có gap row ở giữa |
| Backup CSV trước mỗi transfer quan trọng | `backup_to_csv()` đã có từ phiên 22, phiên 26 xác nhận backup cứu data sau sự cố |
| Placeholder "(Không rõ tên)" cho lead tên trống | `load_data()` không bỏ qua lead này; sale có thể nhận ra và cập nhật tên đúng sau |
| Script phục hồi one-shot, xóa sau khi dùng | Pattern nhất quán từ phiên 24: script temp đặt tên `_tên.py`, xóa sau khi dùng xong |

**Quy tắc bất biến sau phiên 26:**
> **KHÔNG BAO GIỜ dùng `if v` filter khi gọi `col_values()` để tính `next_row`.** `col_values()` đã dừng ở row cuối có data; filter `if v` bỏ qua gap row ở giữa → undercount → ghi đè data hiện có. Luôn dùng `len(ws.col_values(N)) + 1` (không filter). Hiện áp dụng đúng ở: `append_row()`, `append_staging_row()`, `append_telesale_rows()`.

