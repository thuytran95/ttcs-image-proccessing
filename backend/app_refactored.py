from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.image_controller import ImageController

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)

# Khởi tạo controller
image_controller = ImageController()


@app.route('/', methods=['GET'])
def get_process_info():
    """
    Endpoint để lấy thông tin về các thuật toán được hỗ trợ
    """
    result = image_controller.get_process_info()
    
    if result.get('status') == 'error':
        return jsonify(result), 500
    
    return jsonify(result)


@app.route('/process', methods=['POST'])
def process_image():
    """
    Endpoint để xử lý ảnh
    """
    result = image_controller.process_image()
    
    if result.get('status') == 'error':
        error_code = 400 if 'error' in result else 500
        return jsonify(result), error_code
    
    return jsonify(result)


@app.route('/algorithms/<algorithm>', methods=['GET'])
def get_algorithm_info(algorithm):
    """
    Endpoint để lấy thông tin chi tiết về một thuật toán
    """
    result = image_controller.get_algorithm_info(algorithm)
    
    if result.get('status') == 'error':
        error_code = 404 if 'not found' in result.get('error', '').lower() else 500
        return jsonify(result), error_code
    
    return jsonify(result)


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Image processing service is running'
    })


@app.errorhandler(404)
def not_found(error):
    """
    Handler cho 404 errors
    """
    return jsonify({
        'error': 'Endpoint không tìm thấy',
        'status': 'error'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handler cho 500 errors
    """
    return jsonify({
        'error': 'Lỗi server nội bộ',
        'status': 'error'
    }), 500


if __name__ == '__main__':
    print("Starting Image Processing API...")
    print("Available endpoints:")
    print("  GET  / - Get supported algorithms")
    print("  POST /process - Process image")
    print("  GET  /algorithms/<name> - Get algorithm info")
    print("  GET  /health - Health check")
    
    app.run(port=5000, debug=True)
