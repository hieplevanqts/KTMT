import json

def merge_json_files(file1_path, file2_path, output_file_path):
    """
    Gộp nội dung từ file JSON thứ hai vào cuối file JSON thứ nhất.

    Args:
        file1_path (str): Đường dẫn đến file JSON gốc.
        file2_path (str): Đường dẫn đến file JSON cần gộp.
        output_file_path (str): Đường dẫn đến file JSON đầu ra đã gộp.
    """
    try:
        # Mở và đọc nội dung của hai file JSON
        with open(file1_path, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
        
        with open(file2_path, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)

        # Gộp nội dung của data2 vào cuối data1
        # Sử dụng extend() để thêm tất cả các phần tử của data2 vào data1
        data1.extend(data2)

        # Lưu nội dung đã gộp vào file đầu ra mới
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data1, outfile, ensure_ascii=False, indent=4)
        
        print(f"Đã gộp thành công và lưu vào file '{output_file_path}'")

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy một hoặc cả hai file JSON.")
    except json.JSONDecodeError:
        print("Lỗi: Không thể giải mã nội dung JSON. Vui lòng kiểm tra lại định dạng file.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Các đường dẫn file
file_goc = 'json/Co_So_Du_Lieu_IT06_063_base64.json'
file_gop = 'json/Co_So_Du_Lieu_IT06_063_base64_02.json'
file_dau_ra = 'json/Co_So_Du_Lieu_IT06_063_merged.json'

# Gọi hàm để thực thi
merge_json_files(file_goc, file_gop, file_dau_ra)