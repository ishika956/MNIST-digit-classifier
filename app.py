from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import base64
import re
import io
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model("mnist_model.h5")

def preprocess_image(image_data):
    image_str = re.search(r'base64,(.*)', image_data).group(1)
    image_bytes = base64.b64decode(image_str)
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = image.resize((28, 28))
    image_array = np.array(image)
    image_array = 255 - image_array  # invert background
    image_array = image_array / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)
    return image_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']
    processed = preprocess_image(image_data)
    prediction = model.predict(processed)
    digit = int(np.argmax(prediction))
    return jsonify({'prediction': digit})

if __name__ == '__main__':
    app.run(debug=True)
