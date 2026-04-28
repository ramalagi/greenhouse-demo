from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import random
import time
# import tensorflow as tf  # Uncomment when TensorFlow is installed
# from PIL import Image  # Uncomment when Pillow is installed
# import numpy as np  # Uncomment when needed

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

@app.context_processor
def inject_user():
    return {'logged_in': 'logged_in' in session}

# Load the model (uncomment when model is available)
# model = tf.keras.models.load_model('model/plant_model.h5')

# Disease information
DISEASES = {
    0: {
        'name': 'Healthy Plant',
        'symptoms': 'No visible symptoms',
        'prevention': 'Continue regular care'
    },
    1: {
        'name': 'Leaf Spot',
        'symptoms': 'Dark spots on leaves, yellowing',
        'prevention': 'Remove affected leaves, improve air circulation, avoid overhead watering'
    },
    2: {
        'name': 'Powdery Mildew',
        'symptoms': 'White powdery coating on leaves',
        'prevention': 'Increase air circulation, reduce humidity, apply fungicide if necessary'
    },
    3: {
        'name': 'Rust Disease',
        'symptoms': 'Orange or reddish-brown pustules on leaves',
        'prevention': 'Remove infected plants, apply fungicide, improve drainage'
    },
    4: {
        'name': 'Bacterial Blight',
        'symptoms': 'Water-soaked lesions, wilting',
        'prevention': 'Use disease-resistant varieties, avoid wet conditions, apply copper-based fungicide'
    }
}

# Translations
TRANSLATIONS = {
    'en': {
        'title': 'AI Smart Greenhouse System',
        'upload_image': 'Upload Image',
        'detect_disease': 'Detect Disease',
        'plant_healthy': 'Plant is Healthy',
        'disease_name': 'Disease Name',
        'symptoms': 'Symptoms',
        'prevention': 'Prevention Methods',
        'soil_moisture': 'Soil Moisture',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'login': 'Login',
        'logout': 'Logout',
        'home': 'Home',
        'detect_plant': 'Detect Plant',
        'dashboard': 'Dashboard',
        'admin_login': 'Admin Login',
        'features': 'Features',
        'plant_disease_detection': 'Plant Disease Detection',
        'soil_monitoring': 'Soil Monitoring',
        'live_dashboard': 'Live Dashboard',
        'ai_analysis': 'AI Analysis',
        'admin_dashboard': 'Admin Dashboard',
        'plant_detection_logs': 'Plant Detection Logs',
        'hero_description': 'Revolutionizing agriculture with AI-powered plant disease detection and smart monitoring',
        'feature_plant_desc': 'Upload plant images and get instant AI-powered disease diagnosis',
        'feature_soil_desc': 'Real-time monitoring of soil moisture, temperature, and humidity',
        'feature_dashboard_desc': 'Interactive dashboard with live data visualization',
        'feature_ai_desc': 'Advanced AI algorithms for accurate plant health assessment',
        'detect_another_plant': 'Detect Another Plant',
        'copyright': '© 2024 AI Smart Greenhouse System. All rights reserved.',
        'timestamp': 'Timestamp',
        'disease_detected': 'Disease Detected',
        'image': 'Image'
    },
    'hi': {
        'title': 'एआई स्मार्ट ग्रीनहाउस सिस्टम',
        'upload_image': 'छवि अपलोड करें',
        'detect_disease': 'रोग का पता लगाएं',
        'plant_healthy': 'प्लांट स्वस्थ है',
        'disease_name': 'रोग का नाम',
        'symptoms': 'लक्षण',
        'prevention': 'रोकथाम विधियां',
        'soil_moisture': 'मिट्टी की नमी',
        'temperature': 'तापमान',
        'humidity': 'नमी',
        'login': 'लॉगिन',
        'logout': 'लॉगआउट',
        'home': 'होम',
        'detect_plant': 'प्लांट का पता लगाएं',
        'dashboard': 'डैशबोर्ड',
        'admin_login': 'एडमिन लॉगिन',
        'features': 'विशेषताएं',
        'plant_disease_detection': 'प्लांट रोग का पता लगाना',
        'soil_monitoring': 'मिट्टी की निगरानी',
        'live_dashboard': 'लाइव डैशबोर्ड',
        'ai_analysis': 'एआई विश्लेषण',
        'admin_dashboard': 'एडमिन डैशबोर्ड',
        'plant_detection_logs': 'प्लांट पता लगाने के लॉग',
        'hero_description': 'एआई-सक्षम पौधे रोग पहचान और स्मार्ट निगरानी के साथ कृषि में क्रांति',
        'feature_plant_desc': 'पौधे की तस्वीरें अपलोड करें और त्वरित एआई रोग निदान प्राप्त करें',
        'feature_soil_desc': 'मिट्टी की नमी, तापमान और आर्द्रता की वास्तविक समय निगरानी',
        'feature_dashboard_desc': 'लाइव डेटा विज़ुअलाइज़ेशन के साथ इंटरैक्टिव डैशबोर्ड',
        'feature_ai_desc': 'सटीक पौधे स्वास्थ्य मूल्यांकन के लिए उन्नत एआई एल्गोरिदम',
        'detect_another_plant': 'एक और पौधा पहचानें',
        'copyright': '© 2024 एआई स्मार्ट ग्रीनहाउस सिस्टम। सर्वाधिकार सुरक्षित।',
        'timestamp': 'समय चिह्न',
        'disease_detected': 'पता लगा रोग',
        'image': 'छवि'
    },
    'kn': {
        'title': 'ಎಐ ಸ್ಮಾರ್ಟ್ ಗ್ರೀನ್‌ಹೌಸ್ ಸಿಸ್ಟಮ್',
        'upload_image': 'ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'detect_disease': 'ರೋಗವನ್ನು ಪತ್ತೆ ಮಾಡಿ',
        'plant_healthy': 'ಸಸ್ಯ ಆರೋಗ್ಯವಾಗಿದೆ',
        'disease_name': 'ರೋಗದ ಹೆಸರು',
        'symptoms': 'ಲಕ್ಷಣಗಳು',
        'prevention': 'ತಡೆಗಟ್ಟುವ ವಿಧಾನಗಳು',
        'soil_moisture': 'ಮಣ್ಣಿನ ತೇವಾಂಶ',
        'temperature': 'ತಾಪಮಾನ',
        'humidity': 'ಆರ್ದ್ರತೆ',
        'login': 'ಲಾಗಿನ್',
        'logout': 'ಲಾಗೌಟ್',
        'home': 'ಮುಖ್ಯ ಪುಟ',
        'detect_plant': 'ಸಸ್ಯವನ್ನು ಪತ್ತೆ ಮಾಡಿ',
        'dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'admin_login': 'ಆಡ್ಮಿನ್ ಲಾಗಿನ್',
        'features': 'ವೈಶಿಷ್ಟ್ಯಗಳು',
        'plant_disease_detection': 'ಸಸ್ಯ ರೋಗ ಪತ್ತೆ',
        'soil_monitoring': 'ಮಣ್ಣಿನ ಮೇಲ್ವಿಚಾರಣೆ',
        'live_dashboard': 'ಲೈವ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'ai_analysis': 'ಎಐ ವಿಶ್ಲೇಷಣೆ',
        'admin_dashboard': 'ಆಡ್ಮಿನ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'plant_detection_logs': 'ಸಸ್ಯ ಪತ್ತೆ ಲಾಗ್‌ಗಳು',
        'hero_description': 'ಎಐ ಚಾಲಿತ ಸಸ್ಯ ರೋಗ ಪತ್ತೆ ಮತ್ತು ತಂತ್ರಜ್ಞಾನಾತ್ಮಕ ತದ್ರುಪದ ನಿರೀಕ್ಷಣೆಯೊಂದಿಗೆ ಕೃಷಿಯಲ್ಲಿ ಕ್ರಾಂತಿ',
        'feature_plant_desc': 'ಸಸ್ಯ ಚಿತ್ರಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ತಕ್ಷಣದ ಎಐ ರೋಗ ನಿರ್ಣಯವನ್ನು ಪಡೆಯಿರಿ',
        'feature_soil_desc': 'ಮಣ್ಣಿನ ತೇವಾಂಶ, ತಾಪಮಾನ ಮತ್ತು ಆರ್ದ್ರತೆಯ ವಾಸ್ತವಿಕ-ಸಮಯ ಮೇಲ್ವೀಕ್ಷಣೆ',
        'feature_dashboard_desc': 'ಲೈವ್ ಡೇಟಾ ದೃಶ್ಯೀಕರಣದೊಂದಿಗೆ ಸಂವಹನಾತ್ಮಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'feature_ai_desc': 'ಸಸ್ಯ ಆರೋಗ್ಯದ ಶುದ್ಧತೆಯ ಮೌಲ್ಯಮಾಪನಕ್ಕಾಗಿ ಉನ್ನತ ಎಐ ಅಲ್ಗಾರಿದಮ್‌ಗಳು',
        'detect_another_plant': 'ಮತ್ತೊಂದು ಸಸ್ಯ ಪತ್ತೆ ಮಾಡಿ',
        'copyright': '© 2024 ಎಐ ಸ್ಮಾರ್ಟ್ ಗ್ರೀನ್‌ಹೌಸ್ ಸಿಸ್ಟಮ್. ಎಲ್ಲಾ ಹಕ್ಕುಗಳೂ ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
        'timestamp': 'ಟೈಮ್‌ಸ್ಟ್ಯಾಂಪ್',
        'disease_detected': 'ರೋಗ ಪತ್ತೆಯಾಗಿದೆ',
        'image': 'ಚಿತ್ರ'
    }
}

# Global variables for logs and soil data
detection_logs = []
soil_data = {'moisture': 50, 'temperature': 25, 'humidity': 60}

def get_language():
    return session.get('language', 'en')

def translate(key):
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def generate_soil_data():
    global soil_data
    soil_data['moisture'] = random.randint(30, 80)
    soil_data['temperature'] = random.randint(20, 35)
    soil_data['humidity'] = random.randint(40, 90)

def preprocess_image(image_path):
    # Uncomment when PIL and TensorFlow are installed
    # img = Image.open(image_path)
    # img = img.resize((224, 224))  # Assuming model expects 224x224
    # img_array = np.array(img) / 255.0
    # img_array = np.expand_dims(img_array, axis=0)
    # return img_array
    return None

def predict_disease(image_path):
    # Uncomment when model is loaded
    # img_array = preprocess_image(image_path)
    # predictions = model.predict(img_array)
    # class_index = np.argmax(predictions[0])
    # return class_index

    # For demo purposes, return a random class
    return random.randint(0, 4)

@app.before_request
def require_login():
    # Allow public access to login, language selection, API, and static files
    public_endpoints = ['login', 'set_language', 'api_soil', 'static']
    if request.endpoint in public_endpoints:
        return
    if 'logged_in' not in session:
        return redirect(url_for('login'))

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save the uploaded file
            filename = 'uploaded_' + str(int(time.time())) + '.jpg'
            filepath = os.path.join('static', 'uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            # Predict disease
            prediction = predict_disease(filepath)
            disease_info = DISEASES[prediction]

            # Log the detection
            detection_logs.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'disease': disease_info['name'],
                'image': filename
            })

            return render_template('result.html', disease_info=disease_info, image=filename, translate=translate)
    return render_template('predict.html', translate=translate)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password', translate=translate)
    return render_template('login.html', translate=translate)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    generate_soil_data()
    return render_template('dashboard.html', soil_data=soil_data, logs=detection_logs[-10:], translate=translate)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/api/soil')
def api_soil():
    generate_soil_data()
    return jsonify(soil_data)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in TRANSLATIONS:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)