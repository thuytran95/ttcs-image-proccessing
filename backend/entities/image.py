import cv2
import numpy as np
from typing import Optional, Union
from dataclasses import dataclass


@dataclass
class ImageMetadata:
    """Metadata của ảnh"""
    width: int
    height: int
    channels: int
    dtype: str
    size_bytes: int


class Image:
    """
    Entity class đại diện cho một ảnh và các thao tác cơ bản
    """
    
    def __init__(self, image_data: Optional[np.ndarray] = None, file_path: Optional[str] = None):
        """
        Khởi tạo Image entity
        
        Args:
            image_data: Dữ liệu ảnh dạng numpy array
            file_path: Đường dẫn file ảnh
        """
        if image_data is not None:
            self._data = image_data.copy()
        elif file_path is not None:
            self._data = self._load_from_file(file_path)
        else:
            raise ValueError("Phải cung cấp image_data hoặc file_path")
        
        self._metadata = self._extract_metadata()
    
    @property
    def data(self) -> np.ndarray:
        """Trả về dữ liệu ảnh"""
        return self._data.copy()
    
    @property
    def metadata(self) -> ImageMetadata:
        """Trả về metadata của ảnh"""
        return self._metadata
    
    @property
    def shape(self) -> tuple:
        """Trả về shape của ảnh"""
        return self._data.shape
    
    @property
    def dtype(self) -> np.dtype:
        """Trả về kiểu dữ liệu của ảnh"""
        return self._data.dtype
    
    def _load_from_file(self, file_path: str) -> np.ndarray:
        """Tải ảnh từ file"""
        try:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Không thể tải ảnh từ {file_path}")
            return image
        except Exception as e:
            raise ValueError(f"Lỗi tải ảnh: {str(e)}")
    
    def _extract_metadata(self) -> ImageMetadata:
        """Trích xuất metadata từ ảnh"""
        height, width = self._data.shape[:2]
        channels = 1 if len(self._data.shape) == 2 else self._data.shape[2]
        dtype = str(self._data.dtype)
        size_bytes = self._data.nbytes
        
        return ImageMetadata(
            width=width,
            height=height,
            channels=channels,
            dtype=dtype,
            size_bytes=size_bytes
        )
    
    def to_grayscale(self) -> 'Image':
        """Chuyển ảnh sang grayscale"""
        if len(self._data.shape) == 3:
            gray = cv2.cvtColor(self._data, cv2.COLOR_BGR2GRAY)
            return Image(image_data=gray)
        return self
    
    def resize(self, width: int, height: int) -> 'Image':
        """Thay đổi kích thước ảnh"""
        resized = cv2.resize(self._data, (width, height))
        return Image(image_data=resized)
    
    def normalize(self, min_val: float = 0.0, max_val: float = 1.0) -> 'Image':
        """Chuẩn hóa ảnh về khoảng [min_val, max_val]"""
        normalized = cv2.normalize(
            self._data, None, 
            alpha=min_val, beta=max_val, 
            norm_type=cv2.NORM_MINMAX, 
            dtype=cv2.CV_32F
        )
        return Image(image_data=normalized)
    
    def to_uint8(self) -> 'Image':
        """Chuyển ảnh về kiểu uint8"""
        if self._data.dtype != np.uint8:
            # Normalize về [0, 255] trước khi convert
            normalized = cv2.normalize(
                self._data, None, 
                alpha=0, beta=255, 
                norm_type=cv2.NORM_MINMAX, 
                dtype=cv2.CV_8U
            )
            return Image(image_data=normalized)
        return self
    
    def to_float32(self) -> 'Image':
        """Chuyển ảnh về kiểu float32"""
        if self._data.dtype != np.float32:
            return Image(image_data=self._data.astype(np.float32))
        return self
    
    def encode_to_jpeg(self, quality: int = 95) -> bytes:
        """Encode ảnh thành JPEG bytes"""
        success, buffer = cv2.imencode('.jpg', self._data, [cv2.IMWRITE_JPEG_QUALITY, quality])
        if not success:
            raise ValueError("Không thể encode ảnh thành JPEG")
        return buffer.tobytes()
    
    def encode_to_base64(self, quality: int = 95) -> str:
        """Encode ảnh thành base64 string"""
        import base64
        jpeg_bytes = self.encode_to_jpeg(quality)
        return base64.b64encode(jpeg_bytes).decode('utf-8')
    
    def copy(self) -> 'Image':
        """Tạo bản sao của ảnh"""
        return Image(image_data=self._data.copy())
    
    def __str__(self) -> str:
        return f"Image(shape={self.shape}, dtype={self.dtype})"
    
    def __repr__(self) -> str:
        return self.__str__()
