# signature.py
import cv2
import numpy as np


def detect_signature_zone(image):
    """
    Detecte une zone probable de signature.
    Retourne une liste de zones pour être compatible avec l'application :
    [(x, y, w, h)]
    """
    try:
        h, w, _ = image.shape
        y1 = int(h * 0.70)

        # Retourner une liste (même avec une seule zone)
        return [(0, y1, w, h - y1)]
    except Exception:
        # En cas d'erreur : retourner liste vide
        return []


def check_signature_presence(image, signature_zones):
    """
    Vérifie si la signature est présente dans les zones détectées.

    Args:
        image : numpy array
        signature_zones : liste [(x, y, w, h)]

    Returns:
        bool : signature présente
    """

    # Si aucune zone détectée → pas de signature
    if not signature_zones:
        return False

    # On ne traite que la première zone
    zone = signature_zones[0]

    # Vérifier format correct
    if not isinstance(zone, (list, tuple)) or len(zone) < 4:
        return False

    x, y, w, h = zone

    try:
        crop = image[y:y+h, x:x+w]

        if crop.size == 0:
            return False

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)[1]

        ink_pixels = np.sum(thresh > 0)
        total_pixels = thresh.size

        ink_ratio = ink_pixels / total_pixels

        # Seuil simple : si assez d'encre, on considère qu'il y a signature
        presence = ink_ratio > 0.005

        return bool(presence)

    except Exception:
        return False
