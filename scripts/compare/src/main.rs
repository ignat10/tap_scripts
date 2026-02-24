use image;

fn main() {
    let img = image::open("D:\\Documents\\GitHub\\PythonProject\\tap_scripts\\screen.png")
        .unwrap()
        .to_luma8();
    let (width, height) = img.dimensions();
    println!("Image dimensions: {}x{}", width, height);  
}
