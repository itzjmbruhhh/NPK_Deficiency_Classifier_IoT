from keras.models import load_model
from keras.applications.resnet import preprocess_input
from PIL import Image, UnidentifiedImageError
import numpy as np
from io import BytesIO
from django.core.cache import cache

# Load the model at startup
MODEL_PATH = "model/saved_model.h5"
model = load_model(MODEL_PATH)

# Define class labels (Modify based on your model's classes)
CLASS_LABELS = ["Healthy", "Nitrogen Deficient", "Phosphorus Deficient", "Potassium Deficient"]

def is_probably_a_leaf(image: np.ndarray) -> bool:
    """
    A simple heuristic to check if the image is predominantly green, 
    which could indicate that it is a leaf.
    """
    # Calculate the percentage of green pixels in the image
    # A pixel is considered "green" if the green channel is dominant compared to red and blue
    green_pixels = np.sum((image[:, :, 1] > image[:, :, 0]) & (image[:, :, 1] > image[:, :, 2]))
    total_pixels = image.shape[0] * image.shape[1]
    green_ratio = green_pixels / total_pixels
    
    # If more than 10% of the image is green, we assume it's likely a leaf
    return green_ratio > 0.1

def read_file_as_image(data) -> np.ndarray:
    try:
        image = Image.open(BytesIO(data))  # Open the image file from the data stream
        if image.mode != 'RGB':  # Ensure the image is in RGB format
            image = image.convert('RGB')
        image_np = np.array(image)  # Convert image to numpy array
        
        # Optional: Basic heuristic to check if it's probably a leaf (can be customized)
        if not is_probably_a_leaf(image_np):
            raise ValueError("The image doesn't seem to be a leaf.")
        
        return image_np
    except UnidentifiedImageError:
        raise ValueError("Invalid image file.")
    except Exception as e:
        raise ValueError(f"An error occurred while processing the image: {str(e)}")

def preprocess_image(uploaded_file):
    # Open the uploaded image file directly without using `.read()`
    image = Image.open(uploaded_file)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    img = image.resize((299, 299))  # Resize to model input size
    img_array = np.array(img)

    if img_array.shape[-1] != 3:
        img_array = np.stack([img_array] * 3, axis=-1)

    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array

# Prediction function
def predict_image(img_array):
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)
    return CLASS_LABELS[predicted_class], confidence