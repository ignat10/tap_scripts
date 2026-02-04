from cv2 import matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, quality
from numpy import ndarray



def ssim(screen: ndarray, image: ndarray, threshold: float) -> bool:
            """Wrapper for SSIM method."""
            similarity = quality.QualitySSIM_compute(screen, image)[0][0]
            return similarity >= threshold


def match_template(screen: ndarray, image: ndarray, threshold: float) -> tuple[int, int] | None:
            """Wrapper for cv2.matchTemplate method."""
            matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
            _, similarity, _, coords = minMaxLoc(matched)
            return coords if similarity >= threshold else None
