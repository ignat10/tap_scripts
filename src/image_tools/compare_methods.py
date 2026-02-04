import numpy as np


def ssim(screen: np.ndarray, image: np.ndarray) -> tuple[float, None]:
            """Wrapper for SSIM method."""
            return quality.QualitySSIM_compute(screen, image)[0][0], None


def match_template(screen: np.ndarray, image: np.ndarray):
            """Wrapper for cv2.matchTemplate method."""
            matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
            _, result, _, coords = minMaxLoc(matched)
            return result, tuple(coords)


def numpy_diff(screen: np.ndarray, image: np.ndarray):
        diff = np.mean(np.abs(screen.astype(np.int16) - image.astype(np.int16)))
        return np.iinfo(np.uint8).max() - diff