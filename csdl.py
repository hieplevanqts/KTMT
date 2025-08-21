# Author: Hiep Le Van
# Website: https://vanhiep.net

import json
import base64
import requests

# ---- CONFIG ----
INPUT_FILE = "json/Co_So_Du_Lieu_IT06_063.json"
OUTPUT_FILE = "json/Co_So_Du_Lieu_IT06_063_base64_02.json"

# Nếu server yêu cầu đăng nhập -> bạn phải copy cookie từ trình duyệt bỏ vào đây
HEADERS = {
    "Cookie": "_ga_YQRMY1CBJ9=GS1.1.1732639140.1.1.1732639182.0.0.0; _ga_ED48KBZ29Z=GS1.1.1732638835.2.1.1732639712.0.0.0; _ga=GA1.3.1156918811.1731685105; _ga_4SJJ09QM1E=GS1.3.1740194617.2.0.1740194617.0.0.0; __session:0.6108774371853148:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1145137; __session:0.29074814658116466:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1112681; __session:0.5365010317441669:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1180922; _gid=GA1.3.1984800252.1755761020; MoodleSession=9n5pf9roo7c39amukj9t0frfq6; __session:0.7045724075994289:myVar=https://learning.ehou.edu.vn/mod/forum/view.php?id=1145535; __session:0.8031620374167373:=https:; _gat=1; _ga_TQWDDMY9FW=GS2.3.s1755761021$o114$g1$t1755762868$j60$l0$h0"
}


def url_to_base64(url):
    try:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        b64 = base64.b64encode(resp.content).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"Lỗi tải {url}: {e}")
        return url  # nếu lỗi thì giữ nguyên link

def process_json(data):
    for q in data:
        # question_images
        if "question_images" in q and q["question_images"]:
            q["question_images"] = [url_to_base64(img) for img in q["question_images"]]

        # option images
        if "options" in q:
            for opt in q["options"].values():
                if "images" in opt and opt["images"]:
                    opt["images"] = [url_to_base64(img) for img in opt["images"]]
    return data

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = process_json(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu file {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
