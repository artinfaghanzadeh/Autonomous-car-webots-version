import numpy as np
import cv2

from config_loader import parameters as cfg


def adjust_gamma(img, gamma: float):
    inv = 1.0 / (gamma + 1e-6)
    table = np.array([(i / 255.0) ** inv * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(img, table)


def apply_brightness_mode(gray_raw: np.ndarray):
    mean_raw = float(np.mean(gray_raw))
    use_boost = mean_raw < cfg.DARK_THRESHOLD

    if use_boost:
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
        gray = clahe.apply(gray_raw)

        gamma = 160.0 / (np.mean(gray) + 1e-6)
        gamma = float(np.clip(gamma, 0.5, 3.0))
        gray = adjust_gamma(gray, gamma)

        gray = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        mode = "BOOST"
    else:
        gray = gray_raw.copy()
        mode = "NORMAL"

    mode_text = f"Mode={mode} MeanRaw={mean_raw:.1f} Thr={cfg.DARK_THRESHOLD:.1f}"
    return gray, mode_text, mean_raw


def denoise(gray: np.ndarray) -> np.ndarray:
    blur = cv2.GaussianBlur(gray, (9, 9), 2)
    blur = cv2.medianBlur(blur, 5)
    return blur


def detect_edges(blur: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(blur, cfg.CANNY_LOW, cfg.CANNY_HIGH)
    kernel = np.ones((cfg.MORPH_KERNEL_SIZE, cfg.MORPH_KERNEL_SIZE), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    return edges