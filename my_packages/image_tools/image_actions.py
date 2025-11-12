import cv2
from numpy import ndarray, frombuffer, uint8
from skimage.metrics import structural_similarity as ssim

from my_packages.adb_tools.adb_device import device
from my_packages.loaders.image_loader import read_images


class ScreenManager:
    def __init__(self):
        self.screen: ndarray =  self.capture_gray()

    def capture_gray(self) -> ndarray:
        console_output =  device.screencap()
        screen_bytes = frombuffer(console_output, uint8)
        screen = cv2.imdecode(screen_bytes, cv2.IMREAD_COLOR)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        self.screen = gray_screen
        return gray_screen

    @staticmethod
    def _cut(screen: ndarray, image: ndarray, coords: tuple[int, int]) -> ndarray:
        image_shaped = image.shape
        image_size = (image_shaped[1], image_shaped[0])
        x_half, y_half = image_size[0] // 2, image_size[1] // 2
        section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
        x0, x1, y0, y1 = section
        print(f"section: {x1 - x0, y1 - y0}, shape: {image_size} should be same")
        return screen[y0:y1, x0:x1]


class ImageAnalyzer:
    def __init__(self):
        self.images = read_images()
        self.screen_manager = ScreenManager()

    def _get_screen(self, do_screen) -> ndarray:
        return self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen

    @staticmethod
    def loop_images(method):
        def wrapper(self: ImageAnalyzer, folder_name: str, gap: float, do_screen=True, **kwargs) -> bool | tuple | None:
            screen = self._get_screen(do_screen)
            for image in self.images[folder_name].values():
                result = method(screen, image, gap, **kwargs)
                match result:
                    case float() as similarity if similarity >= gap:
                        return similarity
                    case (similarity, coords) if similarity >= gap:
                        return coords
            return None
        return wrapper

    @loop_images
    def find_part(self, screen, image) -> (float, tuple):
        matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
        _, result, _, coords = cv2.minMaxLoc(matched)
        return result, tuple(coords)

    @loop_images
    def compare_part(self, screen, image, coords: tuple[int, int]) -> float:
        cutted = self.screen_manager._cut(screen, image, coords)
        result = ssim(image, cutted, win_size=min(image.shape))
        return result

    @loop_images
    def match_screen(self, screen, image) -> float:
        return float(ssim(screen, image))
