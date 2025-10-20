# TTCS Image Processing

Ứng dụng xử lý ảnh với các thuật toán phát hiện biên và lọc nhiễu, được xây dựng với kiến trúc Full-stack.

## 📋 Tổng quan

Project này là một ứng dụng web cho phép người dùng upload ảnh và áp dụng các thuật toán xử lý ảnh như:
- **Canny Edge Detection**: Phát hiện biên ảnh với thuật toán Canny tự implement
- **Median Filter**: Lọc nhiễu bằng thuật toán lọc trung vị

## 🏗️ Kiến trúc hệ thống

### Backend (Python Flask)
```
backend/
├── app.py                 # Flask application chính
├── controllers/          # Layer xử lý HTTP requests
│   └── image_controller.py
├── entities/             # Domain models và business logic
│   ├── image.py         # Image entity
│   └── filters.py       # Filter implementations (Canny, Median)
├── services/            # Business logic layer
│   ├── image_processor.py
│   └── filter_factory.py # Factory pattern cho filters
├── utils/               # Utilities và constants
│   ├── constants.py
│   └── validators.py
└── requirements.txt     # Python dependencies
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── App.tsx          # Main React component
│   ├── api/             # API client
│   │   └── image.ts
│   ├── hooks/           # Custom React hooks
│   │   └── useImageProccess.ts
│   ├── types/           # TypeScript type definitions
│   └── utils/           # Frontend utilities
├── package.json         # Node.js dependencies
└── vite.config.js       # Vite build configuration
```

## 🚀 Công nghệ sử dụng

### Backend
- **Flask**: Web framework
- **OpenCV**: Xử lý ảnh
- **NumPy**: Tính toán số học
- **SciPy**: Thuật toán khoa học
- **Matplotlib**: Visualization

### Frontend
- **React 19**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Axios**: HTTP client

## 🔧 Cài đặt và chạy

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Server sẽ chạy tại `http://localhost:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Ứng dụng sẽ chạy tại `http://localhost:5173`

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Lấy danh sách thuật toán hỗ trợ |
| POST | `/process` | Xử lý ảnh với thuật toán được chọn |
| GET | `/algorithms/<name>` | Lấy thông tin chi tiết thuật toán |
| GET | `/health` | Health check |

### Ví dụ sử dụng API

**Upload và xử lý ảnh:**
```bash
curl -X POST http://localhost:5000/process \
  -F "image=@path/to/image.jpg" \
  -F "algorithm=canny" \
  -F "kernel_size=5"
```

## 🧮 Thuật toán được hỗ trợ

### 1. Canny Edge Detection
- **Mô tả**: Phát hiện biên ảnh với thuật toán Canny tự implement
- **Tham số**:
  - `sigma`: Độ mờ Gaussian (default: 1.0)
  - `low_threshold`: Ngưỡng thấp (default: 50)
  - `high_threshold`: Ngưỡng cao (default: 150)
  - `kernel_size`: Kích thước kernel (default: 5)

### 2. Median Filter
- **Mô tả**: Lọc nhiễu bằng cách thay thế pixel bằng giá trị trung vị
- **Tham số**:
  - `kernel_size`: Kích thước kernel (3, 5, 7, 9)

## 🎯 Tính năng chính

- ✅ Upload ảnh từ máy tính
- ✅ Chọn thuật toán xử lý
- ✅ Tùy chỉnh tham số kernel size
- ✅ Xem trước ảnh gốc và ảnh đã xử lý
- ✅ Download ảnh kết quả
- ✅ Giao diện responsive và thân thiện
- ✅ Xử lý lỗi và validation

## 🔍 Kiến trúc Design Patterns

- **Factory Pattern**: `FilterFactory` để tạo các filter instances
- **Strategy Pattern**: `BaseFilter` abstract class cho các thuật toán
- **MVC Pattern**: Tách biệt Controller, Service và Entity layers
- **Repository Pattern**: `ImageProcessor` để xử lý logic nghiệp vụ

## 📝 Ghi chú phát triển

- Backend sử dụng kiến trúc layered với separation of concerns
- Frontend sử dụng React hooks để quản lý state
- API responses được chuẩn hóa với format JSON
- Error handling được implement đầy đủ ở cả backend và frontend
- Code được viết bằng tiếng Việt cho comments và messages

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.