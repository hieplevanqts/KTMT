import subprocess
import sys

def run_commands(commands):
    """
    Chạy một danh sách các lệnh liên tiếp.
    """
    for command in commands:
        try:
            print(f"Bắt đầu chạy lệnh: {command}")
            # subprocess.run() sẽ chạy lệnh và đợi cho đến khi nó hoàn thành.
            # check=True sẽ ném một ngoại lệ nếu lệnh trả về mã lỗi khác 0.
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print("Lệnh hoàn thành thành công.")
            print("--- Kết quả đầu ra ---")
            print(result.stdout)
            print("-----------------------")
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi chạy lệnh: {command}")
            print(f"Mã lỗi: {e.returncode}")
            print(f"Đầu ra lỗi: {e.stderr}")
            # Thoát script nếu có lỗi xảy ra
            sys.exit(1)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp hoặc lệnh '{command.split()[0]}'.")
            sys.exit(1)

# Danh sách các lệnh cần chạy theo thứ tự
# Sử dụng 'python' thay cho 'python3' nếu hệ thống của bạn chỉ có 'python'
list_of_commands = [
    "python3 export_json.py",
    "python3 csdl.py",
    "python3 merge_json.py",
    # "python3 filter_duplicates.py"
]

# Gọi hàm để chạy các lệnh
run_commands(list_of_commands)
print("Tất cả các lệnh đã được chạy xong.")