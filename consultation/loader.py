import os
import json
import yaml
from functools import lru_cache

# Đường dẫn tương đối ổn định tới config.json và templates.yaml
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates.yaml")
CONFIG_PATH = os.path.join(os.path.dirname(BASE_DIR), "config.json")

def load_project_config():
    """Tải thông tin dự án từ config.json"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("project", {}), cfg.get("sale_team", [])
    except Exception as e:
        print(f"Cảnh báo: Không thể tải config.json ({e})")
    
    # Giá trị mặc định nếu có lỗi hoặc file không tồn tại
    return {
        "ten_du_an": "Kha Sơn Green Home",
        "hotline": "0368.557.832",
        "khu_vuc": "KCN Phú Bình, Thái Nguyên",
        "gia_tu": "chỉ từ 800 triệu",
        "dien_tich": "80–120m²",
        "phap_ly": "Sổ đỏ lâu dài, pháp lý minh bạch"
    }, ["Hiển", "Đức", "Tuấn Anh", "Nam", "Chị Dung", "Chương"]

@lru_cache(maxsize=1)
def load_raw_templates():
    """Tải và parse file templates.yaml với chế độ cache"""
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Không tìm thấy file kịch bản tư vấn tại: {TEMPLATE_PATH}")
    
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Lỗi phân tích cú pháp YAML trong templates.yaml: {e}")

def get_topics():
    """Lấy danh sách các chủ đề kịch bản"""
    try:
        data = load_raw_templates()
        return [item["topic"] for item in data if "topic" in item]
    except Exception as e:
        print(f"Lỗi khi lấy danh sách chủ đề: {e}")
        return []

def get_templates_by_topic(topic_name):
    """Lấy danh sách kịch bản thuộc một chủ đề cụ thể"""
    try:
        data = load_raw_templates()
        for item in data:
            if item.get("topic") == topic_name:
                return item.get("items", [])
    except Exception as e:
        print(f"Lỗi khi lấy kịch bản theo chủ đề {topic_name}: {e}")
    return []

def render_template_content(content_str, sale_name=None):
    """
    Điền các thông số động vào kịch bản tư vấn.
    Nếu placeholder không có trong config, sử dụng giá trị mặc định an toàn.
    """
    proj_cfg, _ = load_project_config()
    
    # Khởi tạo các giá trị thay thế (placeholders)
    placeholders = {
        "du_an": proj_cfg.get("ten_du_an", "Kha Sơn Green Home"),
        "hotline": proj_cfg.get("hotline", "0368.557.832"),
        "khu_vuc": proj_cfg.get("khu_vuc", "KCN Phú Bình, Thái Nguyên"),
        "gia_tu": proj_cfg.get("gia_tu", "chỉ từ 800 triệu"),
        "dien_tich": proj_cfg.get("dien_tich", "80–120m²"),
        "phap_ly": proj_cfg.get("phap_ly", "Sổ đỏ lâu dài, pháp lý minh bạch"),
        "ten_sale": sale_name if sale_name else "Chuyên viên tư vấn"
    }
    
    try:
        return content_str.format(**placeholders)
    except KeyError as e:
        # Trường hợp thừa placeholder lạ trong file YAML
        # Thay thế thủ công tránh crash hệ thống
        missing_key = str(e).strip("'")
        print(f"Cảnh báo: Phát hiện placeholder lạ {{{missing_key}}} trong kịch bản.")
        placeholders[missing_key] = f"[{missing_key.upper()}]"
        # Thử format lại với placeholder bổ sung
        return content_str.format(**placeholders)
