/* =========================================================
   INDIAN CRICKET FACE IDENTIFICATION
   Frontend JavaScript
   ========================================================= */


/* ================= ELEMENTS ================= */

const uploadArea = document.getElementById("upload-area");
const imageInput = document.getElementById("image-input");

const previewContainer = document.getElementById("preview-container");
const imagePreview = document.getElementById("image-preview");
const removeImageButton = document.getElementById("remove-image");

const identifyButton = document.getElementById("identify-button");

const resultPlaceholder = document.getElementById("result-placeholder");
const resultLoading = document.getElementById("result-loading");
const predictionResult = document.getElementById("prediction-result");

const playerName = document.getElementById("player-name");
const confidenceValue = document.getElementById("confidence-value");
const confidenceProgress = document.getElementById("confidence-progress");
const predictionMessage = document.getElementById("prediction-message");

const resultStatus = document.querySelector(".result-status");


/* ================= VARIABLES ================= */

let selectedFile = null;


/* ================= INITIAL STATE ================= */

function resetResult() {

    resultPlaceholder.hidden = false;
    resultLoading.hidden = true;
    predictionResult.hidden = true;

    resultStatus.textContent = "Ready";

    playerName.textContent = "Player Name";

    confidenceValue.textContent = "0%";

    confidenceProgress.style.width = "0%";

    predictionMessage.textContent =
        "Player identified successfully.";

}


/* ================= FILE VALIDATION ================= */

function isValidImage(file) {

    if (!file) {
        return false;
    }

    return file.type.startsWith("image/");

}


/* ================= FILE SIZE VALIDATION ================= */

function isFileSizeValid(file) {

    if (!file) {
        return false;
    }

    const maxSize = 10 * 1024 * 1024;

    return file.size <= maxSize;

}


/* ================= SELECT IMAGE ================= */

function handleFile(file) {

    if (!file) {
        return;
    }

    if (!isValidImage(file)) {

        alert(
            "Please select a valid image file.\n\n" +
            "Supported formats: JPG, JPEG, PNG"
        );

        return;

    }

    if (!isFileSizeValid(file)) {

        alert(
            "Image size is too large.\n\n" +
            "Maximum allowed size is 10 MB."
        );

        return;

    }

    selectedFile = file;

    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;

    previewContainer.hidden = false;

    uploadArea.style.display = "none";

    identifyButton.disabled = false;

    resetResult();

}


/* ================= FILE INPUT ================= */

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    handleFile(file);

});


/* ================= DRAG & DROP ================= */

uploadArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadArea.classList.add("dragover");

});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.classList.remove("dragover");

});


uploadArea.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadArea.classList.remove("dragover");

    const file = event.dataTransfer.files[0];

    handleFile(file);

});


/* ================= CLICK UPLOAD AREA ================= */

uploadArea.addEventListener("click", function (event) {

    if (event.target.closest(".browse-button")) {
        return;
    }

    imageInput.click();

});


/* ================= REMOVE IMAGE ================= */

removeImageButton.addEventListener("click", function () {

    selectedFile = null;

    imagePreview.src = "";

    previewContainer.hidden = true;

    uploadArea.style.display = "flex";

    identifyButton.disabled = true;

    imageInput.value = "";

    resetResult();

});


/* ================= SHOW LOADING ================= */

function showLoading() {

    resultPlaceholder.hidden = true;

    resultLoading.hidden = false;

    predictionResult.hidden = true;

    resultStatus.textContent = "Analyzing";

}


/* ================= SHOW PLAYER DETAILS ================= */

function showPlayerDetails(details) {
    if (!details) {
        return;
    }

    const roleElement = document.getElementById("player-role");
    const stateElement = document.getElementById("player-state");
    const dobElement = document.getElementById("player-dob");
    const ageElement = document.getElementById("player-age");
    const statusElement = document.getElementById("player-status");
    const iplTeamElement = document.getElementById("player-ipl-team");
    const achievementElement = document.getElementById("player-achievement");

    if (roleElement) {
        roleElement.textContent =
            details.role || "Information available soon";
    }

    if (stateElement) {
        stateElement.textContent =
            details.state || "Information available soon";
    }

    if (dobElement) {
        dobElement.textContent =
            details.date_of_birth || "Information available soon";
    }

    if (ageElement) {
        ageElement.textContent =
            details.age || "Information available soon";
    }

    if (statusElement) {
        statusElement.textContent =
            details.career_status || "Information available soon";
    }

    if (iplTeamElement) {
        iplTeamElement.textContent =
            details.ipl_team || "Not Available / No IPL Team";
    }

    if (achievementElement) {
        achievementElement.textContent =
            details.achievements || "Information available soon";
    }
}


/* ================= SHOW RESULT ================= */

function showPrediction(
    player,
    confidence,
    message,
    details
) {

    resultPlaceholder.hidden = true;

    resultLoading.hidden = true;

    predictionResult.hidden = false;

    resultStatus.textContent = "Complete";

    /* Player name */

    playerName.textContent = player;

    /* Confidence */

    let confidenceNumber = Number(confidence);

    if (confidenceNumber <= 1) {
        confidenceNumber = confidenceNumber * 100;
    }

    confidenceNumber = Math.max(
        0,
        Math.min(100, confidenceNumber)
    );

    const roundedConfidence =
        confidenceNumber.toFixed(1);

    confidenceValue.textContent =
        roundedConfidence + "%";

    setTimeout(function () {

        confidenceProgress.style.width =
            confidenceNumber + "%";

    }, 100);

    predictionMessage.textContent =
        message ||
        "Player identified successfully.";

    /* Player details */

    showPlayerDetails(details);

}


/* ================= SHOW ERROR ================= */

function showError(message) {

    resultPlaceholder.hidden = false;

    resultLoading.hidden = true;

    predictionResult.hidden = true;

    resultStatus.textContent = "Error";

    resultPlaceholder.querySelector("h5").textContent =
        "Identification Failed";

    resultPlaceholder.querySelector("p").innerHTML =
        message;

    confidenceProgress.style.width = "0%";

}


/* ================= IDENTIFY PLAYER ================= */

identifyButton.addEventListener("click", async function () {

    if (!selectedFile) {

        alert("Please select an image first.");

        return;

    }

    identifyButton.disabled = true;

    showLoading();

    const formData = new FormData();

    formData.append(
        "image",
        selectedFile
    );

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",
                body: formData
            }
        );

        let result;

        try {

            result = await response.json();

        } catch (jsonError) {

            throw new Error(
                "Invalid response received from server."
            );

        }

        if (!response.ok) {

            throw new Error(
                result.message ||
                "Server could not process the image."
            );

        }

        if (result.success === false) {

            throw new Error(
                result.message ||
                "Player identification failed."
            );

        }

        const predictedPlayer =
            result.player ||
            result.player_name ||
            result.name ||
            "Unknown Player";

        const confidence =
            result.confidence ||
            result.confidence_score ||
            0;

        const message =
            result.message ||
            "Player identified successfully.";

        const details =
            result.details ||
            null;

        showPrediction(
            predictedPlayer,
            confidence,
            message,
            details
        );

    } catch (error) {

        console.error(
            "Prediction Error:",
            error
        );

        showError(
            error.message ||
            "Something went wrong while identifying the player."
        );

    } finally {

        identifyButton.disabled =
            !selectedFile;

    }

});


/* ================= KEYBOARD SUPPORT ================= */

imageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        imageInput.click();

    }

});


/* ================= INITIALIZE ================= */

resetResult();

console.log(
    "Indian Cricket Face Identification frontend loaded successfully."
);