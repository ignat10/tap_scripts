use std::collections::HashMap;
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



#[pymodule]
mod game_objects {
    #[pymodule_export]
    use super::{
        get_object,
        init,
    };
}



static GAME_OBJECTS: OnceLock<serde_json::Value> = OnceLock::new();



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
    fn compare(&mut self, steps: Option<u16>) -> bool {
        let steps = steps.unwrap_or(0);

        let coords = self.point
            .as_ref()
            .unwrap()
            .move_coords(steps);

        let template = self.template.as_mut().unwrap();
        let threshold = template.threshold;

        let size = template.iter_images().next().unwrap().dimensions();

        let screen_guard = screen::get();
        let screen_part = screen_guard.view(coords.x as u32, coords.y as u32, size.0, size.1).to_image();

        let num_pixels = size.0 * size.1;
         

        template.iter_images().any(|image| {
            let total_diff: u32 = screen_part
                .iter()
                .zip(image.iter())
                .map(|(a, b)| (*a as i16 - *b as i16).abs() as u32)
                .sum();

            let normalized_diff: f32 = (total_diff / num_pixels) as f32 / u8::MAX as f32;

            normalized_diff > threshold
        })
    }

    fn tap(&self, steps: Option<u16>, repeat: Option<u8>) {
        let point = self.point.as_ref().unwrap();
        let coords = if let Some(steps) = steps {
            &point.move_coords(steps)
        } else {
            &point.coords
        };
        let x = coords.x.to_string();
        let y = coords.y.to_string();

        for _ in 0..repeat.unwrap_or(1) {
            adb::device_action(&[&x, &y]);
        }
    }
}


#[derive(Deserialize, Debug)]
struct Template {
    threshold: f32,
    path: PathBuf,
    #[serde(skip, default)]
    _images: HashMap<OsString, Option<image::GrayImage>>,
}


impl Template {
    fn init(&mut self) {
        for entry in fs::read_dir(&self.path).unwrap() {
            let entry = entry.unwrap();
            self._images.insert(entry.file_name(), None);
        }
    }

    fn iter_images(&mut self) -> impl Iterator<Item = &image::GrayImage> {
        if self._images.is_empty() {
            self.init();
        }

        let path = self.path.clone();

        self._images.iter_mut().filter_map(move |(key, image)| {
            if image.is_none() {
                *image = Some(image::open(path.join(key)).unwrap().to_luma8());
            }

            image.as_ref()
        })
    }
}


#[derive(Deserialize, Debug)]
struct Point {
    coords: Coords,
    delta: Delta
}


impl Point {
    fn move_coords(&self, steps: u16) -> Coords {
        match self.delta.axis {
            Axis::X => Coords {
                x: self.coords.x + self.delta.interval * steps,
                y: self.coords.y,
            },
            Axis::Y => Coords {
                x: self.coords.x,
                y: self.coords.y + self.delta.interval * steps,
            },
        }
    }
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
