import cv2
import numpy as np
from typing import Dict, Any, Optional
from entities.image import Image
from entities.filters import BaseFilter
from .filter_factory import FilterFactory


class ImageProcessor:
    """
    Service class để xử lý ảnh với các filter khác nhau
    """
    
    def __init__(self):
        self.filter_factory = FilterFactory()
    
    def process_image_from_file(self, file_data: bytes, algorithm: str, 
                              parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Xử lý ảnh từ file data
        
        Args:
            file_data: Dữ liệu file ảnh
            algorithm: Thuật toán xử lý
            parameters: Tham số cho thuật toán
            
        Returns:
            Dictionary chứa kết quả xử lý
        """
        try:
            # Tạo Image entity từ file data
            image = self._create_image_from_bytes(file_data)
            
            # Lấy tham số mặc định nếu không có
            if parameters is None:
                parameters = self.filter_factory.get_default_parameters(algorithm)
            
            # Tạo filter
            filter_instance = self.filter_factory.create_filter(algorithm, parameters)
            
            # Xử lý ảnh
            processed_image = filter_instance.apply(image)
            
            # Encode kết quả
            processed_base64 = processed_image.encode_to_base64()
            
            # Tạo response data
            response_data = {
                'processed_image': processed_base64,
                'algorithm_used': algorithm,
                'original_metadata': {
                    'width': image.metadata.width,
                    'height': image.metadata.height,
                    'channels': image.metadata.channels,
                    'dtype': image.metadata.dtype
                },
                'processed_metadata': {
                    'width': processed_image.metadata.width,
                    'height': processed_image.metadata.height,
                    'channels': processed_image.metadata.channels,
                    'dtype': processed_image.metadata.dtype
                }
            }
            
            # Thêm tham số đã sử dụng
            response_data.update(parameters)
            
            return response_data
            
        except Exception as e:
            raise ValueError(f"Lỗi xử lý ảnh: {str(e)}")
    
    def process_image_from_array(self, image_array: np.ndarray, algorithm: str,
                               parameters: Optional[Dict[str, Any]] = None) -> Image:
        """
        Xử lý ảnh từ numpy array
        
        Args:
            image_array: Dữ liệu ảnh dạng numpy array
            algorithm: Thuật toán xử lý
            parameters: Tham số cho thuật toán
            
        Returns:
            Image entity đã được xử lý
        """
        try:
            # Tạo Image entity từ array
            image = Image(image_data=image_array)
            
            # Lấy tham số mặc định nếu không có
            if parameters is None:
                parameters = self.filter_factory.get_default_parameters(algorithm)
            
            # Tạo filter
            filter_instance = self.filter_factory.create_filter(algorithm, parameters)
            
            # Xử lý ảnh
            processed_image = filter_instance.apply(image)
            
            return processed_image
            
        except Exception as e:
            raise ValueError(f"Lỗi xử lý ảnh: {str(e)}")
    
    def _create_image_from_bytes(self, file_data: bytes) -> Image:
        """
        Tạo Image entity từ file bytes
        
        Args:
            file_data: Dữ liệu file ảnh
            
        Returns:
            Image entity
        """
        try:
            # Decode ảnh từ bytes
            img_array = np.frombuffer(file_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Không thể decode ảnh từ file data")
            
            return Image(image_data=img)
            
        except Exception as e:
            raise ValueError(f"Lỗi tạo ảnh từ bytes: {str(e)}")
    
    def get_supported_algorithms(self) -> Dict[str, str]:
        """
        Trả về danh sách các thuật toán được hỗ trợ
        
        Returns:
            Dictionary mapping algorithm name to description
        """
        return self.filter_factory.get_supported_filters()
    
    def get_algorithm_parameters(self, algorithm: str) -> Dict[str, Any]:
        """
        Trả về tham số mặc định cho thuật toán
        
        Args:
            algorithm: Tên thuật toán
            
        Returns:
            Dictionary chứa tham số mặc định
        """
        return self.filter_factory.get_default_parameters(algorithm)
    
    def validate_parameters(self, algorithm: str, parameters: Dict[str, Any]) -> bool:
        """
        Validate tham số cho thuật toán
        
        Args:
            algorithm: Tên thuật toán
            parameters: Tham số cần validate
            
        Returns:
            True nếu hợp lệ, False nếu không
        """
        try:
            self.filter_factory.create_filter(algorithm, parameters)
            return True
        except Exception:
            return False
