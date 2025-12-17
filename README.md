# 🍄 Mushroom Vision - Computer Vision Project

Aplikasi web berbasis Computer Vision untuk identifikasi dan klasifikasi berbagai jenis jamur menggunakan Deep Learning (CNN). Project ini dibuat untuk tugas akhir Computer Vision.

## 📋 Deskripsi

Mushroom Vision adalah aplikasi yang dapat mengidentifikasi berbagai jenis jamur dari gambar menggunakan model Convolutional Neural Network (CNN). Aplikasi ini dilengkapi dengan informasi tentang jenis jamur yang terdeteksi, termasuk deskripsi, region, dan status edibility (dapat dimakan/tidak).

## 🛠️ Tech Stack

### Backend

- **Python 3.x**
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep Learning framework
- **OpenCV** - Image processing
- **scikit-learn** - Machine learning utilities
- **scikit-image** - Feature extraction (HOG, LBP, GLCM)

### Frontend

- **React 19** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **Lucide React** - Icons

## 📁 Struktur Project

```
Mushroom/
├── backend/                    # Flask API Server
│   ├── app.py                 # Main Flask application
│   ├── best_mushroom_cnn.keras # Trained CNN model
│   ├── mushroom_scaler_2.joblib # Feature scaler
│   ├── mushroom_le_2.joblib   # Label encoder
│   ├── check_classes.py       # Utility script
│   └── requirements.txt       # Python dependencies
│
├── computervision/            # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Hero/         # Hero section
│   │   │   ├── Navbar/       # Navigation bar
│   │   │   └── Scanner/      # Image scanner component
│   │   └── App.tsx           # Main app component
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
├── FOURTH TEST/               # Training notebooks
│   └── AOL_CV_CNN_Manual_2.ipynb  # Model training notebook
│
├── run.bat                    # Quick start script (Windows)
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Prerequisites

Sebelum menjalankan project, pastikan sudah terinstall:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** dan **npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **Git LFS** (untuk file model) - [Download Git LFS](https://git-lfs.github.com/)

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/mushroom-vision.git
cd mushroom-vision
```

### 2. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies yang akan terinstall:**

- flask
- flask-cors
- opencv-python
- numpy
- scikit-image
- scikit-learn
- keras
- tensorflow
- joblib

### 3. Setup Frontend

```bash
cd computervision
npm install
```

## ▶️ Cara Menjalankan

### Opsi 1: Menggunakan run.bat (Windows)

Double-click file `run.bat` di root folder. Script ini akan menjalankan backend dan frontend secara bersamaan.

### Opsi 2: Manual (Semua OS)

#### Jalankan Backend

```bash
cd backend
python app.py
```

Backend akan berjalan di **http://localhost:5000**

#### Jalankan Frontend (Terminal baru)

```bash
cd computervision
npm run dev
```

Frontend akan berjalan di **http://localhost:5173** (atau port lain yang tersedia)

### Verifikasi Setup

1. Buka browser dan akses **http://localhost:5173**
2. Pastikan backend sudah running (check console untuk pesan "Model load success")
3. Upload gambar jamur untuk testing

## 🔌 API Documentation

### Endpoint: `/predict`

**Method:** `POST`

**Content-Type:** `multipart/form-data`

**Request:**

- `image` (file): Gambar jamur yang akan diidentifikasi

**Response (Success):**

```json
{
  "name": "Morchella",
  "confidence": 0.95,
  "desc": "Morel sejati, berbentuk sarang lebah, sangat dicari.",
  "region": "Hemisfer Utara",
  "edibility": "Dapat Dimakan (Istimewa)"
}
```

**Response (Error):**

```json
{
  "error": "Error message"
}
```

## 🍄 Jenis Jamur yang Dapat Diidentifikasi

Model dapat mengidentifikasi berbagai jenis jamur, termasuk (tidak terbatas pada):

- **Agaricus** - Jamur kancing
- **Boletus** - Porcini
- **Chanterelle** - Jamur corong oranye
- **Morchella** - Morel
- **Amanita** - Jamur beracun
- **Pleurotus** - Jamur tiram
- **Tuber** - Truffle
- Dan banyak lagi...

*Catatan: Model dilatih dengan dataset tertentu, akurasi mungkin bervariasi tergantung kualitas gambar.*

## 🔧 Model Information

- **Architecture:** CNN (Convolutional Neural Network)
- **Input Size:** 128x128 pixels
- **Features:** Kombinasi HOG, LBP, GLCM, dan HSV histograms
- **Training:** Dilakukan di notebook `FOURTH TEST/AOL_CV_CNN_Manual_2.ipynb`

## 📝 Development Notes

- Model files (`.keras`, `.joblib`) dikelola menggunakan **Git LFS** karena ukuran yang besar
- Pastikan Git LFS sudah terinstall sebelum clone repository
- Jika model files tidak ter-download, jalankan: `git lfs pull`

## 🌐 Deployment

### Live Demo
- **URL:** [https://mushroom-vision-phi.vercel.app/](https://mushroom-vision-phi.vercel.app/)

### Frontend (Vercel)
Sudah ter-deploy secara otomatis.

### Backend (Railway)
**Status:** Active (Trial Mode)

> [!WARNING]
> **Masa Berlaku Deployment Backend:**
> Backend deployment di Railway menggunakan **Trial Plan** yang akan berakhir dalam **30 hari**.
>
> **Jika deployment mati/trial habis:**
> 1. Gunakan opsi **Jalankan Lokal** menggunakan `run.bat` di laptop Anda.
> 2. `run.bat` sudah diupdate untuk otomatis menginstall semua dependencies yang diperlukan.
> 3. Aplikasi akan berjalan 100% normal di localhost.

## ⚠️ Important Notes

- **Jangan mengandalkan aplikasi ini untuk menentukan apakah jamur aman untuk dimakan.** Selalu konsultasikan dengan ahli jamur (mycologist) profesional.
- Model ini untuk tujuan edukasi dan demonstrasi Computer Vision saja.
- Akurasi model tergantung pada kualitas dan kondisi gambar input.

## 📄 License

Project ini dibuat untuk tujuan akademis (tugas akhir Computer Vision).

## 👤 Author

* CALVIN JUNAIDY - 2702225865
* JANICE TIFFANY - 2702215630
* ANDY SAPUTRA - 2702234094

## 🙏 Acknowledgments

- Frontend component dibuat oleh ANDY SAPUTRA - 2702234094
- Dataset dan model training menggunakan teknik Computer Vision modern

---

**⚠️ Disclaimer:** Aplikasi ini tidak dimaksudkan sebagai pengganti konsultasi profesional untuk identifikasi jamur yang aman untuk dikonsumsi. Selalu berhati-hati dan konsultasikan dengan ahli sebelum mengonsumsi jamur liar.
