# [Private Release]: Công cụ hỗ trợ tăng tốc biên dịch Bài tập lớn DSA HK241

## 1. Nguyên lý hoạt động
Khi khởi tạo, hệ thống sẽ build tất cả file của các thành phần trước. Sau khi khởi tạo xong, hệ thống sẽ ghi nhận mỗi lần bạn save file, hệ thống sec hỉ build lại các file cần thiết để chạy

## 2. Cách sử dụng
### 2.1 Yêu cầu hệ thống
Linux (tested on Ubuntu)  
Python 3  
pip (for install watchdog)  

### 2.2 Sử dụng lần đầu
* Cài đặt thư viện watchdog thông qua lệnh: pip install watchdog
* Tiến hành chạy file helper.py
* Nhập "r" để build lại toàn bộ source code cho lần đầu
* Khi save file. Output sẽ được lưu vào file outtest.txt nếu hoạt động được

### 2.3 Cho những lần sau đó
* Bạn chỉ cần chạy file helper.py

## 3. Các vấn đề còn gặp phải
* Thao tác kill task chưa thật sự hoàn thiện, có thể xảy ra lỗi
* Đôi khi bị bouching trong việc nhận file lưu
* Việc save file khi đang build có thể xáy ra lỗi ở lần chạy lại 
=> có thể fix bằng cách khởi động lại helper.py

Link download: https://github.com/namanhishere/dsahelperk241

