from flask import Flask, request, jsonify # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np # type: ignore
import os
from PIL import Image  # type: ignore # Import PIL
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

# Load the model
model = load_model('plant_disease_prediction_model.h5')

# Load the plant/non-plant classifier model
leaf_classifier = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)

class_to_disease = {
    0: "Apple : Apple_scab",
    1: "Apple : Black_rot",
    2: "Apple : Cedar_apple_rust",
    3: "Apple : healthy",
    4: "Blueberry : healthy",
    5: "Cherry_(including_sour) : Powdery_mildew",
    6: "Cherry_(including_sour) : healthy",
    7: "Corn_(maize) : Cercospora_leaf_spot Gray_leaf_spot",
    8: "Corn_(maize) : Common_rust_",
    9: "Corn_(maize) : Northern_Leaf_Blight",
    10: "Corn_(maize) : healthy",
    11: "Grape : Black_rot",
    12: "Grape : Esca_(Black_Measles)",
    13: "Grape : Leaf_blight_(Isariopsis_Leaf_Spot)",
    14: "Grape : healthy",
    15: "Orange : Haunglongbing_(Citrus_greening)",
    16: "Peach : Bacterial_spot",
    17: "Peach : healthy",
    18: "Pepper bell : Bacterial_spot",
    19: "Pepper,_bell : healthy",
    20: "Potato :Early_blight",
    21: "Potato : Late_blight",
    22: "Potato : healthy",
    23: "Raspberry : healthy",
    24: "Soybean : healthy",
    25: "Squash : Powdery_mildew",
    26: "Strawberry : Leaf_scorch",
    27: "Strawberry : healthy",
    28: "Tomato : Bacterial_spot",
    29: "Tomato : Early_blight",
    30: "Tomato : Late_blight",
    31: "Tomato : Leaf_Mold",
    32: "Tomato : Septoria_leaf_spot",
    33: "Tomato : Spider_mites Two-spotted_spider_mite",
    34: "Tomato : Target_Spot",
    35: "Tomato : Tomato_Yellow_Leaf_Curl_Virus",
    36: "Tomato : Tomato_mosaic_virus",
    37: "Tomato : healthy"
}

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('uint32') 
    return img_array

def is_leaf(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    predictions = leaf_classifier.predict(img_array) 
    
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        print(f"{i+1}: {label} ({score:.2f})")
    for _, label,score in decoded_predictions:
        if 'leaf' in label.lower():
            return True
    return False

# Define a route to handle model inference
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file provided'}), 400

        # Save the file temporarily
        file_path = os.path.join('temp', file.filename)
        os.makedirs('temp', exist_ok=True)
        file.save(file_path)

        # Check if the image is a plant
        result = is_leaf(file_path)
        print(result)
        if is_leaf(file_path):
            os.remove(file_path)
            return jsonify({'error': 'The uploaded image does not appear to be a plant. Please upload a plant image.'}),400
        
        # Preprocess the image
        img_array = preprocess_image(file_path)
        
        # Predict
        prediction = model.predict(img_array)
        predicted_class = class_to_disease[np.argmax(prediction)]
        
        # Clean up temporary file
        os.remove(file_path)

        # Return the result as JSON
        return jsonify({'predicted_class': predicted_class})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
