from flask import Flask, request, jsonify
import cv2
import numpy as np
from flask_cors import CORS
import base64
from numpy.lib.stride_tricks import sliding_window_view
import math
from scipy import ndimage

app = Flask(__name__)
CORS(app)


def gaussian_kernel(size, sigma=1.0):
    """
    Tạo kernel Gaussian 2D tối ưu (Bước 1: Làm mượt ảnh).
    """
    if size % 2 == 0:
        raise ValueError("Kernel size phải là số lẻ!")

    # Tối ưu: sử dụng meshgrid thay vì nested loops
    center = size // 2
    x = np.arange(size) - center
    y = np.arange(size) - center
    X, Y = np.meshgrid(x, y)

    # Vectorized calculation
    kernel = np.exp(-(X ** 2 + Y ** 2) / (2 * sigma ** 2))
    return kernel / np.sum(kernel)


def convolve(image, kernel):
    """
    Convolution tối ưu sử dụng sliding window view.
    """
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')

    # Sử dụng sliding window view cho vectorized operations
    windows = sliding_window_view(padded, (kh, kw))
    result = np.sum(windows * kernel, axis=(2, 3))

    return result


def sobel_gradients(image):
    """
    Tính gradient Sobel tối ưu (Bước 2: Tính độ lớn và hướng gradient).
    """
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)

    # Sử dụng convolution tối ưu
    gx = convolve(image, sobel_x)
    gy = convolve(image, sobel_y)

    # Vectorized magnitude và angle calculation
    magnitude = np.sqrt(gx ** 2 + gy ** 2)
    angle = np.arctan2(gy, gx) * (180 / np.pi) % 180  # Góc 0-180 độ

    return magnitude, angle


def non_max_suppression(magnitude, angle):
    """
    Non-max suppression tối ưu (Bước 3: Giữ gradient max cục bộ theo hướng).
    """
    h, w = magnitude.shape
    result = np.zeros_like(magnitude)

    # Quantize angles to 4 directions: 0°, 45°, 90°, 135°
    angle_quantized = np.round(angle / 45) * 45
    angle_quantized = angle_quantized % 180

    # Create masks for each direction
    mask_0 = (angle_quantized == 0) | (angle_quantized == 180)
    mask_45 = (angle_quantized == 45)
    mask_90 = (angle_quantized == 90)
    mask_135 = (angle_quantized == 135)

    # Get neighbors for each direction
    # 0°: left and right
    left = np.roll(magnitude, 1, axis=1)
    right = np.roll(magnitude, -1, axis=1)

    # 45°: diagonal
    diag1 = np.roll(np.roll(magnitude, 1, axis=0), 1, axis=1)
    diag2 = np.roll(np.roll(magnitude, -1, axis=0), -1, axis=1)

    # 90°: top and bottom
    top = np.roll(magnitude, 1, axis=0)
    bottom = np.roll(magnitude, -1, axis=0)

    # 135°: diagonal
    diag3 = np.roll(np.roll(magnitude, 1, axis=0), -1, axis=1)
    diag4 = np.roll(np.roll(magnitude, -1, axis=0), 1, axis=1)

    # Apply non-max suppression for each direction
    result = np.where(
        (mask_0 & (magnitude >= left) & (magnitude >= right)) |
        (mask_45 & (magnitude >= diag1) & (magnitude >= diag2)) |
        (mask_90 & (magnitude >= top) & (magnitude >= bottom)) |
        (mask_135 & (magnitude >= diag3) & (magnitude >= diag4)),
        magnitude, 0
    )

    # Set border pixels to 0
    result[0, :] = 0
    result[-1, :] = 0
    result[:, 0] = 0
    result[:, -1] = 0

    return result


def double_threshold(image, low, high):
    """
    Double threshold tối ưu (Bước 4: Phân loại strong/weak edges).
    """
    # Vectorized thresholding
    strong = (image >= high)
    weak = (image >= low) & (image < high)

    # Create result array with proper values
    result = np.zeros_like(image, dtype=np.uint8)
    result[strong] = 255
    result[weak] = 128  # Weak edges (easier to track)

    return result


def hysteresis_optimized(image):
    """
    Hysteresis tối ưu (Bước 5: Nối weak edges với strong).
    """
    # Create a copy to avoid modifying original
    result = image.copy()

    # Find weak edges (value = 128)
    weak_mask = (result == 128)

    # Use morphological operations for faster processing

    # Create 8-connectivity kernel
    kernel = np.ones((3, 3), dtype=np.uint8)

    # Find strong edges (value = 255)
    strong_mask = (result == 255)

    # Dilate strong edges to find connected weak edges
    strong_dilated = ndimage.binary_dilation(strong_mask, structure=kernel)

    # Keep weak edges that are connected to strong edges
    result[weak_mask & strong_dilated] = 255

    # Remove remaining weak edges
    result[weak_mask & ~strong_dilated] = 0

    return result


def canny_optimized(image, sigma=1.0, low_thresh=50, high_thresh=150, kernel_size=5):
    """
    Canny tối ưu với vectorized operations.
    Input: Ảnh grayscale (float32 hoặc uint8).
    Output: Edges (uint8).
    """
    # Convert to float32 for better precision
    if image.dtype != np.float32:
        image = image.astype(np.float32)

    # Bước 1: Gaussian blur (tối ưu)
    gaussian_k = gaussian_kernel(kernel_size, sigma)
    smoothed = convolve(image, gaussian_k)

    # Bước 2: Sobel gradients (tối ưu)
    magnitude, angle = sobel_gradients(smoothed)

    # Bước 3: Non-maximum suppression (tối ưu)
    nms = non_max_suppression(magnitude, angle)

    # Bước 4: Double threshold (tối ưu)
    thresh = double_threshold(nms, low_thresh, high_thresh)

    # Bước 5: Hysteresis (tối ưu)
    edges = hysteresis_optimized(thresh)

    return edges.astype(np.uint8)


def median_filter(image, kernel_size=3):
    # Đảm bảo kích thước kernel là số lẻ
    assert kernel_size % 2 == 1, "Kích thước kernel phải là số lẻ."

    # Lấy kích thước ảnh
    m, n = image.shape

    # Tính toán biên của kernel
    pad_size = kernel_size // 2

    # Thêm padding vào ảnh gốc
    padded_image = np.pad(image, pad_size, mode='edge')

    # Tạo sliding window view
    windows = sliding_window_view(padded_image, (kernel_size, kernel_size))

    # Tính median cho tất cả windows cùng lúc
    filtered_image = np.median(windows, axis=(2, 3))

    return filtered_image.astype(image.dtype)


@app.route('/', methods=['GET'])
def get_process_info():
    print('hello world')
    algorithms = {
        'canny': 'Phát hiện biên (Canny) - Thủ công',
        'canny_opencv': 'Phát hiện biên (Canny) - OpenCV',
        'median': 'Lọc trung vị (Median Filter)'
    }
    return jsonify({
        'message': 'Danh sách thuật toán hỗ trợ',
        'algorithms': algorithms
    })


@app.route('/process', methods=['POST'])
def process_image():
    try:
        file = request.files['image']
        algorithm = request.form.get('algorithm', 'canny')
        kernel_size = int(request.form.get('kernel_size', 3))

        # Tham số cho Canny
        low_threshold = int(request.form.get('low_threshold', 50))
        high_threshold = int(request.form.get('high_threshold', 150))
        sigma = float(request.form.get('sigma', 1.0))

        # Validate kernel size
        if kernel_size % 2 == 0:
            kernel_size += 1

        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if algorithm == 'canny':
            # Try optimized version first, fallback to manual
            processed = canny_optimized(gray, sigma, low_threshold, high_threshold)
        elif algorithm == 'median':
            processed = median_filter(gray, kernel_size)
        else:
            return jsonify({'error': 'Thuật toán không hợp lệ'}), 400

        print(f"Encoding image to JPEG...")
        success, buffer = cv2.imencode('.jpg', processed)
        if not success:
            print("ERROR: Failed to encode image to JPEG")
            return jsonify({'error': 'Lỗi encode ảnh'}), 500
        processed = buffer.tobytes()
        print(f"Encoded image size: {len(processed)} bytes")

        img_base64 = base64.b64encode(processed).decode('utf-8')
        print(f"Base64 length: {len(img_base64)}")

        response_data = {
            'processed_image': img_base64,
            'algorithm_used': algorithm,
        }

        # Thêm tham số tương ứng
        if algorithm in ['median']:
            response_data['kernel_size'] = kernel_size
        elif algorithm in ['canny', 'canny_opencv']:
            response_data['low_threshold'] = low_threshold
            response_data['high_threshold'] = high_threshold
            if algorithm == 'canny':
                response_data['sigma'] = sigma

        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Lỗi xử lý ảnh: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
