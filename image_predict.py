import os
import pickle
import numpy as np
from PIL import Image as PILImage
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scipy.spatial.distance import cosine

# File to store features and labels
FEATURES_FILE = os.path.join(settings.BASE_DIR, "features.pkl")

# Pretrained feature extractor (ResNet50)
feature_extractor = ResNet50(weights="imagenet", include_top=False, pooling="avg")


def extract_features(img):
    """
    Extract features from an image using a pretrained ResNet50 model.
    Ensure the image is converted to RGB if it's in grayscale.
    """
    # Ensure image is in RGB format
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize to match model input size
    img = img.resize((224, 224))

    # Convert to array and preprocess
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Preprocess for ResNet
    features = feature_extractor.predict(img_array)  # Extract features
    return features[0]  # Flatten to 1D array



# **Save Features and Labels**
def save_features_and_label(img, label):
    """
    Save extracted features and labels to a file.
    """
    # Extract features
    features = extract_features(img)

    # Load existing features
    if os.path.exists(FEATURES_FILE):
        with open(FEATURES_FILE, "rb") as f:
            data = pickle.load(f)
    else:
        data = []

    # Append new feature and label
    data.append({"features": features, "label": label})

    # Save back to file
    with open(FEATURES_FILE, "wb") as f:
        pickle.dump(data, f)

    return {"message": "Features and label saved successfully"}


# **Predict Label**
def predict_label(img):
    """
    Predict the label of an image based on stored features.
    """
    # Extract features of the input image
    query_features = extract_features(img)

    # Load stored features
    if not os.path.exists(FEATURES_FILE):
        return {"error": "No features stored. Train the model first."}

    with open(FEATURES_FILE, "rb") as f:
        data = pickle.load(f)

    # Find the closest match
    min_distance = float("inf")
    predicted_label = None

    for item in data:
        distance = cosine(query_features, item["features"])
        if distance < min_distance:
            min_distance = distance
            predicted_label = item["label"]

    return {"predicted_label": predicted_label, "confidence": 1 - min_distance}


# **Train API**
@csrf_exempt
def train_model(request):
    """
    API to train the system by adding images and their corresponding labels.
    """
    if request.method == "POST":
        if "image" not in request.FILES or "label" not in request.POST:
            return JsonResponse({"error": "Image and label are required."}, status=400)

        label = request.POST["label"]
        img_files = request.FILES.getlist("image")

        for img_file in img_files:
            img = PILImage.open(img_file)
            save_features_and_label(img, label)

        return JsonResponse({"message": "Images added successfully for training."})


# **Predict API**
@csrf_exempt
def predict_model(request):
    """
    API to predict the label of an uploaded image.
    """
    if request.method == "POST":
        if "image" not in request.FILES:
            return JsonResponse({"error": "Image is required."}, status=400)

        img_file = request.FILES["image"]
        img = PILImage.open(img_file)
        result = predict_label(img)

        return JsonResponse(result)

def predict_model_from_image(img_file):
    """
    Function to predict the label of a given image file.
    """
    try:
        img = PILImage.open(img_file)
        result = predict_label(img)
        return result
    except Exception as e:
        print(f"Error in predicting label: {e}")
        return {"error": "Prediction failed."}