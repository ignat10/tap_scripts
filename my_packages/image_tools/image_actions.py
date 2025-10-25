import cv2
from numpy import ndarray, frombuffer, uint8
from skimage.metrics import structural_similarity as ssim

from my_packages.core.adb_device import device
from my_packages.loaders.image_loader import read_images


class ScreenManager:
    def __init__(self):
        self.screen =  device.screencap()

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

    def find_part(self, folder_name: str, gap: float, do_screen=True) -> tuple | None:
        screen = self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen
        max_val: float = 0.0
        for image in self.images[folder_name]:
            matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
            _, result, _, coords = cv2.minMaxLoc(matched)
            if result >= gap:
                print(f"matched {result}/{gap}")
                return tuple(coords)
            max_val = max(max_val, result)
        print(f"no matched {max_val}/{gap}")
        return None

    def compare_part(self, folder_name: str, coords: tuple[int, int], gap: float, do_screen=True) -> bool:
        screen = self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen
        for image in self.images[folder_name]:
            image_shaped = image.shape
            image_size = (image_shaped[1], image_shaped[0])
            x_half, y_half = image_size[0] // 2, image_size[1] // 2
            section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
            cutted = self.screen_manager.cut(screen, *section)
            print(f"size of: image: {image_size} cutted: {cutted.shape}")
            resized_screen = cv2.resize(cutted, image_size)
            result = ssim(image, resized_screen, win_size=min(image_size))
            print(f"ssim result: {result}")
            if result > gap:
                return True
        return False

    def match_screen(self, folder_name: str, gap: float, do_screen=True) -> bool:
        screen = self.screen_manager.capture_gray() if do_screen else self.screen_manager.screen
        max_val: float = 0
        for image in self.images[folder_name]:
            result = ssim(screen, image)
            if result >= gap:
                print(f"is full {folder_name}. {result}/{gap}")
                return True
            max_val = max(max_val, result)
        print(f"no full {max_val}/{gap}")
        return False
