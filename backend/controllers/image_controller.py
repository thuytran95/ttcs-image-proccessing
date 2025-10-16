from flask import request, jsonify
from typing import Dict, Any, Optional
from services.image_processor import ImageProcessor


class ImageController:
    """
    Controller class để xử lý các HTTP requests liên quan đến ảnh
    """
    
    def __init__(self):
        self.image_processor = ImageProcessor()
    
    def get_process_info(self) -> Dict[str, Any]:
        """
        Trả về thông tin về các thuật toán được hỗ trợ
        
        Returns:
            JSON response với danh sách thuật toán
        """
        try:
            algorithms = self.image_processor.get_supported_algorithms()
            
            return {
                'message': 'Danh sách thuật toán hỗ trợ',
                'algorithms': algorithms,
                'status': 'success'
            }
        except Exception as e:
            return {
                'error': f'Lỗi lấy thông tin: {str(e)}',
                'status': 'error'
            }
    
    def process_image(self) -> Dict[str, Any]:
        """
        Xử lý ảnh theo thuật toán được chỉ định
        
        Returns:
            JSON response với ảnh đã xử lý
        """
        try:
            # Validate request
            if 'image' not in request.files:
                return {
                    'error': 'Không tìm thấy file ảnh',
                    'status': 'error'
                }, 400
            
            file = request.files['image']
            if file.filename == '':
                return {
                    'error': 'File ảnh trống',
                    'status': 'error'
                }, 400
            
            # Lấy tham số từ form data
            algorithm = request.form.get('algorithm', 'canny')
            parameters = self._extract_parameters(algorithm)
            
            # Validate algorithm
            if algorithm not in self.image_processor.get_supported_algorithms():
                return {
                    'error': f'Thuật toán "{algorithm}" không được hỗ trợ',
                    'status': 'error'
                }, 400
            
            # Validate parameters
            if not self.image_processor.validate_parameters(algorithm, parameters):
                return {
                    'error': 'Tham số không hợp lệ',
                    'status': 'error'
                }, 400
            
            # Xử lý ảnh
            result = self.image_processor.process_image_from_file(
                file.read(), 
                algorithm, 
                parameters
            )
            
            result['status'] = 'success'
            return result
            
        except ValueError as e:
            return {
                'error': str(e),
                'status': 'error'
            }, 400
        except Exception as e:
            return {
                'error': f'Lỗi xử lý ảnh: {str(e)}',
                'status': 'error'
            }, 500
    
    def _extract_parameters(self, algorithm: str) -> Dict[str, Any]:
        """
        Trích xuất tham số từ form data dựa trên thuật toán
        
        Args:
            algorithm: Tên thuật toán
            
        Returns:
            Dictionary chứa tham số
        """
        parameters = {}
        
        if algorithm == 'canny':
            parameters = {
                'sigma': float(request.form.get('sigma', 1.0)),
                'low_threshold': int(request.form.get('low_threshold', 50)),
                'high_threshold': int(request.form.get('high_threshold', 150)),
                'kernel_size': int(request.form.get('kernel_size', 5))
            }
        elif algorithm == 'median':
            parameters = {
                'kernel_size': int(request.form.get('kernel_size', 3))
            }
        
        # Validate kernel size
        if 'kernel_size' in parameters:
            kernel_size = parameters['kernel_size']
            if kernel_size % 2 == 0:
                parameters['kernel_size'] = kernel_size + 1
        
        return parameters
    
    def get_algorithm_info(self, algorithm: str) -> Dict[str, Any]:
        """
        Trả về thông tin chi tiết về một thuật toán
        
        Args:
            algorithm: Tên thuật toán
            
        Returns:
            JSON response với thông tin thuật toán
        """
        try:
            if algorithm not in self.image_processor.get_supported_algorithms():
                return {
                    'error': f'Thuật toán "{algorithm}" không được hỗ trợ',
                    'status': 'error'
                }, 404
            
            parameters = self.image_processor.get_algorithm_parameters(algorithm)
            description = self.image_processor.get_supported_algorithms()[algorithm]
            
            return {
                'algorithm': algorithm,
                'description': description,
                'parameters': parameters,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': f'Lỗi lấy thông tin thuật toán: {str(e)}',
                'status': 'error'
            }, 500
