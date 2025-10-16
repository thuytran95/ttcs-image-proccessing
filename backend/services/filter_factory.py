from typing import Dict, Any
from entities.filters import BaseFilter, CannyFilter, MedianFilter, CannyParameters, MedianParameters


class FilterFactory:
    """
    Factory class để tạo các filter instances
    """
    
    _filter_registry = {
        'canny': CannyFilter,
        'median': MedianFilter,
    }
    
    @classmethod
    def create_filter(cls, filter_type: str, parameters: Dict[str, Any]) -> BaseFilter:
        """
        Tạo filter instance dựa trên type và parameters
        
        Args:
            filter_type: Loại filter ('canny', 'median')
            parameters: Dictionary chứa các tham số
            
        Returns:
            BaseFilter instance
        """
        if filter_type not in cls._filter_registry:
            raise ValueError(f"Filter type '{filter_type}' không được hỗ trợ")
        
        filter_class = cls._filter_registry[filter_type]
        
        # Tạo parameters object tương ứng
        if filter_type == 'canny':
            params = CannyParameters(**parameters)
        elif filter_type == 'median':
            params = MedianParameters(**parameters)
        else:
            raise ValueError(f"Không thể tạo parameters cho filter type '{filter_type}'")
        
        return filter_class(params)
    
    @classmethod
    def get_supported_filters(cls) -> Dict[str, str]:
        """
        Trả về danh sách các filter được hỗ trợ
        
        Returns:
            Dictionary mapping filter type to description
        """
        return {
            'canny': 'Phát hiện biên (Canny) - Thủ công',
            'median': 'Lọc trung vị (Median Filter)'
        }
    
    @classmethod
    def get_default_parameters(cls, filter_type: str) -> Dict[str, Any]:
        """
        Trả về các tham số mặc định cho filter type
        
        Args:
            filter_type: Loại filter
            
        Returns:
            Dictionary chứa các tham số mặc định
        """
        defaults = {
            'canny': {
                'sigma': 1.0,
                'low_threshold': 50,
                'high_threshold': 150,
                'kernel_size': 5
            },
            'median': {
                'kernel_size': 3
            }
        }
        
        if filter_type not in defaults:
            raise ValueError(f"Filter type '{filter_type}' không được hỗ trợ")
        
        return defaults[filter_type]
