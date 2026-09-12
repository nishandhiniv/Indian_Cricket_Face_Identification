import os
import cv2
import pickle
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "cricket_face_model.pkl"
)

LABEL_ENCODER_PATH = os.path.join(
    BASE_DIR,
    "model",
    "label_encoder.pkl"
)


# ============================================================
# IMAGE / HOG SETTINGS
# ============================================================

IMAGE_SIZE = (64, 64)

CASCADE_PATH = (
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)

face_detector = cv2.CascadeClassifier(
    CASCADE_PATH
)

hog = cv2.HOGDescriptor(
    (32, 32),
    (16, 16),
    (8, 8),
    (8, 8),
    9
)


# ============================================================
# GLOBAL MODEL VARIABLES
# ============================================================

classifier = None
label_encoder = None
model_loaded = False


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():
    """
    Load trained SVM model and label encoder.
    """

    global classifier
    global label_encoder
    global model_loaded

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not os.path.exists(LABEL_ENCODER_PATH):
        raise FileNotFoundError(
            f"Label encoder not found: {LABEL_ENCODER_PATH}"
        )

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        classifier = pickle.load(file)

    with open(
        LABEL_ENCODER_PATH,
        "rb"
    ) as file:

        label_encoder = pickle.load(file)

    model_loaded = True

    return True


# ============================================================
# FACE DETECTION
# ============================================================

def detect_largest_face(image):
    """
    Detect the largest face in an image.
    """

    if image is None:
        return None

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    if len(faces) == 0:
        return None

    largest_face = max(
        faces,
        key=lambda rect: rect[2] * rect[3]
    )

    x, y, w, h = largest_face

    margin_x = int(w * 0.15)
    margin_y = int(h * 0.15)

    x1 = max(
        0,
        x - margin_x
    )

    y1 = max(
        0,
        y - margin_y
    )

    x2 = min(
        image.shape[1],
        x + w + margin_x
    )

    y2 = min(
        image.shape[0],
        y + h + margin_y
    )

    face = image[
        y1:y2,
        x1:x2
    ]

    return face


# ============================================================
# HOG FEATURE EXTRACTION
# ============================================================

def extract_hog_features(face):
    """
    Extract HOG features from detected face.
    """

    face = cv2.resize(
        face,
        IMAGE_SIZE
    )

    gray = cv2.cvtColor(
        face,
        cv2.COLOR_BGR2GRAY
    )

    features = hog.compute(gray)

    return features.flatten()


# ============================================================
# CONFIDENCE CALCULATION
# ============================================================

def calculate_confidence(decision_scores):
    """
    Convert SVM decision scores into a relative confidence score.

    IMPORTANT:
    This is a confidence estimate, not a calibrated probability.
    """

    scores = np.asarray(
        decision_scores
    ).flatten()

    if len(scores) == 0:
        return 0.0

    # Sort scores from highest to lowest
    sorted_scores = np.sort(scores)[::-1]

    best_score = float(
        sorted_scores[0]
    )

    second_score = (
        float(sorted_scores[1])
        if len(sorted_scores) > 1
        else best_score - 1.0
    )

    margin = best_score - second_score

    # Convert score margin to a bounded confidence estimate.
    confidence = 50.0 + (
        50.0 * np.tanh(margin)
    )

    confidence = max(
        0.0,
        min(99.0, confidence)
    )

    return round(
        confidence,
        2
    )


# ============================================================
# PREDICT PLAYER
# ============================================================

def predict_player(image):
    """
    Predict the cricket player from an OpenCV image.
    """

    global classifier
    global label_encoder

    # --------------------------------------------------------
    # Lazy model loading
    # --------------------------------------------------------

    if not model_loaded:
        load_model()

    if classifier is None:
        raise RuntimeError(
            "Machine learning model is not loaded."
        )

    if label_encoder is None:
        raise RuntimeError(
            "Label encoder is not loaded."
        )

    # --------------------------------------------------------
    # Detect face
    # --------------------------------------------------------

    face = detect_largest_face(
        image
    )

    if face is None:

        return {
            "success": False,
            "player": None,
            "player_name": None,
            "confidence": 0.0,
            "confidence_score": 0.0,
            "message": (
                "No clear face detected. "
                "Please upload a clear front-facing image."
            )
        }

    # --------------------------------------------------------
    # Extract features
    # --------------------------------------------------------

    features = extract_hog_features(
        face
    )

    features = features.reshape(
        1,
        -1
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = classifier.predict(
        features
    )

    predicted_class = int(
        prediction[0]
    )

    player_name = label_encoder.inverse_transform(
        [predicted_class]
    )[0]

    # --------------------------------------------------------
    # Decision function
    # --------------------------------------------------------

    decision_scores = classifier.decision_function(
        features
    )

    confidence = calculate_confidence(
        decision_scores
    )

    # --------------------------------------------------------
    # Confidence message
    # --------------------------------------------------------

    if confidence >= 80:

        message = (
            "High-confidence prediction."
        )

    elif confidence >= 60:

        message = (
            "Moderate-confidence prediction."
        )

    else:

        message = (
            "Low-confidence prediction. "
            "Try a clearer image."
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "success": True,
        "player": player_name,
        "player_name": player_name,
        "confidence": confidence,
        "confidence_score": confidence,
        "message": message
    }


# ============================================================
# PREDICT FROM FILE
# ============================================================

def predict_from_file(image_path):
    """
    Read an image file and predict the player.
    """

    if not os.path.exists(image_path):

        return {
            "success": False,
            "player": None,
            "player_name": None,
            "confidence": 0.0,
            "confidence_score": 0.0,
            "message": "Image file not found."
        }

    image = cv2.imread(
        image_path
    )

    if image is None:

        return {
            "success": False,
            "player": None,
            "player_name": None,
            "confidence": 0.0,
            "confidence_score": 0.0,
            "message": "Unable to read image file."
        }

    return predict_player(
        image
    )


# ============================================================
# MODEL STATUS
# ============================================================

def get_model_status():

    model_exists = os.path.exists(
        MODEL_PATH
    )

    encoder_exists = os.path.exists(
        LABEL_ENCODER_PATH
    )

    return {
        "model_exists": model_exists,
        "label_encoder_exists": encoder_exists,
        "model_loaded": model_loaded,
        "ready": (
            model_exists
            and encoder_exists
        )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Indian Cricket Face Identification")
    print("Model Status")
    print("=" * 60)

    status = get_model_status()

    print(
        f"Model exists: "
        f"{status['model_exists']}"
    )

    print(
        f"Label encoder exists: "
        f"{status['label_encoder_exists']}"
    )

    print(
        f"Model loaded: "
        f"{status['model_loaded']}"
    )

    print(
        f"System ready: "
        f"{status['ready']}"
    )

    if status["ready"]:

        try:

            load_model()

            print(
                "\nModel loaded successfully!"
            )

            print(
                f"Number of classes: "
                f"{len(label_encoder.classes_)}"
            )

        except Exception as error:

            print(
                f"\nModel loading error: {error}"
            )

    print("=" * 60)