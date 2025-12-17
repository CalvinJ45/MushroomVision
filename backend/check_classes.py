import joblib
import os

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    le_path = os.path.join(BASE_DIR, "mushroom_le.joblib")
    print(f"Loading LE from: {le_path}")
    le = joblib.load(le_path)
    print("Classes in LabelEncoder:")
    for cls in le.classes_:
        print(f"'{cls}'")
except Exception as e:
    print(f"Error: {e}")
