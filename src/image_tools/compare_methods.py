from cv2 import matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, quality
from numpy import ndarray



def ssim(screen: ndarray, image: ndarray) -> tuple[float, None]:
            """Wrapper for SSIM method."""
            return quality.QualitySSIM_compute(screen, image)[0][0], None


def match_template(screen: ndarray, image: ndarray):
            """Wrapper for cv2.matchTemplate method."""
            matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
            _, result, _, coords = minMaxLoc(matched)
            return result, tuple(coords)
