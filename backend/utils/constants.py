"""
Constants cho image processing service
"""

# Supported image formats
SUPPORTED_IMAGE_FORMATS = {
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/bmp': ['.bmp'],
    'image/tiff': ['.tiff', '.tif']
}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Default parameters
DEFAULT_CANNY_PARAMS = {
    'sigma': 1.0,
    'low_threshold': 50,
    'high_threshold': 150,
    'kernel_size': 5
}

DEFAULT_MEDIAN_PARAMS = {
    'kernel_size': 3
}

# Parameter limits
PARAMETER_LIMITS = {
    'canny': {
        'sigma': {'min': 0.1, 'max': 10.0},
        'low_threshold': {'min': 0, 'max': 255},
        'high_threshold': {'min': 0, 'max': 255},
        'kernel_size': {'min': 3, 'max': 15}
    },
    'median': {
        'kernel_size': {'min': 3, 'max': 15}
    }
}
