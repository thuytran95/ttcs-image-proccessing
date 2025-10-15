#!/usr/bin/env python3
"""
Test manual Canny edge detection
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from app import canny_edge_detection

def create_test_image():
    """Tạo ảnh test với các hình dạng đơn giản"""
    # Tạo ảnh trắng
    img = np.ones((200, 200), dtype=np.uint8) * 255
    
    # Vẽ hình chữ nhật
    cv2.rectangle(img, (50, 50), (150, 100), 0, -1)
    
    # Vẽ hình tròn
    cv2.circle(img, (100, 150), 30, 0, -1)
    
    # Thêm noise
    noise = np.random.normal(0, 10, img.shape)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    return img

def test_canny_steps():
    """Test từng bước của Canny"""
    print("=== Testing Manual Canny Edge Detection ===\n")
    
    # Tạo ảnh test
    img = create_test_image()
    print(f"Test image shape: {img.shape}")
    print(f"Test image range: {img.min()} - {img.max()}")
    
    # Test với các tham số khác nhau
    test_params = [
        {"low": 30, "high": 100, "sigma": 1.0},
        {"low": 50, "high": 150, "sigma": 1.0},
        {"low": 70, "high": 200, "sigma": 1.5},
    ]
    
    results = []
    
    for i, params in enumerate(test_params):
        print(f"\n--- Test {i+1}: low={params['low']}, high={params['high']}, sigma={params['sigma']} ---")
        
        try:
            result = canny_edge_detection(img, **params)
            results.append((params, result))
            print(f"✅ Success! Result shape: {result.shape}")
            print(f"   Edge pixels: {np.sum(result > 0)}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return img, results

def compare_with_opencv():
    """So sánh với OpenCV Canny"""
    print("\n=== Comparing with OpenCV Canny ===\n")
    
    img = create_test_image()
    
    # Manual Canny
    print("Manual Canny...")
    manual_result = canny_edge_detection(img, 50, 150, 1.0)
    
    # OpenCV Canny
    print("OpenCV Canny...")
    opencv_result = cv2.Canny(img, 50, 150)
    
    # So sánh
    mse = np.mean((manual_result - opencv_result) ** 2)
    print(f"MSE between manual and OpenCV: {mse:.6f}")
    
    # Thống kê
    print(f"Manual edges: {np.sum(manual_result > 0)}")
    print(f"OpenCV edges: {np.sum(opencv_result > 0)}")
    
    return img, manual_result, opencv_result

def visualize_results(img, manual_result, opencv_result):
    """Hiển thị kết quả"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    axes[1].imshow(manual_result, cmap='gray')
    axes[1].set_title('Manual Canny')
    axes[1].axis('off')
    
    axes[2].imshow(opencv_result, cmap='gray')
    axes[2].set_title('OpenCV Canny')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('canny_comparison.png', dpi=150, bbox_inches='tight')
    print("Results saved to 'canny_comparison.png'")

if __name__ == "__main__":
    print("🔬 Testing Manual Canny Edge Detection\n")
    
    # Test các bước
    img, results = test_canny_steps()
    
    # So sánh với OpenCV
    img, manual_result, opencv_result = compare_with_opencv()
    
    # Hiển thị kết quả
    try:
        visualize_results(img, manual_result, opencv_result)
    except ImportError:
        print("Matplotlib not available, skipping visualization")
    
    print("\n✅ Testing completed!")
