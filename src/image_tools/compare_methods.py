import numpy as np


# def ssim(screen: np.ndarray, image: np.ndarray, threshold: float) -> bool:
#             """Wrapper for SSIM method."""
#             similarity = cv2.quality.QualitySSIM_compute(screen, image)[0][0]
#             return similarity >= threshold


# def match_template(screen: np.ndarray, image: np.ndarray, thredshold: float) -> tuple[int, int] | None:
#             """Wrapper for cv2.matchTemplate method."""
#             matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
#             _, similarity, _, coords = cv2.minMaxLoc(matched)
#             return coords if similarity >= thredshold else None


def numpy_diff(screen: np.ndarray, image: np.ndarray, threshold: float) -> bool:
        diff = np.uint8(np.mean(np.abs(screen.astype(np.int16) - image.astype(np.int16), dtype=np.uint8), dtype=np.uint32))
        result = float((255 - diff) / 255)
        return result >= threshold
