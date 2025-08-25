from flask import Flask, jsonify, send_from_directory, request
import os
import json
import requests
import base64
from bs4 import BeautifulSoup
# Thêm import cho Flask-CORS
from flask_cors import CORS

app = Flask(__name__)
# Áp dụng CORS cho toàn bộ ứng dụng
CORS(app)

# Phục vụ các file tĩnh (bao gồm tool.html)
@app.route('/')
def serve_tool_html():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'tool.html')
@app.route('/home')
def serve_tool_html():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')
# API endpoint để lấy danh sách các file JSON từ file_list.json
@app.route('/api/files')
def get_json_files():
    list_file_path = os.path.join(os.path.dirname(__file__), 'file_list.json')
    if os.path.exists(list_file_path):
        with open(list_file_path, 'r', encoding='utf-8') as f:
            try:
                files = json.load(f)
                return jsonify(files)
            except json.JSONDecodeError:
                return jsonify([]), 500
    return jsonify([]), 404

# API endpoint để thêm môn học và cập nhật file_list.json
@app.route('/api/add-subject', methods=['POST'])
def add_subject():
    data = request.json
    subject_name = data.get('subjectName')
    
    if not subject_name:
        return jsonify({"success": False, "message": "Tên môn không được để trống."}), 400
    
    file_name = f"{subject_name}.json"
    json_dir = os.path.join(os.path.dirname(__file__), 'json')
    file_path = os.path.join(json_dir, file_name)

    if os.path.exists(file_path):
        return jsonify({"success": False, "message": "Môn học đã tồn tại."}), 409

    try:
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        
        list_file_path = os.path.join(os.path.dirname(__file__), 'file_list.json')
        
        existing_list = []
        if os.path.exists(list_file_path):
            with open(list_file_path, 'r', encoding='utf-8') as f:
                try:
                    existing_list = json.load(f)
                except json.JSONDecodeError:
                    existing_list = []
        
        existing_list.append(file_name)
        
        with open(list_file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_list, f, ensure_ascii=False, indent=4)
            
        return jsonify({"success": True, "message": "Thêm môn học thành công!", "fileName": file_name})
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi server: {str(e)}"}), 500

# Hàm chuyển đổi URL ảnh thành chuỗi Base64
def url_to_base64(url):
    try:
        HEADERS = {
            "Cookie": "_ga_YQRMY1CBJ9=GS1.1.1732639140.1.1.1732639182.0.0.0; _ga_ED48KBZ29Z=GS1.1.1732638835.2.1.1732639712.0.0.0; _ga=GA1.3.1156918811.1731685105; _ga_4SJJ09QM1E=GS1.3.1740194617.2.0.1740194617.0.0.0; __session:0.6108774371853148:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1145137; __session:0.29074814658116466:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1112681; __session:0.5365010317441669:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1180922; _gid=GA1.3.1984800252.1755761020; MoodleSession=9n5pf9roo7c39amukj9t0frfq6; __session:0.7045724075994289:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1145535; __session:0.8031620374167373:=https:; _gat=1; _ga_TQWDDMY9FW=GS2.3.s1755761021$o114$g1$t1755762868$j60$l0$h0"
        }
        
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        content_type = resp.headers['content-type']
        b64 = base64.b64encode(resp.content).decode("utf-8")
        return f"data:{content_type};base64,{b64}"
    except Exception as e:
        print(f"Lỗi tải {url}: {e}")
        return url

def remove_duplicates(questions):
    unique_questions = {}
    for q in questions:
        question_text = q.get("question")
        if question_text:
            if question_text not in unique_questions:
                unique_questions[question_text] = q
            else:
                existing_q = unique_questions[question_text]
                # Ưu tiên giữ lại câu hỏi có đáp án đúng
                if q.get("correctAnswer") is not None and existing_q.get("correctAnswer") is None:
                    unique_questions[question_text] = q
    
    # Chuyển dictionary thành list và cập nhật index
    final_list = list(unique_questions.values())
    for i, q in enumerate(final_list):
        q["index"] = i + 1
    
    return final_list

# API endpoint để xử lý HTML và xuất JSON
@app.route('/api/export-json', methods=['POST'])
def export_json():
    try:
        data = request.json
        html_content = data.get('htmlCode', '')
        selected_file = data.get('selectedFile', '')
        
        if not html_content:
            return jsonify({"success": False, "message": "Nội dung HTML không được để trống."}), 400

        soup = BeautifulSoup(html_content, "html.parser")
        
        newly_parsed_questions = []
        index = 1
        for q in soup.find_all("div", class_="que"):
            q_text = q.find("div", class_="qtext").get_text(" ", strip=True) if q.find("div", class_="qtext") else ""
            q_images = [url_to_base64(img["src"]) for img in q.find("div", class_="qtext").find_all("img")] if q.find("div", class_="qtext") else []
            
            options = {}
            option_index = 1
            correct_answer = None
            for ans_block in q.find_all("div", class_="answer"):
                for ans in ans_block.find_all("div", recursive=False):
                    label = ans.find("label")
                    text = label.get_text(" ", strip=True) if label else ""
                    images = [url_to_base64(img["src"]) for img in ans.find_all("img")]
                    
                    if "correct" in ans.get("class", []):
                        correct_answer = option_index
                    
                    options[str(option_index)] = {
                        "text": text,
                        "images": images
                    }
                    option_index += 1
            
            newly_parsed_questions.append({
                "index": index,
                "question": q_text,
                "question_images": q_images,
                "options": options,
                "correctAnswer": correct_answer
            })
            index += 1

        output_file_name = selected_file if selected_file else "exported_data.json"
        
        output_dir = os.path.join(os.path.dirname(__file__), 'json')
        output_path = os.path.join(output_dir, output_file_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        all_questions = []
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        all_questions.extend(existing_data)
                except json.JSONDecodeError:
                    pass
        
        all_questions.extend(newly_parsed_questions)
        
        # Gọi hàm loại bỏ trùng lặp
        unique_questions = remove_duplicates(all_questions)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(unique_questions, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": f"Dữ liệu đã được gộp, loại bỏ trùng lặp và lưu thành công vào {output_path}."})

    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi xử lý: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)