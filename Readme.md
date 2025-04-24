
# 🤖 Chatbot AI - Tóm tắt URL, Trích xuất PDF, Tìm sự kiện mới

Ứng dụng Chatbot AI hỗ trợ:
- Tóm tắt bài báo từ URL.
- Đọc và hỏi đáp theo file PDF.
- Tìm kiếm và tóm tắt sự kiện mới nhất bằng DuckDuckGo.
- Chat tương tác qua mô hình LLM OpenRouter.

## 🧰 Yêu cầu hệ thống

- Python >= 3.8
- pip (Python package manager)
- Kết nối Internet
- Tài khoản [OpenRouter.ai](https://openrouter.ai)

---

## 🚀 Cài đặt

### 1. Clone source code(bỏ qua nếu tải file .zip)

```bash
git clone [https://github.com/yourusername/ai-chatbot-app.git](https://github.com/viettrung23/Chatbot.git)
cd ai-chatbot-app
```

### 2. Tạo môi trường ảo (tuỳ chọn nhưng nên dùng)

```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate     # Trên Windows
```

### 3. Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env` chứa API Key

Tạo file `.env` trong thư mục gốc với nội dung:

```bash
API_KEY=your_openrouter_api_key # Thay your_openrouter_api_key bằng API KEY của bạn
```

> 🔑 Bạn lấy API Key tại: https://openrouter.ai

---

## ▶️ Cách chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ hiển thị link Gradio ví dụ như:

```
Running on local URL: http://127.0.0.1:7860/
```

Mở link đó trên trình duyệt để bắt đầu trò chuyện!

---
