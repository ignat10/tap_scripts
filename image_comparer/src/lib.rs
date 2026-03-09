use std::collections:: {HashMap, HashSet};
use std::ffi::OsString;
use std::fs;
use std::path::PathBuf;
use std::sync::OnceLock;

use image::GenericImageView;
use pyo3::prelude::*;
use serde::Deserialize;
use serde_json;

pub mod paths;
pub mod adb;
mod screen;


static GAME_OBJECTS: OnceLock<serde_json::Value> = OnceLock::new();


#[pymodule]
mod image_comparer {
    #[pymodule_export]
    use super::{
        get_object,
        init,
    };
}


#[pyfunction]
fn init(data_path: &str) {
    paths::init(PathBuf::from(data_path));

    GAME_OBJECTS.set(serde_json::from_reader(
        fs::File::open(paths::get_game_objects()).unwrap()
    ).unwrap()).unwrap();
}


#[pyfunction]
fn get_object(name: &str) -> Option<GameObject> {
    let v = GAME_OBJECTS
        .get()
        .unwrap()
        .get(name)?;

    let game_object: GameObject = serde_json::from_value(v.clone()).unwrap();
    Some(game_object)
}


#[pyclass]
#[derive(Debug, Deserialize)]
struct GameObject {
    point: Option<Point>,
    template: Option<Template>
}


#[pymethods]
impl GameObject {
    fn compare(&mut self, steps: u8) -> bool {
        let coords = &self.point.as_ref().unwrap().coords;
        let template = self.template.as_mut().unwrap();
        let threshold = template.threshold;

        let screen_guard = screen::get();
        let size = screen_guard.dimensions();
        let cropped_screen = image::imageops::crop_imm(&*screen_guard, coords.x as u32, coords.y as u32, size.0, size.1);

        let num_pixels = size.0 * size.1;
         

        template.iter_images().any(|image| {
            let total_diff: u32 = cropped_screen.pixels()
                .map(|(_x, _y, pixel)| pixel.0[0])
                .zip(image.iter())
                .map(|(a, b)| (a as i16 - *b as i16).abs() as u32)
                .sum();

            let normalized_diff: f32 = (total_diff / num_pixels) as f32 / u8::MAX as f32;

            normalized_diff > threshold
        })
    }

    fn tap(&self, steps: u16, repeat: u8) {
        let point = self.point.as_ref().unwrap();
        let coords = &point.coords;

        let moved_coords = match point.delta.axis {
            Axis::X => Coords {
                x: coords.x + point.delta.interval * steps,
                y: coords.y,
            },
            Axis::Y => Coords {
                x: coords.x,
                y: coords.y + point.delta.interval * steps,
            },
        };

        let x = moved_coords.x.to_string();
        let y = moved_coords.y.to_string();

        for _ in 0..repeat {
            adb::device_action(&[&x, &y]);
        }
    }
}


#[derive(Deserialize, Debug)]
struct Template {
    threshold: f32,
    path: PathBuf,
    #[serde(skip, default)]
    _images: HashMap<OsString, Option<Vec<u8>>>,
    #[serde(skip, default)]
    _used_images: HashSet<OsString>,
}


impl Template {
    fn init(&mut self) {
        for entry in fs::read_dir(&self.path).unwrap() {
            let entry = entry.unwrap();
            self._images.insert(entry.file_name(), None);
        }
    }

    fn iter_images(&mut self) -> impl Iterator<Item = &Vec<u8>> {
        if self._images.is_empty() {
            self.init();
        }

        self._images.iter_mut().filter_map(|(key, image)| {
            if self._used_images.contains(key) {
                None
            } else {
                if image.is_none() {
                    *image = Some(image::open(self.path.join(key)).unwrap().into_luma8().into_raw());
                }
                self._used_images.insert(key.clone());
                image.as_ref()
            }
        })
    }
}


#[derive(Deserialize, Debug)]
struct Point {
    coords: Coords,
    delta: Delta
}


#[derive(Deserialize, Debug)]
struct Coords {
    x: u16,
    y: u16,
}


#[derive(Deserialize, Debug)]
struct Delta {
    interval: u16,
    axis: Axis,
}


#[derive(Deserialize, Debug)]
enum Axis {
    X,
    Y,
}
