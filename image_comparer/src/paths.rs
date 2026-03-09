use std::sync::OnceLock;
use std::path::PathBuf;


static DATA: OnceLock<PathBuf> = OnceLock::new();



pub fn init(data_path: PathBuf) {
    DATA.set(data_path).unwrap();
}


pub fn get_ip() -> PathBuf {
    DATA
        .get()
        .unwrap()
        .join("device_ip.json")
}


pub fn get_game_objects() -> PathBuf {
    DATA
        .get()
        .unwrap()
        .join("game_objects.json")
}
