#!/usr/bin/env python3
"""
Simple test for median filter
"""

import numpy as np
import cv2
from app import median_filter

def test_median_filter():
    # Tạo ảnh test đơn giản
    img = np.random.randint(0, 256, (50, 50), dtype=np.uint8)
    
    # Thêm noise
    img[img < 20] = 0
    img[img > 235] = 255
    
    print(f"Original image shape: {img.shape}")
    print(f"Original image min: {img.min()}, max: {img.max()}")
    
    # Áp dụng median filter
    filtered = median_filter(img, kernel_size=3)
    
    print(f"Filtered image shape: {filtered.shape}")
    print(f"Filtered image min: {filtered.min()}, max: {filtered.max()}")
    
    # Test encode
    success, buffer = cv2.imencode('.jpg', filtered)
    print(f"Encode success: {success}")
    if success:
        print(f"Buffer size: {len(buffer)} bytes")
        
        # Test base64
        import base64
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        print(f"Base64 length: {len(img_base64)}")
        print(f"Base64 preview: {img_base64[:50]}...")
    
    return filtered

if __name__ == "__main__":
    print("Testing median filter...")
    result = test_median_filter()
    print("Test completed!")
