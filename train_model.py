import os
import cv2
import json
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "indian cricketer"
)

MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "cricket_face_model.pkl"
)

LABEL_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

REPORT_PATH = os.path.join(
    MODEL_DIR,
    "training_report.json"
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = (64, 64)

MIN_IMAGES_PER_PLAYER = 10

TEST_SIZE = 0.20

RANDOM_STATE = 42


# ============================================================
# FACE DETECTOR
# ============================================================

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(CASCADE_PATH)

if face_detector.empty():
    raise RuntimeError("Failed to load OpenCV Haar Cascade face detector.")


# ============================================================
# HOG DESCRIPTOR
# ============================================================

hog = cv2.HOGDescriptor(
    (32, 32),
    (16, 16),
    (8, 8),
    (8, 8),
    9
)


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# FUNCTIONS
# ============================================================

def detect_largest_face(image):
    """
    Detect faces and return the largest detected face.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

    # Add a small margin around face
    margin_x = int(w * 0.15)
    margin_y = int(h * 0.15)

    x1 = max(0, x - margin_x)
    y1 = max(0, y - margin_y)

    x2 = min(image.shape[1], x + w + margin_x)
    y2 = min(image.shape[0], y + h + margin_y)

    face = image[y1:y2, x1:x2]

    return face


def extract_hog_features(face):
    """
    Resize face and extract HOG features.
    """

    face = cv2.resize(face, IMAGE_SIZE)

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    features = hog.compute(gray)

    return features.flatten()


def load_dataset():
    """
    Load images from every player folder.
    """

    features = []
    labels = []

    processed_images = 0
    skipped_images = 0

    player_folders = []

    if not os.path.exists(DATASET_DIR):
        raise FileNotFoundError(
            f"Dataset folder not found: {DATASET_DIR}"
        )

    for name in sorted(os.listdir(DATASET_DIR)):

        player_path = os.path.join(DATASET_DIR, name)

        if os.path.isdir(player_path):
            player_folders.append(name)

    print("=" * 65)
    print("Indian Cricket Face Identification")
    print("=" * 65)

    print(f"\nDataset location:")
    print(DATASET_DIR)

    print(f"\nTotal player folders found: {len(player_folders)}")
    print("\nProcessing images...\n")

    valid_extensions = (
        ".jpg",
        ".jpeg",
        ".png"
    )

    for player_index, player_name in enumerate(player_folders, start=1):

        player_path = os.path.join(
            DATASET_DIR,
            player_name
        )

        image_files = [
            file_name
            for file_name in os.listdir(player_path)
            if file_name.lower().endswith(valid_extensions)
        ]

        if len(image_files) < MIN_IMAGES_PER_PLAYER:
            print(
                f"[SKIP PLAYER] {player_name}: "
                f"only {len(image_files)} images"
            )
            continue

        player_processed = 0

        for image_name in image_files:

            image_path = os.path.join(
                player_path,
                image_name
            )

            try:

                image = cv2.imread(image_path)

                if image is None:
                    skipped_images += 1
                    continue

                face = detect_largest_face(image)

                if face is None:
                    skipped_images += 1
                    continue

                hog_features = extract_hog_features(face)

                features.append(hog_features)
                labels.append(player_name)

                processed_images += 1
                player_processed += 1

            except Exception as error:
                skipped_images += 1
                print(f"[ERROR] {player_name}/{image_name}: {error}")

        print(
            f"[{player_index}/{len(player_folders)}] "
            f"{player_name}: {player_processed} images"
        )

    print("\n" + "=" * 65)
    print("Dataset Processing Completed")
    print("=" * 65)

    print(f"Images successfully processed: {processed_images}")
    print(f"Images skipped: {skipped_images}")
    print(f"Training classes: {len(set(labels))}")

    print("=" * 65)

    return np.array(features), np.array(labels)


# ============================================================
# LOAD DATA
# ============================================================

X, y = load_dataset()


if len(X) == 0:
    raise RuntimeError(
        "No training images were successfully processed."
    )


# ============================================================
# LABEL ENCODING
# ============================================================

label_encoder = LabelEncoder()

encoded_labels = label_encoder.fit_transform(y)

number_of_classes = len(label_encoder.classes_)


print("\n")
print("=" * 65)
print("Preparing Machine Learning Model")
print("=" * 65)

print(f"\nNumber of classes: {number_of_classes}")


# ============================================================
# TRAIN / VALIDATION SPLIT
# ============================================================

X_train, X_val, y_train, y_val = train_test_split(
    X,
    encoded_labels,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=encoded_labels
)


print(f"\nTraining samples: {len(X_train)}")
print(f"Validation samples: {len(X_val)}")


# ============================================================
# SVM CLASSIFIER
# ============================================================
#
# IMPORTANT:
# probability=False makes training much faster.
#
# We calculate a confidence score later from the SVM
# decision function instead of probability calibration.
# ============================================================

print("\nTraining SVM classifier...")

classifier = LinearSVC(
    C=1.0,
    class_weight="balanced",
    max_iter=10000,
    random_state=RANDOM_STATE
)

classifier.fit(
    X_train,
    y_train
)


print("\nSVM training completed successfully!")


# ============================================================
# VALIDATION
# ============================================================

print("\nEvaluating model...")

y_pred = classifier.predict(X_val)

accuracy = accuracy_score(
    y_val,
    y_pred
)

print(
    f"\nValidation Accuracy: "
    f"{accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y_val,
    y_pred,
    target_names=label_encoder.classes_,
    output_dict=True,
    zero_division=0
)


# ============================================================
# SAVE MODEL
# ============================================================

with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        classifier,
        file
    )


# ============================================================
# SAVE LABEL ENCODER
# ============================================================

with open(
    LABEL_ENCODER_PATH,
    "wb"
) as file:

    pickle.dump(
        label_encoder,
        file
    )


# ============================================================
# TRAINING REPORT
# ============================================================

training_report = {

    "project": "Indian Cricket Team Member Face Identification",

    "dataset_directory": DATASET_DIR,

    "number_of_classes": int(number_of_classes),

    "processed_images": int(len(X)),

    "training_samples": int(len(X_train)),

    "validation_samples": int(len(X_val)),

    "validation_accuracy": float(accuracy),

    "validation_accuracy_percentage":
        float(accuracy * 100),

    "model": {
        "algorithm": "Support Vector Machine",
        "kernel": "linear",
        "C": 1.0,
        "max_iter": 10000,  
        "class_weight": "balanced",
        "probability_calibration": False
    },

    "feature_extraction": {
        "method": "HOG",
        "image_size": [
            IMAGE_SIZE[0],
            IMAGE_SIZE[1]
        ]
    },

    "face_detection": {
        "method": "OpenCV Haar Cascade"
    },

    "random_state": RANDOM_STATE,

    "classification_report": report
}


with open(
    REPORT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        training_report,
        file,
        indent=4
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n")
print("=" * 65)
print("MODEL TRAINING COMPLETED")
print("=" * 65)

print(
    f"\nValidation Accuracy: "
    f"{accuracy * 100:.2f}%"
)

print("\nModel saved:")
print(MODEL_PATH)

print("\nLabel encoder saved:")
print(LABEL_ENCODER_PATH)

print("\nTraining report saved:")
print(REPORT_PATH)

print("\n" + "=" * 65)