# =========================================================
# INDIAN CRICKET TEAM MEMBER FACE IDENTIFICATION
# Flask Application
# =========================================================

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

import os
import uuid
import json

from face_recognition import predict_from_file


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

PLAYER_DETAILS_FILE = os.path.join(
    BASE_DIR,
    "player_details.json"
)

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}

MAX_FILE_SIZE = 10 * 1024 * 1024

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# =========================================================
# CREATE UPLOAD FOLDER
# =========================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# LOAD PLAYER DETAILS
# =========================================================

def load_player_details():

    if not os.path.exists(
        PLAYER_DETAILS_FILE
    ):
        print(
            "Warning: player_details.json not found."
        )
        return {}

    try:

        with open(
            PLAYER_DETAILS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            details = json.load(file)

        print(
            f"Loaded {len(details)} player profiles."
        )

        return details

    except Exception as error:

        print(
            "Player details loading error:",
            error
        )

        return {}


PLAYER_DETAILS = load_player_details()


# =========================================================
# ALLOWED FILE CHECK
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "success": True,
        "message":
            "Indian Cricket Face Identification server is running."
    })


# =========================================================
# MODEL STATUS
# =========================================================

@app.route("/model-status")
def model_status():

    try:

        from face_recognition import get_model_status

        status = get_model_status()

        return jsonify({
            "success": True,
            "model": status,
            "player_profiles": len(PLAYER_DETAILS)
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================================================
# PLAYER DETAILS API
# =========================================================

@app.route(
    "/player-details/<path:player_name>",
    methods=["GET"]
)
def player_details(player_name):

    details = PLAYER_DETAILS.get(
        player_name
    )

    if details is None:

        return jsonify({
            "success": False,
            "message":
                "Player details not found."
        }), 404

    return jsonify({
        "success": True,
        "player_name": player_name,
        "details": details
    })


# =========================================================
# PREDICTION ENDPOINT
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # -----------------------------------------------------
    # Check image
    # -----------------------------------------------------

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message":
                "No image was uploaded."
        }), 400

    file = request.files["image"]

    # -----------------------------------------------------
    # Check filename
    # -----------------------------------------------------

    if file.filename == "":

        return jsonify({
            "success": False,
            "message":
                "No image was selected."
        }), 400

    # -----------------------------------------------------
    # Check file extension
    # -----------------------------------------------------

    if not allowed_file(
        file.filename
    ):

        return jsonify({
            "success": False,
            "message":
                "Invalid image format. "
                "Please use JPG, JPEG or PNG."
        }), 400

    # -----------------------------------------------------
    # Create unique filename
    # -----------------------------------------------------

    original_name = secure_filename(
        file.filename
    )

    extension = original_name.rsplit(
        ".",
        1
    )[1].lower()

    unique_filename = (
        str(uuid.uuid4())
        + "."
        + extension
    )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    # -----------------------------------------------------
    # Save image
    # -----------------------------------------------------

    try:

        file.save(
            image_path
        )

    except Exception as error:

        print(
            "Image save error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to save the uploaded image."
        }), 500

    # =====================================================
    # RUN MODEL PREDICTION
    # =====================================================

    try:

        result = predict_from_file(
            image_path
        )

        # -------------------------------------------------
        # Attach player details
        # -------------------------------------------------

        if result.get("success"):

            predicted_player = result.get(
                "player_name"
            ) or result.get(
                "player"
            )

            details = PLAYER_DETAILS.get(
                predicted_player,
                {
                    "role": "Indian Cricketer",
                    "batting_style":
                        "Information available soon",
                    "bowling_style":
                        "Information available soon",
                    "country": "India",
                    "achievement":
                        "Player profile under development",
                    "about":
                        f"{predicted_player} is an Indian cricketer "
                        "included in the identification dataset."
                }
            )

            result["details"] = details

        return jsonify(
            result
        )

    except FileNotFoundError:

        return jsonify({
            "success": False,
            "message":
                "Trained model is not available yet. "
                "Please train the model first."
        }), 503

    except Exception as error:

        print(
            "Prediction error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "An error occurred while "
                "identifying the player."
        }), 500

    finally:

        # -------------------------------------------------
        # Delete temporary uploaded image
        # -------------------------------------------------

        try:

            if os.path.exists(
                image_path
            ):

                os.remove(
                    image_path
                )

        except Exception as error:

            print(
                "Temporary file cleanup error:",
                error
            )


# =========================================================
# FILE TOO LARGE
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "success": False,
        "message":
            "Image is too large. Maximum size is 10 MB."
    }), 413


# =========================================================
# GENERAL SERVER ERROR
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "message":
            "Internal server error."
    }), 500


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 65)

    print(
        "INDIAN CRICKET TEAM MEMBER FACE IDENTIFICATION"
    )

    print(
        "Flask Application"
    )

    print("=" * 65)

    print()

    print(
        f"Loaded player profiles: {len(PLAYER_DETAILS)}"
    )

    print(
        "Server URL:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "Prediction endpoint:"
    )

    print(
        "POST /predict"
    )

    print()

    print("=" * 65)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )