"""Agent: OCR (PaddleOCR v3.5+ fallback a tesseract)."""
from pathlib import Path
import logging
log = logging.getLogger("ocr")

def run_ocr(path: Path) -> str:
    """Lee un archivo. Si es txt/md lo devuelve tal cual. Si es pdf/img intenta OCR."""
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in (".pdf", ".png", ".jpg", ".jpeg"):
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang="es", show_log=False)
            result = ocr.ocr(str(path), cls=True)
            return "\n".join([line[1][0] for line in result[0] if line])
        except ImportError:
            log.warning("paddleocr not installed, falling back to tesseract")
            try:
                import pytesseract
                from PIL import Image
                img = Image.open(path)
                return pytesseract.image_to_string(img, lang="spa")
            except ImportError:
                return f"[OCR skipped: {path.name} - no OCR lib installed]"
    return f"[Unknown format: {path.name}]"
