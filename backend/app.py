import os
# Force TensorFlow to use Keras 3 to match the saved model format
os.environ["TF_USE_LEGACY_KERAS"] = "0"

import cv2
import numpy as np
import joblib
from skimage.feature import graycomatrix, graycoprops, hog, local_binary_pattern
from flask import Flask, request, jsonify
from flask_cors import CORS
# Use standalone Keras 3 to check versions and load model
import tensorflow as tf

app = Flask(__name__)
CORS(app)

# --- Configuration ---
IMG_SIZE = (128, 128)
HOG_PIXELS_PER_CELL = (16, 16)
HOG_CELLS_PER_BLOCK = (2, 2)
HSV_BINS = [8, 8, 8]

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Model is now TFLite for memory efficiency
MODEL_PATH = os.path.join(BASE_DIR, "best_mushroom_cnn.tflite")
SCALER_PATH = os.path.join(BASE_DIR, "mushroom_scaler_2.joblib")
LE_PATH = os.path.join(BASE_DIR, "mushroom_le_2.joblib")

# --- Load Artifacts ---
print("Loading artifacts...")
print(f"TensorFlow Version: {tf.__version__}")

load_error = None
interpreter = None
input_details = None
output_details = None
scaler = None
le = None

try:
    # Load TFLite Model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"TFLite model not found at {MODEL_PATH}")

    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print("TFLite Model loaded success.")
    print(f"Input Shape: {input_details[0]['shape']}")

    scaler = joblib.load(SCALER_PATH)
    le = joblib.load(LE_PATH)
    
except Exception as e:
    print(f"Error loading artifacts: {e}")
    load_error = str(e)

# --- Feature Extraction Logic (Must Match Notebook) ---
def extract_features(image):
    """Extract manual features from mushroom image"""
    try:
        if image is None:
            return None

        # Ensure image is resized if not already
        if image.shape[:2] != IMG_SIZE:
             image = cv2.resize(image, IMG_SIZE)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Color features: HSV histogram
        hist_hsv = cv2.calcHist([hsv], [0, 1, 2], None, HSV_BINS, [0, 180, 0, 256, 0, 256])
        cv2.normalize(hist_hsv, hist_hsv)
        features_hsv = hist_hsv.flatten()

        # Texture features: GLCM
        glcm = graycomatrix(gray, distances=[5], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                            levels=256, symmetric=True, normed=True)
        props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
        features_glcm = [np.mean(graycoprops(glcm, p)) for p in props]

        # Shape features: Hu moments
        moments = cv2.moments(gray)
        features_hu = cv2.HuMoments(moments).flatten()

        # Local shape: HOG
        features_hog = hog(gray, orientations=9, pixels_per_cell=HOG_PIXELS_PER_CELL,
                           cells_per_block=HOG_CELLS_PER_BLOCK, visualize=False,
                           block_norm='L2-Hys', feature_vector=True)

        # Texture features: LBP
        radius = 1
        n_points = 8 * radius
        lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
        (hist_lbp, _) = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
        hist_lbp = hist_lbp.astype("float")
        hist_lbp /= (hist_lbp.sum() + 1e-7)
        features_lbp = hist_lbp

        # Keypoint features: FAST
        fast = cv2.FastFeatureDetector_create()
        kp = fast.detect(gray, None)
        feat_fast_count = [len(kp)]
        feat_fast_resp = [np.mean([k.response for k in kp])] if kp else [0]
        
        all_features = np.hstack([features_hsv, features_glcm, features_hu, features_hog, features_lbp, feat_fast_count, feat_fast_resp])
        return np.nan_to_num(all_features)
    except Exception as e:
        print(f"Feature Extraction Error: {e}")
        return None

# --- Metadata ---
MUSHROOM_DATA = {
    "Abrupta": {"desc": "Jamur dengan bentuk unik yang tidak beraturan.", "region": "Amerika Utara", "edibility": "Tidak Diketahui"},
    "Agaricus": {"desc": "Genus jamur yang mencakup jamur kancing umum.", "region": "Seluruh Dunia", "edibility": "Dapat Dimakan (Sebagian)"},
    "Alloclavaria": {"desc": "Jamur berbentuk koral berwarna ungu.", "region": "Amerika Utara", "edibility": "Tidak Diketahui"},
    "Amanita": {"desc": "Genus yang mencakup beberapa jamur paling beracun.", "region": "Seluruh Dunia", "edibility": "Beracun / Mematikan"},
    "Bisporella": {"desc": "Jamur cangkir kuning kecil yang tumbuh di kayu.", "region": "Eropa & Amerika", "edibility": "Tidak Dimakan"},
    "Boletus": {"desc": "Jamur berpori, banyak yang lezat seperti Porcini.", "region": "Hemisfer Utara", "edibility": "Dapat Dimakan (Populer)"},
    "Chanterelle": {"desc": "Jamur corong berwarna oranye/kuning, sangat lezat.", "region": "Hutan sejuk", "edibility": "Dapat Dimakan (Pilihan)"},
    "Chlorociboria": {"desc": "Jamur cangkir hijau teal, menodai kayu.", "region": "Seluruh Dunia", "edibility": "Tidak Dimakan"},
    "Clathrus": {"desc": "Jamur keranjang merah, bau busuk.", "region": "Tropis & Subtropis", "edibility": "Tidak Dimakan"},
    "Cordyceps": {"desc": "Jamur parasit yang tumbuh pada serangga.", "region": "Asia & Tropis", "edibility": "Obat Tradisional"},
    "Cortinarius": {"desc": "Genus besar, banyak yang beracun mematikan.", "region": "Seluruh Dunia", "edibility": "Beracun"},
    "Cytidia": {"desc": "Jamur kerak yang tumbuh di kayu.", "region": "Afrika & Asia", "edibility": "Tidak Dimakan"},
    "Geastrum": {"desc": "Jamur bintang bumi, bentuknya seperti bintang.", "region": "Seluruh Dunia", "edibility": "Tidak Dimakan"},
    "Gliophorus": {"desc": "Jamur kecil, berlendir, dan berwarna cerah.", "region": "Eropa & Australia", "edibility": "Tidak Dimakan"},
    "Gyromitra": {"desc": "Morel palsu, mengandung racun mematikan jika mentah.", "region": "Eropa & Amerika", "edibility": "Beracun"},
    "Helvella": {"desc": "Jamur pelana, bentuk topi aneh.", "region": "Hemisfer Utara", "edibility": "Beracun (jika mentah)"},
    "Hydnellum": {"desc": "Jamur gigi, sering mengeluarkan cairan merah.", "region": "Amerika Utara", "edibility": "Tidak Dimakan (Keras)"},
    "Lactarius": {"desc": "Jamur susu, mengeluarkan getah saat dipotong.", "region": "Seluruh Dunia", "edibility": "Dapat Dimakan (Sebagian)"},
    "Morchella": {"desc": "Morel sejati, berbentuk sarang lebah, sangat dicari.", "region": "Hemisfer Utara", "edibility": "Dapat Dimakan (Istimewa)"},
    "Mycena": {"desc": "Jamur bonnet kecil, rapuh.", "region": "Seluruh Dunia", "edibility": "Tidak Dimakan"},
    "Pleurotus": {"desc": "Jamur tiram, tumbuh di kayu, populer dimasak.", "region": "Seluruh Dunia", "edibility": "Dapat Dimakan"},
    "Russula": {"desc": "Jamur rapuh dengan warna topi cerah.", "region": "Seluruh Dunia", "edibility": "Bervariasi (Hati-hati)"},
    "Tremella": {"desc": "Jamur kuping jeli, tekstur kenyal.", "region": "Tropis & Subtropis", "edibility": "Dapat Dimakan (Obat/Sup)"},
    "Tuber": {"desc": "Truffle, jamur bawah tanah yang sangat mahal.", "region": "Eropa", "edibility": "Dapat Dimakan (Mewah)"}
}
DEFAULT_INFO = {"desc": "Informasi tidak tersedia.", "region": "Unknown", "edibility": "Unknown"}

@app.route('/predict', methods=['POST'])
def predict():
    # Return loading error if model failed to start
    if interpreter is None:
        return jsonify({"error": f"Model not loaded. Error: {load_error}"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    try:
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None: return jsonify({"error": "Failed to decode image"}), 400

        img_resized = cv2.resize(img, IMG_SIZE)
        features = extract_features(img_resized)
        
        if features is None: return jsonify({"error": "Feature extraction failed"}), 500

        features_scaled = scaler.transform([features])
        
        # Reshape for CNN: (1, 2301, 1)
        features_cnn = features_scaled.reshape(1, features_scaled.shape[1], 1).astype(np.float32)

        # TFLite Inference
        input_index = input_details[0]['index']
        output_index = output_details[0]['index']
        
        interpreter.set_tensor(input_index, features_cnn)
        interpreter.invoke()
        preds = interpreter.get_tensor(output_index)

        class_idx = np.argmax(preds)
        confidence = float(preds[0][class_idx])
        class_name = le.inverse_transform([class_idx])[0].strip()

        info = MUSHROOM_DATA.get(class_name, DEFAULT_INFO)

        return jsonify({
            "name": class_name,
            "confidence": confidence,
            "desc": info["desc"],
            "region": info["region"],
            "edibility": info["edibility"]
        })
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
