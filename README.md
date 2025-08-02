# 🕸️ CRAWL TOOLS

**CRAWL TOOLS** là một công cụ thu thập thông tin từ Internet dựa trên từ khóa và tên quốc gia do người dùng nhập. Dữ liệu thu được sẽ được lưu ở định dạng `.jsonl` để dễ dàng xử lý và phân tích sau này.

---

## Yêu cầu hệ thống

- Python 3.7+
- Kết nối Internet
- Đã cài đặt Google Chrome
- pip (Python package installer)

---

## Hướng dẫn cài đặt

### 1. Cài Python

Truy cập trang chủ Python và tải phiên bản mới nhất:

https://www.python.org/

### 2. Cài đặt các package cần thiết

Mở Terminal hoặc CMD trong thư mục chứa file `requirements.txt`, sau đó chạy lệnh:

```bash
pip install -r requirements.txt
```

## Hướng dẫn sử dụng
### 1. Mở CMD hoặc Terminal tại thư mục chứa ```crawl_auto.py```
### 2. chạy lệnh
```bash
python crawl_auto.py
```
### 3. Nhập thông tin về 
tên quốc gia  (Ví dụ: Vietnam)
từ khóa (Ví dụ: English )
### 4. Kết quả lưu tại file 
```bash
crawl_result.jsonl
```
### Cấu trúc thư mục
```bash
├── crawl_auto.py
├── requirements.txt
├── crawl_result.jsonl       # File kết quả sau khi crawl
└── README.md
```