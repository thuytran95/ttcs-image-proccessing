"""
Validation utilities cho image processing service
"""

from typing import Dict, Any, List, Tuple
from .constants import PARAMETER_LIMITS, MAX_FILE_SIZE, SUPPORTED_IMAGE_FORMATS


class ParameterValidator:
    """
    Class để validate các tham số đầu vào
    """
    
    @staticmethod
    def validate_algorithm(algorithm: str) -> Tuple[bool, str]:
        """
        Validate tên thuật toán
        
        Args:
            algorithm: Tên thuật toán
            
        Returns:
            Tuple (is_valid, error_message)
        """
        supported_algorithms = list(PARAMETER_LIMITS.keys())
        
        if not algorithm:
            return False, "Tên thuật toán không được để trống"
        
        if algorithm not in supported_algorithms:
            return False, f"Thuật toán '{algorithm}' không được hỗ trợ. Các thuật toán hỗ trợ: {', '.join(supported_algorithms)}"
        
        return True, ""
    
    @staticmethod
    def validate_parameters(algorithm: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate tham số cho thuật toán
        
        Args:
            algorithm: Tên thuật toán
            parameters: Dictionary chứa tham số
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if algorithm not in PARAMETER_LIMITS:
            return False, f"Không có thông tin giới hạn cho thuật toán '{algorithm}'"
        
        limits = PARAMETER_LIMITS[algorithm]
        
        for param_name, value in parameters.items():
            if param_name not in limits:
                return False, f"Tham số '{param_name}' không hợp lệ cho thuật toán '{algorithm}'"
            
            param_limits = limits[param_name]
            
            # Validate min/max
            if 'min' in param_limits and value < param_limits['min']:
                return False, f"Tham số '{param_name}' phải >= {param_limits['min']}"
            
            if 'max' in param_limits and value > param_limits['max']:
                return False, f"Tham số '{param_name}' phải <= {param_limits['max']}"
            
            # Validate kernel size is odd
            if param_name == 'kernel_size' and value % 2 == 0:
                return False, f"Tham số '{param_name}' phải là số lẻ"
        
        return True, ""
    
    @staticmethod
    def validate_file_size(file_size: int) -> Tuple[bool, str]:
        """
        Validate kích thước file
        
        Args:
            file_size: Kích thước file (bytes)
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if file_size <= 0:
            return False, "File không được trống"
        
        if file_size > MAX_FILE_SIZE:
            return False, f"File quá lớn. Kích thước tối đa: {MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, ""
    
    @staticmethod
    def validate_image_format(filename: str) -> Tuple[bool, str]:
        """
        Validate định dạng file ảnh
        
        Args:
            filename: Tên file
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not filename:
            return False, "Tên file không được để trống"
        
        # Lấy extension
        if '.' not in filename:
            return False, "File phải có extension"
        
        extension = '.' + filename.split('.')[-1].lower()
        
        # Check if extension is supported
        for mime_type, extensions in SUPPORTED_IMAGE_FORMATS.items():
            if extension in extensions:
                return True, ""
        
        supported_extensions = []
        for extensions in SUPPORTED_IMAGE_FORMATS.values():
            supported_extensions.extend(extensions)
        
        return False, f"Định dạng file không được hỗ trợ. Các định dạng hỗ trợ: {', '.join(supported_extensions)}"
    
    @staticmethod
    def validate_canny_parameters(parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate tham số Canny cụ thể
        
        Args:
            parameters: Tham số Canny
            
        Returns:
            Tuple (is_valid, error_message)
        """
        # Check required parameters
        required_params = ['sigma', 'low_threshold', 'high_threshold', 'kernel_size']
        for param in required_params:
            if param not in parameters:
                return False, f"Tham số '{param}' là bắt buộc"
        
        # Check low_threshold < high_threshold
        if parameters['low_threshold'] >= parameters['high_threshold']:
            return False, "Low threshold phải nhỏ hơn high threshold"
        
        return ParameterValidator.validate_parameters('canny', parameters)
    
    @staticmethod
    def validate_median_parameters(parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate tham số Median cụ thể
        
        Args:
            parameters: Tham số Median
            
        Returns:
            Tuple (is_valid, error_message)
        """
        # Check required parameters
        if 'kernel_size' not in parameters:
            return False, "Tham số 'kernel_size' là bắt buộc"
        
        return ParameterValidator.validate_parameters('median', parameters)
