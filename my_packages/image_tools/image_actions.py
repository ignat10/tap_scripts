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
    def cut(fullscreen: ndarray, x0, x1, y0, y1) -> ndarray:
        return fullscreen[y0:y1, x0:x1]


class ImageAnalyzer:
    def __init__(self):
        self.images = read_images()
        self.screen_manager = ScreenManager()

    def _get_screen(self, do_screen) -> ndarray:
        return self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen

    @staticmethod
    def for_each_image(method):
        def wrapper(self: ImageAnalyzer, folder_name: str, gap: float, do_screen=True, **kwargs):
            screen = self._get_screen(do_screen)
            for image in self.images[folder_name].values():
                result = method(self, screen, image, gap, **kwargs)
                if result is not False:
                    return result
            return None
        return wrapper

    @for_each_image
    def find_part(self, screen, image, gap: float) -> tuple | None:
        matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
        _, result, _, coords = cv2.minMaxLoc(matched)
        if result >= gap:
            return tuple(coords)
        return None

    def compare_part(self, folder_name: str, coords: tuple[int, int], gap: float, do_screen=True) -> bool:
        screen = self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen
        for name, image in self.images[folder_name].items():
            image_shaped = image.shape
            image_size = (image_shaped[1], image_shaped[0])
            x_half, y_half = image_size[0] // 2, image_size[1] // 2
            section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
            cutted = self.screen_manager.cut(screen, *section)
            print(f"size of: image: {image_size} cutted: {cutted.shape}")
            resized_screen = cv2.resize(cutted, image_size)
            result = ssim(image, resized_screen, win_size=min(image_size))
            print(f"ssim {name}: {result}/{gap}")
            if result > gap:
                return True
        return False

    def match_screen(self, folder_name: str, gap: float, do_screen=True) -> bool:
        screen = self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen
        max_val: float = 0
        for name, image in self.images[folder_name].items():
            result = ssim(screen, image)
            if result >= gap:
                print(f"is full {name}. {result:.1f}/{gap}")
                return True
            max_val = max(max_val, result)
        print(f"no {folder_name}, {max_val:.1f}/{gap}")
        return False
