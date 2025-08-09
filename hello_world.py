from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello_world():
    """Return a simple hello world message."""
    try:
        app.logger.info('Hello world endpoint accessed')
        return jsonify({
            'message': 'Hello, World!',
            'status': 'success',
            'system': 'Automotas AI Cognitive System',
            'timestamp': '2025-07-26T13:30:00Z'
        })
    except Exception as e:
        app.logger.error(f'Error in hello_world endpoint: {e}')
        return jsonify({
            'message': 'Internal server error',
            'status': 'error'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'system': 'Automotas AI'})

if __name__ == '__main__':
    print('🚀 Starting Automotas AI Hello World Application')
    print('📍 Available endpoints:')
    print('   • http://localhost:5000/ - Hello World')
    print('   • http://localhost:5000/health - Health Check')
    app.run(debug=True, host='0.0.0.0', port=5000)

