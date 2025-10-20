import cv2
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dataclasses import dataclass
from scipy import ndimage
from numpy.lib.stride_tricks import sliding_window_view
import math

from .image import Image


@dataclass
class FilterParameters:
    """Base class cho các tham số của filter"""
    pass


@dataclass
class CannyParameters(FilterParameters):
    """Tham số cho Canny filter"""
    sigma: float = 1.0
    low_threshold: int = 50
    high_threshold: int = 150
    kernel_size: int = 5


@dataclass
class MedianParameters(FilterParameters):
    """Tham số cho Median filter"""
    kernel_size: int = 3


class BaseFilter(ABC):
    """Base class cho tất cả các filter"""
    
    def __init__(self, parameters: FilterParameters):
        self.parameters = parameters
    
    @abstractmethod
    def apply(self, image: Image) -> Image:
        """Áp dụng filter lên ảnh"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Trả về tên của filter"""
        pass


class CannyEdgeDetector(BaseFilter):
    def __init__(self, parameters: CannyParameters):
        super().__init__(parameters)
        self._validate_parameters()
    
    def _validate_parameters(self):
        params = self.parameters
        if params.kernel_size % 2 == 0:
            raise ValueError("Kernel size phải là số lẻ!")
        if params.low_threshold >= params.high_threshold:
            raise ValueError("Low threshold phải nhỏ hơn high threshold!")
        if params.sigma <= 0:
            raise ValueError("Sigma phải lớn hơn 0!")
    
    def get_name(self) -> str:
        return "Canny Edge Detection"
    
    def apply(self, image: Image) -> Image:
        if len(image.shape) == 3:
            gray_image = image.to_grayscale()
        else:
            gray_image = image
        
        float_image = gray_image.to_float32()
        
        edges = self._canny(
            float_image.data,
            self.parameters.sigma,
            self.parameters.low_threshold,
            self.parameters.high_threshold,
            self.parameters.kernel_size
        )
        
        return Image(image_data=edges.astype(np.uint8))
    
    def _gaussian_kernel(self, size: int, sigma: float) -> np.ndarray:
        if size % 2 == 0:
            raise ValueError("Kernel size phải là số lẻ!")
        
        center = size // 2
        x = np.arange(size) - center
        y = np.arange(size) - center
        X, Y = np.meshgrid(x, y)
        
        kernel = np.exp(-(X ** 2 + Y ** 2) / (2 * sigma ** 2))
        return kernel / np.sum(kernel)
    
    def _convolve(self, image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        kh, kw = kernel.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        
        windows = sliding_window_view(padded, (kh, kw))
        result = np.sum(windows * kernel, axis=(2, 3))
        
        return result
    
    def _sobel_gradients(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        
        gx = self._convolve(image, sobel_x)
        gy = self._convolve(image, sobel_y)
        
        magnitude = np.sqrt(gx ** 2 + gy ** 2)
        angle = np.arctan2(gy, gx) * (180 / np.pi) % 180
        
        return magnitude, angle
    
    def _non_max_suppression(self, magnitude: np.ndarray, angle: np.ndarray) -> np.ndarray:
        h, w = magnitude.shape
        result = np.zeros_like(magnitude)
        
        angle_quantized = np.round(angle / 45) * 45
        angle_quantized = angle_quantized % 180
        
        mask_0 = (angle_quantized == 0) | (angle_quantized == 180)
        mask_45 = (angle_quantized == 45)
        mask_90 = (angle_quantized == 90)
        mask_135 = (angle_quantized == 135)
        
        left = np.roll(magnitude, 1, axis=1)
        right = np.roll(magnitude, -1, axis=1)
        diag1 = np.roll(np.roll(magnitude, 1, axis=0), 1, axis=1)
        diag2 = np.roll(np.roll(magnitude, -1, axis=0), -1, axis=1)
        top = np.roll(magnitude, 1, axis=0)
        bottom = np.roll(magnitude, -1, axis=0)
        diag3 = np.roll(np.roll(magnitude, 1, axis=0), -1, axis=1)
        diag4 = np.roll(np.roll(magnitude, -1, axis=0), 1, axis=1)
        
        result = np.where(
            (mask_0 & (magnitude >= left) & (magnitude >= right)) |
            (mask_45 & (magnitude >= diag1) & (magnitude >= diag2)) |
            (mask_90 & (magnitude >= top) & (magnitude >= bottom)) |
            (mask_135 & (magnitude >= diag3) & (magnitude >= diag4)),
            magnitude, 0
        )
        
        result[0, :] = 0
        result[-1, :] = 0
        result[:, 0] = 0
        result[:, -1] = 0
        
        return result
    
    def _double_threshold(self, image: np.ndarray, low: int, high: int) -> np.ndarray:
        strong = (image >= high)
        weak = (image >= low) & (image < high)
        
        result = np.zeros_like(image, dtype=np.uint8)
        result[strong] = 255
        result[weak] = 128
        
        return result
    
    def _hysteresis(self, image: np.ndarray) -> np.ndarray:
        result = image.copy()
        weak_mask = (result == 128)
        kernel = np.ones((3, 3), dtype=np.uint8)
        strong_mask = (result == 255)
        
        strong_dilated = ndimage.binary_dilation(strong_mask, structure=kernel)
        result[weak_mask & strong_dilated] = 255
        result[weak_mask & ~strong_dilated] = 0
        
        return result
    
    def _canny(self, image: np.ndarray, sigma: float, low_thresh: int, 
                        high_thresh: int, kernel_size: int) -> np.ndarray:
        if image.dtype != np.float32:
            image = image.astype(np.float32)
        
        gaussian_k = self._gaussian_kernel(kernel_size, sigma)
        smoothed = self._convolve(image, gaussian_k)
        
        magnitude, angle = self._sobel_gradients(smoothed)
        nms = self._non_max_suppression(magnitude, angle)
        thresh = self._double_threshold(nms, low_thresh, high_thresh)
        edges = self._hysteresis(thresh)
        
        return edges.astype(np.uint8)


class MedianFilter(BaseFilter):    
    def __init__(self, parameters: MedianParameters):
        super().__init__(parameters)
        self._validate_parameters()
    
    def _validate_parameters(self):
        if self.parameters.kernel_size % 2 == 0:
            raise ValueError("Kernel size phải là số lẻ!")
        if self.parameters.kernel_size < 3:
            raise ValueError("Kernel size phải lớn hơn hoặc bằng 3!")
    
    def get_name(self) -> str:
        return "Median Filter"
    
    def apply(self, image: Image) -> Image:
        if len(image.shape) == 3:
            gray_image = image.to_grayscale()
        else:
            gray_image = image
        
        filtered_data = self._median_filter(
            gray_image.data, 
            self.parameters.kernel_size
        )
        
        return Image(image_data=filtered_data.astype(image.dtype))
    
    def _median_filter(self, image: np.ndarray, kernel_size: int) -> np.ndarray:
        m, n = image.shape
        pad_size = kernel_size // 2
        padded_image = np.pad(image, pad_size, mode='edge')
        
        windows = sliding_window_view(padded_image, (kernel_size, kernel_size))
        filtered_image = np.median(windows, axis=(2, 3))
        
        return filtered_image.astype(image.dtype)
