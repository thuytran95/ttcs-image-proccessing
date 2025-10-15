# Manual Canny Edge Detection Implementation

## Tổng quan
Đây là implementation thủ công của thuật toán Canny Edge Detection, một trong những thuật toán phát hiện biên phổ biến và hiệu quả nhất.

## Thuật toán Canny - 5 bước chính

### 1. **Gaussian Blur** (Làm mờ Gaussian)
```python
def gaussian_kernel(size, sigma):
    # Tạo kernel Gaussian để làm mờ ảnh
    # Giúp giảm noise trước khi phát hiện biên
```

**Mục đích:**
- Giảm noise trong ảnh
- Làm mịn ảnh trước khi tính gradient
- Kernel size thường là 5x5, sigma = 1.0

### 2. **Sobel Filters** (Tính gradient)
```python
def sobel_filters(image):
    # Sobel X: phát hiện biên dọc
    sobel_x = [[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]]
    
    # Sobel Y: phát hiện biên ngang  
    sobel_y = [[-1, -2, -1],
               [0, 0, 0],
               [1, 2, 1]]
```

**Mục đích:**
- Tính gradient theo 2 hướng X và Y
- Magnitude = √(Gx² + Gy²)
- Direction = arctan(Gy/Gx)

### 3. **Non-Maximum Suppression** (Loại bỏ cực đại không tối đa)
```python
def non_maximum_suppression(magnitude, direction):
    # Chỉ giữ lại pixel nếu nó là local maximum
    # theo hướng gradient
```

**Mục đích:**
- Làm mỏng biên (edge thinning)
- Chỉ giữ lại pixel có gradient mạnh nhất theo hướng của nó
- Loại bỏ các pixel không phải là cực đại local

### 4. **Double Thresholding** (Ngưỡng kép)
```python
def double_threshold(image, low_threshold, high_threshold):
    strong_edges = image >= high_threshold
    weak_edges = (image >= low_threshold) & (image < high_threshold)
```

**Mục đích:**
- **Strong edges**: Biên chắc chắn (≥ high_threshold)
- **Weak edges**: Biên yếu (low_threshold ≤ x < high_threshold)
- Loại bỏ noise (x < low_threshold)

### 5. **Edge Tracking by Hysteresis** (Theo dõi biên)
```python
def edge_tracking(strong_edges, weak_edges):
    # Chỉ giữ lại weak edges nếu chúng kết nối với strong edges
    # Sử dụng 8-connectivity
```

**Mục đích:**
- Kết nối các biên bị đứt đoạn
- Chỉ giữ lại weak edges nếu chúng liên kết với strong edges
- Loại bỏ noise và biên giả

## Tham số quan trọng

### **Thresholds:**
- **Low threshold**: 30-50 (phát hiện biên yếu)
- **High threshold**: 100-200 (phát hiện biên mạnh)
- **Tỷ lệ**: high_threshold ≈ 2-3 × low_threshold

### **Sigma (Gaussian blur):**
- **Sigma = 1.0**: Làm mờ nhẹ, giữ chi tiết
- **Sigma = 1.5**: Làm mờ vừa, cân bằng
- **Sigma = 2.0**: Làm mờ mạnh, giảm noise nhiều

## So sánh với OpenCV

| Aspect | Manual Implementation | OpenCV |
|--------|----------------------|--------|
| **Speed** | Chậm hơn (Python loops) | Nhanh (C++ optimized) |
| **Accuracy** | Tương đương | Tương đương |
| **Customization** | Dễ tùy chỉnh | Khó tùy chỉnh |
| **Learning** | Tốt cho học tập | Tốt cho production |

## Cách sử dụng API

### **Endpoint:**
```
POST /process
```

### **Parameters:**
```json
{
  "algorithm": "canny",
  "low_threshold": 50,
  "high_threshold": 150,
  "sigma": 1.0
}
```

### **Response:**
```json
{
  "processed_image": "base64_encoded_image",
  "algorithm_used": "canny",
  "low_threshold": 50,
  "high_threshold": 150,
  "sigma": 1.0
}
```

## Test và Debug

### **Chạy test:**
```bash
cd backend
python test_canny.py
```

### **Test với API:**
```bash
curl -X POST -F "image=@test.jpg" \
     -F "algorithm=canny" \
     -F "low_threshold=50" \
     -F "high_threshold=150" \
     -F "sigma=1.0" \
     http://localhost:5000/process
```

## Ưu điểm của Implementation thủ công

1. **Hiểu rõ thuật toán**: Từng bước được implement rõ ràng
2. **Tùy chỉnh dễ dàng**: Có thể modify từng bước
3. **Debug tốt**: Có thể xem kết quả từng bước
4. **Học tập**: Tốt cho việc nghiên cứu và học tập

## Lưu ý Performance

- **Chậm hơn OpenCV** do sử dụng Python loops
- **Memory usage** cao hơn do tạo nhiều arrays trung gian
- **Phù hợp** cho ảnh nhỏ và học tập
- **Production** nên dùng OpenCV version
