"""
Tạo Windows Scheduled Task cho nhac_sang.py — chạy 1 lần với quyền Admin.
Chạy: python setup_task_scheduler.py
Sau khi chạy, kiểm tra trong Task Scheduler (taskschd.msc): KhaSon_NhacNhoSang
"""
import subprocess
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BAT_PATH = os.path.join(SCRIPT_DIR, "Nhac Sang.bat")
TASK_NAME = "KhaSon_NhacNhoSang"


def check_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def create_task():
    cmd = [
        "schtasks", "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{BAT_PATH}"',
        "/sc", "WEEKLY",
        "/d", "MON,TUE,WED,THU,FRI,SAT",
        "/st", "08:00",
        "/f",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.returncode == 0, result.stdout, result.stderr


def query_task():
    result = subprocess.run(
        ["schtasks", "/query", "/tn", TASK_NAME, "/fo", "LIST"],
        capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode == 0


def main():
    print("=" * 56)
    print("  THIET LAP TASK SCHEDULER — KHA SON GREEN HOME")
    print("=" * 56)

    if not os.path.exists(BAT_PATH):
        print(f"\n[LOI] Khong tim thay file bat: {BAT_PATH}")
        print("  Kiem tra lai thu muc truoc khi chay script nay.")
        input("\nNhan Enter de dong...")
        sys.exit(1)

    print(f"\n  File bat   : {BAT_PATH}")
    print(f"  Task name  : {TASK_NAME}")
    print(f"  Lich chay  : Thu 2 - Thu 7, luc 08:00 sang")

    if not check_admin():
        print("\n[CANH BAO] Script nay can chay voi quyen Admin.")
        print("  Chuot phai file nay -> 'Run as administrator'")
        print("  Hoac chay: python setup_task_scheduler.py trong terminal Admin")
        print("\n  Tiep tuc thu (co the that bai neu khong co quyen)...")

    print("\n  Dang tao scheduled task...")
    ok, out, err = create_task()

    if ok:
        print("\n  [OK] Tao task thanh cong!")
        print(f"  Task '{TASK_NAME}' se chay luc 08:00 moi ngay T2-T7.")
        print("\n  Kiem tra lai: Mo Task Scheduler (taskschd.msc)")
        print("  -> Task Scheduler Library -> KhaSon_NhacNhoSang")
    else:
        print(f"\n  [LOI] Khong tao duoc task.")
        if err:
            print(f"  Chi tiet: {err.strip()}")
        print("\n  Cach tao thu cong:")
        print("  1. Mo Task Scheduler (Windows + R -> taskschd.msc)")
        print("  2. Action -> Create Basic Task")
        print(f"  3. Name: {TASK_NAME}")
        print("  4. Trigger: Weekly, Thu 2-7, 08:00")
        print(f"  5. Action: Start a program -> {BAT_PATH}")

    input("\nNhan Enter de dong...")


if __name__ == "__main__":
    main()
