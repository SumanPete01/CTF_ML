from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/get/<param_type>/<int:index>', methods=['GET'])
def get_parameter(param_type, index):
    if param_type not in ['bias', 'weight', 'activation']:
        return jsonify({'error': 'Invalid type'}), 400
    
    try:
        result = subprocess.run(
            ['./checker.exe', param_type, str(index)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({'result': result.stdout.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

