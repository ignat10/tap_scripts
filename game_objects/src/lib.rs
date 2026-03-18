use std::collections::HashMap;
use std::ffi::OsString;
use std::fs;
use std::path::PathBuf;
use std::thread::sleep;
use std::time::Duration;

use pyo3::prelude::*;
use serde::Deserialize;
use serde_json;

pub mod paths;
pub mod adb;
mod screen;



#[pymodule]
mod game_objects {
    #[pymodule_export]
    use super::get_objects;

    #[pymodule_export]
    use super::GameObject;
}


#[pyfunction]
fn get_objects(data_path: PathBuf) -> HashMap<String, GameObject> {
    paths::init(PathBuf::from(data_path));

    adb::device_config();

    serde_json::from_reader(
        fs::File::open(paths::game_objects())
        .unwrap()
    )
    .unwrap()
}


#[pyclass]
#[derive(Deserialize)]
struct GameObject {
    point: Option<Point>,
    sample: Option<Sample>
}


#[pymethods]
impl GameObject {
    #[pyo3(signature = (steps=None))]
    fn compare(&mut self, steps: Option<u16>) -> bool {
        let point = self.point.as_ref().unwrap();
        let sample = self.sample.as_mut().unwrap();

        let coords = if let Some(steps) = steps {
            &point.move_coords(steps)
        } else {
            &point.coords
        };

        let size = sample.iter_images().next().unwrap().dimensions();
        let screen = screen::get_crop(coords.x as u32, coords.y as u32, size.0, size.1);

        sample.compare(&screen)
    }

    #[pyo3(signature = (delay=None, steps=None, repeat=None))]
    fn tap(&self, delay: Option<f32>, steps: Option<u16>, repeat: Option<u8>) {
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

        if let Some(secs) = delay {
            sleep(Duration::from_secs_f32(secs))
        };
    }
}


#[derive(Deserialize)]
struct Sample {
    threshold: f32,
    path: PathBuf,
    #[serde(skip, default)]
    _images: HashMap<OsString, Option<image::GrayImage>>,
}


impl Sample {
    fn init(&mut self) {
        let samples_dir = paths::samples().join(&self.path);
        
        for entry in fs::read_dir(samples_dir).unwrap() {
            let entry = entry.unwrap();
            self._images.insert(entry.file_name(), None);
        }
    }

    fn iter_images(&mut self) -> impl Iterator<Item = &image::GrayImage> {
        if self._images.is_empty() {
            self.init();
        }

        let path = paths::samples().join(self.path.clone());

        self._images.iter_mut().filter_map(move |(key, image)| {
            if image.is_none() {
                *image = Some(image::open(path.join(key)).unwrap().to_luma8());
            }

            image.as_ref()
        })
    }


    fn compare(&mut self, comparison_image: &image::GrayImage) -> bool {
        let threshold = self.threshold;
        let dims = comparison_image.dimensions();
        let num_pixels = dims.0 * dims.1;

        self.iter_images().any(|sample_image| {
            let diff: Vec<i16> = sample_image.as_raw().iter()
                .zip(comparison_image.as_raw().iter())
                .map(|(a, b)| {
                    (*a as i16 - *b as i16).abs()
                }).collect();

            let average_diff = (diff
                .iter()
                .map(|&x| x as i32)
                .sum::<i32>() / num_pixels as i32
                ) as i16;

            let structural_duff: u8 = (diff.iter()
                .map(|&x| (x - average_diff).abs() as u32)
                .sum::<u32>()
                / num_pixels) as u8;

            let result: f32 = structural_duff as f32 / u8::MAX as f32;
            
            result >= threshold
        })
    }
}


#[derive(Deserialize)]
struct Point {
    coords: Coords,
    delta: Option<Delta>
}


impl Point {
    fn move_coords(&self, steps: u16) -> Coords {
        let delta = self.delta.as_ref().unwrap();

        let x = self.coords.x;
        let y = self.coords.y;

        match delta {
            Delta::PosX(interval) => Coords {
                x: x + interval * steps,
                y: y,
            },
            Delta::NegX(interval) => Coords {
                x: x - interval * steps,
                y: y,
            },
            Delta::PosY(interval) => Coords {
                x: x,
                y: y + interval * steps,
            },
            Delta::NegY(interval) => Coords {
                x: x,
                y: y - interval * steps
            }
        }
    }
}


#[derive(Deserialize)]
struct Coords {
    x: u16,
    y: u16,
}


#[derive(Deserialize, PartialEq, Debug)]
enum Delta {
    PosX(u16),
    NegX(u16),
    PosY(u16),
    NegY(u16),
}




#[cfg(test)]
mod tests {
    use super::*;


    #[test]
    fn sample_test() {
        let data = r#"
            {
                "path": "path_to_sample_dir",
                "threshold": 0.8
            }
        "#;

        let sample_result: Result<Sample, serde_json::Error> = serde_json::from_str(&data);

        assert!(sample_result.is_ok());

        let sample = sample_result.unwrap();

        assert_eq!(sample.path, PathBuf::from("path_to_sample_dir"));
        assert_eq!(sample.threshold, 0.8);
    }

    #[test]
    fn full_point_test() {
        let data = r#"
            {
                "coords": {
                    "x": 200,
                    "y": 900
                },
                "delta": {
                    "PosY": 50
                }
            }
        "#;


        let point_result: Result<Point, serde_json::Error> = serde_json::from_str(&data);

        assert!(point_result.is_ok());

        let point = point_result.unwrap();
        let coords = &point.coords;
        let delta = point.delta.as_ref().unwrap();

        assert_eq!(coords.x, 200);
        assert_eq!(coords.y, 900);

        assert_eq!(delta, &Delta::PosY(50));

        let moved_coords = point.move_coords(3);

        assert_eq!(moved_coords.x, 200);
        assert_eq!(moved_coords.y, 1050);

    }

    #[test]
    fn point_without_delta() {
    let data_without_delta = r#"
        {
            "coords": {
                "x": 1200,
                "y": 400
            }
        }
    "#;

        let point_result: Result<Point, serde_json::Error> = serde_json::from_str(&data_without_delta);

        assert!(point_result.is_ok());

        let point = point_result.unwrap();

        assert_eq!(point.coords.x, 1200);
        assert_eq!(point.coords.y, 400);

        assert!(point.delta.is_none());
    }

    #[test]
    fn load_objects() {
        get_objects(PathBuf::from(r"/home/kazuru/tap_scripts/data"));
    }


    fn compare_test() {
        
    }
}