import os
import sys
from consultation.loader import get_topics, get_templates_by_topic, render_template_content, load_project_config

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = YELLOW = WHITE = RED = MAGENTA = BLUE = ""
    class Style:
        RESET_ALL = BRIGHT = ""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_separator(char="═", color=Fore.GREEN):
    print(color + char * 60)

def display_interactive_cli():
    # Tải danh sách sale hoạt động để chọn nhanh
    _, sale_team = load_project_config()
    
    # Cho chọn Sale
    clear_screen()
    print_separator("✦", Fore.CYAN)
    print(Fore.CYAN + Style.BRIGHT + "   BỘ CÔNG CỤ TƯ VẤN KHÁCH HÀNG - KHA SƠN GREEN HOME")
    print_separator("✦", Fore.CYAN)
    
    print(Fore.YELLOW + "\n  Danh sách nhân sự Sale đang hoạt động:")
    for idx, sale in enumerate(sale_team, 1):
        print(f"  [{idx}] {sale}")
    print(f"  [0] Chuyên viên tư vấn chung")
    
    try:
        sale_choice = input(Fore.WHITE + "\n  Chọn tài khoản của bạn (số): ").strip()
        if sale_choice == "0" or not sale_choice:
            selected_sale = "Chuyên viên tư vấn"
        else:
            sale_idx = int(sale_choice) - 1
            if 0 <= sale_idx < len(sale_team):
                selected_sale = sale_team[sale_idx]
            else:
                selected_sale = "Chuyên viên tư vấn"
    except Exception:
        selected_sale = "Chuyên viên tư vấn"
        
    print(Fore.GREEN + f"\n  -> Chào {selected_sale}! Bắt đầu tải bộ kịch bản...")
    
    while True:
        topics = get_topics()
        if not topics:
            print(Fore.RED + "  Lỗi: Không thể tải danh sách chủ đề kịch bản từ templates.yaml!")
            break
            
        clear_screen()
        print_separator("═", Fore.CYAN)
        print(Fore.CYAN + Style.BRIGHT + f"   TÀI KHOẢN TƯ VẤN: {selected_sale.upper()}")
        print_separator("═", Fore.CYAN)
        
        print(Fore.YELLOW + "\n  Chọn nhóm kịch bản tư vấn:")
        for idx, topic in enumerate(topics, 1):
            print(f"  [{Fore.GREEN}{idx}{Fore.YELLOW}] {topic}")
        print(f"  [{Fore.WHITE}0{Fore.YELLOW}] Quay lại / Thoát\n")
        
        choice = input(Fore.WHITE + "  Chọn nhóm (số): ").strip()
        if choice == "0" or not choice:
            print(Fore.CYAN + "\nChúc sale thành công chốt cọc nhanh chóng! 💪")
            break
            
        try:
            topic_idx = int(choice) - 1
            if 0 <= topic_idx < len(topics):
                selected_topic = topics[topic_idx]
                display_templates_of_topic(selected_topic, selected_sale)
            else:
                print(Fore.RED + "  Lựa chọn không hợp lệ!")
                input("\n  Nhấn Enter để chọn lại...")
        except ValueError:
            print(Fore.RED + "  Vui lòng nhập một số hợp lệ!")
            input("\n  Nhấn Enter để chọn lại...")

def display_templates_of_topic(topic_name, sale_name):
    while True:
        templates = get_templates_by_topic(topic_name)
        if not templates:
            print(Fore.RED + f"  Không tìm thấy mẫu tin nào trong nhóm {topic_name}")
            break
            
        clear_screen()
        print_separator("═", Fore.YELLOW)
        print(Fore.YELLOW + Style.BRIGHT + f"   CHỦ ĐỀ: {topic_name.upper()}")
        print_separator("═", Fore.YELLOW)
        
        print(Fore.CYAN + "\n  Chọn mẫu tin cụ thể:")
        for idx, item in enumerate(templates, 1):
            print(f"  [{Fore.GREEN}{idx}{Fore.CYAN}] {item.get('name')}")
        print(f"  [{Fore.WHITE}0{Fore.CYAN}] Quay lại nhóm trước\n")
        
        choice = input(Fore.WHITE + "  Chọn mẫu (số): ").strip()
        if choice == "0" or not choice:
            break
            
        try:
            item_idx = int(choice) - 1
            if 0 <= item_idx < len(templates):
                item = templates[item_idx]
                raw_content = item.get("content", "")
                rendered_content = render_template_content(raw_content, sale_name)
                
                clear_screen()
                print_separator("★", Fore.GREEN)
                print(Fore.GREEN + Style.BRIGHT + f"   MẪU: {item.get('name').upper()}")
                print_separator("★", Fore.GREEN)
                print()
                print(Fore.WHITE + rendered_content)
                print_separator("★", Fore.GREEN)
                print(Fore.CYAN + f"\n  💡 Mẹo: Bôi đen chuột phải để copy nội dung kịch bản trên!")
                input("\n  Nhấn Enter để quay lại danh sách mẫu...")
            else:
                print(Fore.RED + "  Lựa chọn không hợp lệ!")
                input("\n  Nhấn Enter để chọn lại...")
        except ValueError:
            print(Fore.RED + "  Vui lòng nhập một số hợp lệ!")
            input("\n  Nhấn Enter để chọn lại...")

def main():
    # Nhận tham số dòng lệnh nếu chạy dạng: python -m consultation "Tên Topic"
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        topics = get_topics()
        matched_topic = None
        
        # Thử tìm kiếm theo tên hoặc chỉ số
        if arg.isdigit():
            idx = int(arg) - 1
            if 0 <= idx < len(topics):
                matched_topic = topics[idx]
        else:
            for t in topics:
                if arg.lower() in t.lower():
                    matched_topic = t
                    break
        
        if matched_topic:
            # Chạy trực tiếp hiển thị topic đó
            display_templates_of_topic(matched_topic, "Chuyên viên tư vấn")
        else:
            print(f"Không tìm thấy chủ đề nào trùng khớp với '{arg}'")
            print("Các chủ đề có sẵn:")
            for idx, t in enumerate(topics, 1):
                print(f"  [{idx}] {t}")
    else:
        display_interactive_cli()

if __name__ == "__main__":
    main()
