# CRAWL TOOLS

**CRAWL TOOLS** là một công cụ thu thập thông tin từ Internet dựa trên từ khóa và tên quốc gia do người dùng nhập. Dữ liệu thu được sẽ được lưu ở định dạng `.jsonl` để dễ dàng xử lý và phân tích sau này.

---

## Yêu cầu hệ thống

- Đã cài đặt Docker

---

## Hướng dẫn cài đặt

### 1. Tạo image và chạy container Docker

Trên hệ điều hành window, mở Docker Desktop, mở `cmd` và nhập lệnh sau để kiểm tra docker đã cài đặt và chạy thành công hay chưa
```bash
docker --version
```
Di chuyển vào thư mục chứa file Dockerfile và nhập lệnh sau để tạo docker image
```bash
docker build . --tag selenium_crawl:extend
```
Nhập lệnh sau để kiểm tra xem image đã cài đặt thành công hay chưa
```bash
docker image ls
```
Trong cùng thư mục, tiếp tục nhập lệnh sau để chạy container
```bash
docker-compose up
```

## Hướng dẫn sử dụng
### 1. Mở CMD hoặc Terminal
### 2. chạy lệnh
```bash
docker exec -it crawl-selenium-1 --country "Tên quốc gia" --keyword "Keyword muốn tìm kiếm"
```
### 3. Kết quả lưu tại file 
```bash
crawl_result.jsonl
```
### Cấu trúc thư mục
```bash
├── crawl_auto.py
├── requirements.txt
├── docker-compose.yaml
├── Dockerfile
├── crawl_result.jsonl       # File kết quả sau khi crawl
└── README.md
```
