# Sử dụng một image Python nhẹ làm cơ sở
FROM python:3.9-slim

# Đặt biến môi trường để Python không tạo tệp .pyc và hiển thị đầu ra ngay lập tức
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tạo và chuyển tới thư mục làm việc
WORKDIR /app

# Sao chép tệp yêu cầu và cài đặt các thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép tất cả các tệp từ thư mục hiện tại vào thư mục /app trong container
COPY . .

# Mở port 5000 để nhận yêu cầu từ bên ngoài
EXPOSE 5001

# Lệnh mặc định để khởi chạy ứng dụng bằng Gunicorn, chỉ rõ file server.py và biến app
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "server:app"]