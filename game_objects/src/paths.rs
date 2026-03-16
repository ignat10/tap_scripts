use std::sync::OnceLock;
use std::path::{Path, PathBuf};


static DATA: OnceLock<PathBuf> = OnceLock::new();



pub fn init(data_path: PathBuf) {
    DATA.set(data_path).unwrap();
}


pub fn ip() -> PathBuf {
    data_dir().join("device_ip.json")
}


pub fn game_objects() -> PathBuf {
    data_dir().join("game_objects.json")
}


pub fn templates() -> PathBuf {
    data_dir().join("templates")
}


fn data_dir() -> &'static Path {
    DATA.get().expect("DATA has not been initialized. Call paths::init() before using.")
}
