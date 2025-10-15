# Median Filter Implementation

## Tổng quan
Đây là implementation thủ công của Median Filter sử dụng NumPy, được tích hợp vào Flask API để xử lý ảnh.

## Tính năng

### 1. Median Filter Thủ công (`median_filter`)
- Implementation cơ bản sử dụng vòng lặp
- Dễ hiểu và debug
- Phù hợp cho ảnh nhỏ hoặc học tập

### 2. Median Filter Tối ưu (`median_filter_optimized`)
- Sử dụng `sliding_window_view` của NumPy
- Nhanh hơn implementation thủ công
- Vectorized operations

## API Endpoints

### GET `/`
Trả về danh sách các thuật toán hỗ trợ, bao gồm:
- `median`: Lọc trung vị (Median Filter)
- `median_opt`: Lọc trung vị tối ưu (Optimized)

### POST `/process`
Xử lý ảnh với các tham số:

**Form Data:**
- `image`: File ảnh (required)
- `algorithm`: Thuật toán xử lý (default: 'canny')
- `kernel_size`: Kích thước kernel cho median filter (default: 3)

**Response:**
```json
{
    "processed_image": "base64_encoded_image",
    "algorithm_used": "median",
    "kernel_size": 3
}
```

## Cách sử dụng

### 1. Chạy server
```bash
cd backend
python app.py
```

### 2. Test với curl
```bash
curl -X POST -F "image=@test_image.jpg" -F "algorithm=median" -F "kernel_size=3" http://localhost:5000/process
```

### 3. Test với Python
```python
import requests

with open('test_image.jpg', 'rb') as f:
    files = {'image': f}
    data = {'algorithm': 'median', 'kernel_size': 5}
    response = requests.post('http://localhost:5000/process', files=files, data=data)
    result = response.json()
    print(f"Algorithm used: {result['algorithm_used']}")
    print(f"Kernel size: {result['kernel_size']}")
```

## Chạy test
```bash
cd backend
python test_median_filter.py
```

## Tham số Kernel Size

- **3x3**: Nhẹ, giữ được chi tiết
- **5x5**: Trung bình, cân bằng giữa noise reduction và chi tiết
- **7x7**: Mạnh, loại bỏ nhiều noise nhưng có thể làm mờ chi tiết

## Lưu ý

1. **Kernel size phải là số lẻ** (3, 5, 7, 9, ...)
2. **Ảnh đầu vào sẽ được chuyển thành grayscale**
3. **Padding mode**: Sử dụng 'edge' để giữ nguyên giá trị biên
4. **Performance**: Optimized version nhanh hơn manual version đáng kể

## So sánh với OpenCV

Implementation này được thiết kế để:
- Học tập và hiểu thuật toán
- Tùy chỉnh logic xử lý
- Tích hợp vào hệ thống hiện có

OpenCV's `cv2.medianBlur()` vẫn nhanh hơn và được tối ưu hóa tốt hơn cho production.
