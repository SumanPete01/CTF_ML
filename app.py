from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/get/<param_type>/<int:index>', methods=['GET'])
def get_parameter(param_type, index):
    valid_types = ['bias', 'weight', 'activation']
    if param_type not in valid_types:
        return jsonify({'error': 'Invalid type. Use: bias, weight, or activation'}), 400
    
    try:
        result = subprocess.run(
            ['./checker', param_type, str(index)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({'result': result.stdout.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/step', methods=['POST'])
def step_function():
    try:
        # Get vector from request body
        data = request.get_json()
        if not data or 'vector' not in data:
            return jsonify({'error': 'Please provide vector in request body'}), 400
        
        vector = data['vector']
        
        # Build command: ['./checker', 'step', '8', '12', '13', '14', '15']
        cmd = ['./checker', 'step'] + [str(v) for v in vector]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({'result': result.stdout.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/final', methods=['POST'])
def final_function():
    try:
        # Get vector from request body
        data = request.get_json()
        if not data or 'vector' not in data:
            return jsonify({'error': 'Please provide vector in request body'}), 400
        
        vector = data['vector']
        
        # Build command: ['./checker', 'final', '22', '33', '44', '55']
        cmd = ['./checker', 'final'] + [str(v) for v in vector]
        
        result = subprocess.run(
            cmd,
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
