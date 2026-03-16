use std::collections::HashMap;
use std::ffi::OsString;
use std::fs;
use std::path::PathBuf;
use std::sync::OnceLock;

use pyo3::prelude::*;
use serde::Deserialize;
use serde_json;

pub mod paths;
pub mod adb;
mod screen;



#[pymodule]
mod game_objects {
    use pyo3::prelude::*;

    #[pymodule_export]
    use super::get_object;

    #[pymodule_export]
    use super::init;

    #[pyfunction]
    fn say() -> i8 {print!("say"); 5}
}



static GAME_OBJECTS: OnceLock<serde_json::Value> = OnceLock::new();



#[pyfunction]
fn get_objects(data_path: PathBuf) -> HashMap<String, GameObject> {
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
#[derive(Deserialize)]
struct GameObject {
    point: Option<Point>,
    template: Option<Template>
}


#[pymethods]
impl GameObject {
    fn compare(&mut self, steps: Option<u16>) -> bool {
        let point = self.point.as_ref().unwrap();

        let coords = if let Some(steps) = steps {
            &point.move_coords(steps)
        } else {
            &point.coords
        };

        let template = self.template.as_mut().unwrap();
        let threshold = template.threshold;

        let size = template.iter_images().next().unwrap().dimensions();
        let num_pixels = size.0 * size.1;
         
        let screen = screen::get_crop(coords.x as u32, coords.y as u32, size.0, size.1);         

        template.iter_images().any(|image| {
            let total_diff: u32 = screen
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


#[derive(Deserialize)]
struct Template {
    threshold: f32,
    path: PathBuf,
    #[serde(skip, default)]
    _images: HashMap<OsString, Option<image::GrayImage>>,
}


impl Template {
    fn init(&mut self) {
        let objects_templates_dir = paths::templates().join(&self.path);
        
        for entry in fs::read_dir(objects_templates_dir).unwrap() {
            let entry = entry.unwrap();
            self._images.insert(entry.file_name(), None);
        }
    }

    fn iter_images(&mut self) -> impl Iterator<Item = &image::GrayImage> {
        if self._images.is_empty() {
            self.init();
        }

        let path = paths::templates().join(self.path.clone());

        self._images.iter_mut().filter_map(move |(key, image)| {
            if image.is_none() {
                *image = Some(image::open(path.join(key)).unwrap().to_luma8());
            }

            image.as_ref()
        })
    }
}


#[derive(Deserialize)]
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


#[derive(Deserialize)]
struct Coords {
    x: u16,
    y: u16,
}


#[derive(Deserialize)]
struct Delta {
    interval: u16,
    axis: Axis,
}


#[derive(Deserialize, PartialEq, Debug)]
enum Axis {
    X,
    Y,
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::*;


    #[test]
    fn template_test() {
        let data = r#"
            {
                "path": "path_to_template_dir",
                "threshold": 0.8
            }
        "#;

        let template_result: Result<Template, serde_json::Error> = serde_json::from_str(&data);

        assert!(template_result.is_ok());

        let template = template_result.unwrap();

        assert_eq!(template.path, PathBuf::from_str("path_to_template_dir").unwrap());
        assert_eq!(template.threshold, 0.8);
    }

    #[test]
    fn point_test() {
        let data = r#"
            {
                "coords": {
                    "x": 200,
                    "y": 900
                },
                "delta": {
                    "interval": 50,
                    "axis": "Y"
                }
            }
        "#;


        let point_result: Result<Point, serde_json::Error> = serde_json::from_str(&data);

        assert!(point_result.is_ok());

        let point = point_result.unwrap();
        let coords = &point.coords;
        let delta = &point.delta;

        assert_eq!(coords.x, 200);
        assert_eq!(coords.y, 900);

        assert_eq!(delta.axis, Axis::Y);
        assert_eq!(delta.interval, 50);

        let moved_coords = point.move_coords(3);

        assert_eq!(moved_coords.x, 200);
        assert_eq!(moved_coords.y, 1050);
    }
}