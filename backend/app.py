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
    0: "Apple : Apple scab",
    1: "Apple : Black rot",
    2: "Apple : Cedar apple rust",
    3: "Apple : healthy",
    4: "Blueberry : healthy",
    5: "Cherry_(including_sour) : Powdery mildew",
    6: "Cherry_(including_sour) : healthy",
    7: "Corn_(maize) : Cercospora leaf spot Gray leaf spot",
    8: "Corn_(maize) : Common rust ",
    9: "Corn_(maize) : Northern Leaf Blight",
    10: "Corn_(maize) : healthy",
    11: "Grape : Black rot",
    12: "Grape : Esca (Black Measles)",
    13: "Grape : Leaf blight (Isariopsis Leaf Spot)",
    14: "Grape : healthy",
    15: "Orange : Haunglongbing (Citrus greening)",
    16: "Peach : Bacterial spot",
    17: "Peach : healthy",
    18: "Pepper bell : Bacterial spot",
    19: "Pepper,_bell : healthy",
    20: "Potato :Early blight",
    21: "Potato : Late blight",
    22: "Potato : healthy",
    23: "Raspberry : healthy",
    24: "Soybean : healthy",
    25: "Squash : Powdery mildew",
    26: "Strawberry : Leaf scorch",
    27: "Strawberry : healthy",
    28: "Tomato : Bacterial spot",
    29: "Tomato : Early blight",
    30: "Tomato : Late blight",
    31: "Tomato : Leaf Mold",
    32: "Tomato : Septoria leaf spot",
    33: "Tomato : Spider mites Two-spotted spider mite",
    34: "Tomato : Target Spot",
    35: "Tomato : Tomato Yellow Leaf Curl Virus",
    36: "Tomato : Tomato mosaic virus",
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
        if  is_leaf(file_path):
            os.remove(file_path)
            return jsonify({'error': 'The uploaded image does not appear to be a plant. Please upload a plant image.'}),400
        
        # Preprocess the image
        img_array = preprocess_image(file_path)
        
        # Predict
        prediction = model.predict(img_array)
        predicted_class = class_to_disease[np.argmax(prediction)]
        prediction_accuracy = float(np.max(prediction))
        # Clean up temporary file
        os.remove(file_path)

        # Return the result as JSON
        return jsonify({'predicted_class': predicted_class, 'prediction_accuracy': prediction_accuracy})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
