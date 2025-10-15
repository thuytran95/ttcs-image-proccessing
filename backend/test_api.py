#!/usr/bin/env python3
"""
Test API directly
"""

import requests
import json

def test_api():
    # Tạo ảnh test đơn giản
    import numpy as np
    import cv2
    import io
    
    # Tạo ảnh test
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    img[img < 20] = 0
    img[img > 235] = 255
    
    # Encode thành JPEG
    _, buffer = cv2.imencode('.jpg', img)
    img_bytes = buffer.tobytes()
    
    # Test API
    url = "http://localhost:5000/process"
    
    files = {
        'image': ('test.jpg', img_bytes, 'image/jpeg')
    }
    
    data = {
        'algorithm': 'median',
        'kernel_size': '3'
    }
    
    print("Testing API...")
    print(f"URL: {url}")
    print(f"Algorithm: {data['algorithm']}")
    print(f"Kernel size: {data['kernel_size']}")
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response keys: {result.keys()}")
            print(f"Algorithm used: {result.get('algorithm_used')}")
            print(f"Kernel size: {result.get('kernel_size')}")
            print(f"Processed image length: {len(result.get('processed_image', ''))}")
            print(f"Processed image preview: {result.get('processed_image', '')[:50]}...")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()
