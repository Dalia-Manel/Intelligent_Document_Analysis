# fusion.py
def fuse_results(
    ocr_text="",
    ocr_conf=0.0,
    signature_present=False,
    photo_found=False,
    checkboxes=None,
    signature_score=None,
):
    """
    Combine les résultats des modules (OCR, signature, photo, cases) en :
      - un score global de fiabilité (0–100),
      - une liste d'anomalies détectées.

    Retour : dict
        {
          "score": float,          # 0–100
          "anomalies": [str, ...],
          "details": {...}
        }
    """
    if checkboxes is None:
        checkboxes = []

    ocr_conf = float(ocr_conf) if ocr_conf is not None else 0.0

    # Composantes normalisées entre 0 et 1
    components = []
    components.append(min(max(ocr_conf / 100.0, 0.0), 1.0))   # confiance OCR
    components.append(1.0 if signature_present else 0.0)       # signature présente
    components.append(1.0 if photo_found else 0.0)             # photo présente

    # Les cases ne comptent dans le score que s'il y en a
    if checkboxes:
        ratios = [c.get("fill_ratio", 0.0) for c in checkboxes if isinstance(c, dict)]
        if ratios:
            components.append(sum(ratios) / len(ratios))

    score = round(100.0 * sum(components) / len(components), 1) if components else 0.0

    # Anomalies (points de vigilance pour un document administratif)
    anomalies = []
    if not signature_present:
        anomalies.append("Aucune signature détectée")
    if not photo_found:
        anomalies.append("Aucune photo d'identité détectée")
    if ocr_conf < 50:
        anomalies.append(f"Confiance OCR faible ({ocr_conf:.0f} %)")
    if not ocr_text or not str(ocr_text).strip():
        anomalies.append("Aucun texte extrait du document")

    return {
        "score": score,
        "anomalies": anomalies,
        "details": {
            "ocr_confidence": ocr_conf,
            "signature_present": bool(signature_present),
            "photo_found": bool(photo_found),
            "checkbox_count": len(checkboxes),
        },
    }
