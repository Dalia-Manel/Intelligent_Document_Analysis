# pipeline.py
# Pipeline de traitement en ligne de commande (alternative à l'interface Streamlit).
import os
import sys
import cv2

# Rendre les modules du dossier app/ importables depuis src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from ocr import extract_text
from signature import detect_signature_zone, check_signature_presence
from fusion import fuse_results

# Modules optionnels (fallback si absents)
try:
    from face_detector import detect_photo
except Exception:
    def detect_photo(image):
        return False, None

try:
    from checkbox import detect_checkboxes
except Exception:
    def detect_checkboxes(image):
        return []


def run_full_pipeline(image_path):
    """
    Exécute toutes les étapes de traitement :
    chargement image → OCR → signature → photo → cases → fusion.
    """
    # 1. Chargement de l'image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de lire l'image : {image_path}")

    # 2. OCR (retourne texte + confiance)
    ocr_text, ocr_conf = extract_text(image)

    # 3. Signature (détecter la zone puis vérifier la présence)
    signature_zones = detect_signature_zone(image)
    signature_present = check_signature_presence(image, signature_zones)

    # 4. Photo d'identité (retourne (bool, zone))
    photo_found, _photo_zone = detect_photo(image)

    # 5. Cases à cocher
    checkboxes = detect_checkboxes(image)

    # 6. Fusion finale
    result = fuse_results(
        ocr_text=ocr_text,
        ocr_conf=ocr_conf,
        signature_present=signature_present,
        photo_found=photo_found,
        checkboxes=checkboxes,
    )

    return result


if __name__ == "__main__":
    test_image = sys.argv[1] if len(sys.argv) > 1 else "test.jpg"
    res = run_full_pipeline(test_image)
    print(res)
