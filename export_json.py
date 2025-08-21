# Author: Hiep Le Van
# Website: https://vanhiep.net

from bs4 import BeautifulSoup
import json

# Load file HTML
file_path = "txt/csdl.htm"   # đổi thành đường dẫn file của bạn
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

questions = []
index = 1

for q in soup.find_all("div", class_="que"):
    # Câu hỏi
    q_text = q.find("div", class_="qtext").get_text(" ", strip=True) if q.find("div", class_="qtext") else ""

    # Hình ảnh trong câu hỏi
    q_images = [img["src"] for img in q.find("div", class_="qtext").find_all("img")] if q.find("div", class_="qtext") else []

    # Lấy danh sách đáp án
    options = {}
    option_index = 1
    correct_answer = None

    for ans_block in q.find_all("div", class_="answer"):
        for ans in ans_block.find_all("div", recursive=False):
            label = ans.find("label")
            text = label.get_text(" ", strip=True) if label else ""
            images = [img["src"] for img in ans.find_all("img")]

            # Kiểm tra đáp án đúng
            if "correct" in ans.get("class", []):
                correct_answer = option_index

            options[str(option_index)] = {
                "text": text,
                "images": images
            }
            option_index += 1

    # Thêm vào danh sách câu hỏi
    questions.append({
        "index": index,
        "question": q_text,
        "question_images": q_images,
        "options": options,
        "correctAnswer": correct_answer
    })
    index += 1

# Xuất ra file JSON
output_path = "json/Co_So_Du_Lieu_IT06_063.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ Đã lưu dữ liệu thành {output_path}")
