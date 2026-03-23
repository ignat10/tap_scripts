use parking_lot::{Mutex, MutexGuard, MappedMutexGuard};

use image;

use crate::adb;


static SCREEN: Mutex<Option<image::GrayImage>> =  Mutex::new(None);



pub fn get() -> MappedMutexGuard<'static, image::GrayImage> {
    let mut screen_guard = SCREEN.lock();
    
    if screen_guard.is_none() {
        set(&mut screen_guard);
    }
    
    MutexGuard::map(screen_guard, |opt| opt.as_mut().unwrap())
}


pub fn get_crop(x: u32, y: u32, width: u32, height: u32) -> image::GrayImage {
    let screen_guard = get();
    
    image::imageops::crop_imm(&*screen_guard, x, y, width, height).to_image()
}


fn set(screen_guard: &mut MutexGuard<'static, Option<image::GrayImage>>) {
    let bytes = adb::device_action(&["exec-out", "screencap",]).stdout;

    let output = adb::device_action(&["shell", "wm", "size"]).stdout;
    let size_str = String::from_utf8_lossy(&output);

    let size_part = size_str
        .split_whitespace()
        .last()
        .unwrap();

    let mut dims = size_part
        .split('x')
        .map(|s| s.parse::<u32>().unwrap());

    let w = dims.next().unwrap();
    let h = dims.next().unwrap();

    let mut gray_image: image::GrayImage = image::GrayImage::new(w, h);
    let buf = gray_image.as_mut();

    for (chunk, pixel) in bytes.chunks(4).zip(buf.iter_mut()) {
        let r = chunk[0] as u16;
        let g = chunk[1] as u16;
        let b = chunk[2] as u16;

        let gray = ((r + g + b) / 3) as u8;
        *pixel = gray;
    }
    **screen_guard = Some(gray_image);
}
