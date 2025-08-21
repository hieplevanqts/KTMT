import json

def filter_questions_with_priority(input_file_path, output_file_path):
    """
    Lọc các đối tượng có trường 'question' trùng lặp, ưu tiên giữ lại
    phiên bản có câu trả lời đúng.

    Args:
        input_file_path (str): Đường dẫn đến tệp JSON đầu vào.
        output_file_path (str): Đường dẫn đến tệp JSON đầu ra đã được lọc.
    """
    try:
        # Đọc nội dung của tệp JSON đầu vào
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Sử dụng một dictionary để lưu trữ các câu hỏi duy nhất
        # Key là nội dung câu hỏi (question), value là đối tượng câu hỏi
        unique_questions = {}

        # Lặp qua từng đối tượng trong danh sách
        for item in data:
            question_text = item.get("question")
            if not question_text:
                continue

            # Kiểm tra xem câu hỏi đã tồn tại trong dictionary chưa
            if question_text not in unique_questions:
                # Nếu chưa tồn tại, thêm vào
                unique_questions[question_text] = item
            else:
                # Nếu đã tồn tại, kiểm tra xem bản sao hiện tại có correctAnswer không
                current_correct_answer = item.get("correctAnswer")
                existing_correct_answer = unique_questions[question_text].get("correctAnswer")
                
                # Ưu tiên giữ lại bản sao có đáp án đúng
                if current_correct_answer is not None and existing_correct_answer is None:
                    unique_questions[question_text] = item
        
        # Chuyển dictionary các đối tượng duy nhất thành danh sách
        unique_data = list(unique_questions.values())

        # Ghi danh sách đã lọc vào tệp JSON đầu ra
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(unique_data, outfile, ensure_ascii=False, indent=4)
        
        print(f"Đã lọc thành công các câu hỏi trùng lặp và lưu vào file '{output_file_path}'")
        print(f"Tổng số mục ban đầu: {len(data)}")
        print(f"Tổng số mục sau khi lọc: {len(unique_data)}")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{input_file_path}'.")
    except json.JSONDecodeError:
        print("Lỗi: Không thể giải mã nội dung JSON. Vui lòng kiểm tra lại định dạng file.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Các đường dẫn file
input_file = 'json/Co_So_Du_Lieu_IT06_063_merged.json'
output_file = 'json/Co_So_Du_Lieu_IT06_063_unique.json'

# Gọi hàm để thực thi
filter_questions_with_priority(input_file, output_file)