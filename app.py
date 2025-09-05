from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # In a real app, you would process the image here
        # For now, we'll just simulate processing
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'filename': filename,
            'analysis_id': str(uuid.uuid4())
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/analyze/<analysis_id>', methods=['POST'])
def analyze_image(analysis_id):
    # Simulate AI analysis
    # In a real app, this would call your ML model
    
    # Simulate processing time
    import time
    time.sleep(2)
    
    # Return mock analysis results
    return jsonify({
        'success': True,
        'analysis_id': analysis_id,
        'results': {
            'body_type': 'hourglass',
            'color_palette': ['warm', 'autumn'],
            'recommended_styles': ['casual', 'bohemian', 'business casual'],
            'size_recommendation': 'M'
        }
    })

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    
    # In a real app, this would query a database or external API
    # Return mock recommendations based on analysis results
    recommendations = [
        {
            'id': 1,
            'title': 'Casual Summer Outfit',
            'description': 'Lightweight linen shirt with tailored shorts',
            'price': 89.99,
            'image_url': '/static/images/outfit1.jpg',
            'brand': 'Summer Essentials'
        },
        {
            'id': 2,
            'title': 'Evening Elegance',
            'description': 'Flowy maxi dress with subtle patterns',
            'price': 129.99,
            'image_url': '/static/images/outfit2.jpg',
            'brand': 'Elegant Nights'
        },
        {
            'id': 3,
            'title': 'Business Casual',
            'description': 'Structured blazer with comfortable trousers',
            'price': 159.99,
            'image_url': '/static/images/outfit3.jpg',
            'brand': 'Professional Wear'
        }
    ]
    
    return jsonify({
        'success': True,
        'recommendations': recommendations
    })

@app.route('/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    
    # In a real app, this would save to a database
    rule_id = str(uuid.uuid4())
    
    return jsonify({
        'success': True,
        'rule_id': rule_id,
        'message': 'Fashion rule created successfully'
    })

@app.route('/rules/<user_id>', methods=['GET'])
def get_rules(user_id):
    # In a real app, this would fetch from a database
    # Return mock rules
    rules = [
        {
            'id': 1,
            'name': 'Always suggest warm colors',
            'description': 'Prioritize warm tones like reds, oranges, and yellows',
            'category': 'color_preferences',
            'active': True
        },
        {
            'id': 2,
            'name': 'Avoid tight-fitting clothes',
            'description': 'Focus on loose, comfortable fits',
            'category': 'fit_style',
            'active': False
        }
    ]
    
    return jsonify({
        'success': True,
        'rules': rules
    })

if __name__ == '__main__':
    app.run(debug=True)