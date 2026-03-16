use std::process::{Command, Output};
use std::io::stdin;
use std::fs;

use std::sync::OnceLock;

use crate::paths;


const ADB_PORT_LENGTH: usize = 5;


static DEVICE_SERIAL: OnceLock<String> = OnceLock::new();



pub fn device_action(args: &[&str]) -> Output {
    let serial = DEVICE_SERIAL.get().unwrap();
    run([&["-s", serial], args].concat().as_slice())
}


pub fn device_config() {
    println!("connecting adb device...");

    let ip = get_ip();
    let mut serial: Option<String> = scan();

    while scan().is_none() {

        let port = input_port();
        if let Some(port) = port {
            connect(&format!("{}:{}", ip, port));
        }

        serial = scan();
    }
    DEVICE_SERIAL.set(serial.unwrap()).unwrap();
}


fn scan() -> Option<String> {
    let raw_output = run(&["devices"]).stdout;
    let text_output = String::from_utf8_lossy(&raw_output).into_owned();

    for line in text_output.lines().skip(1) {
        let mut ser_stat = line.split_whitespace();

        let serial = ser_stat.next().unwrap();
        let status = ser_stat.next().unwrap();

        if status == "device" {
            return Some(serial.to_string());
        }
    }

    None
}


fn input_port() -> Option<String> {
    println!("enter device port: ");
    let mut input = String::new();

    stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    let port = input.trim();


    return if port.parse::<u8>().is_ok() && port.len() == ADB_PORT_LENGTH {
        Some(port.to_string())
    } else {
        None
    }
}


fn connect(port: &str) -> bool {
    let raw_output = run(&["connect", port]).stdout;
    let text_output = String::from_utf8_lossy(&raw_output).into_owned();

    text_output.contains("connected to")
}


fn run(args: &[&str]) -> std::process::Output {
    Command::new("adb")
        .args(args)
        .output()
        .expect("Failed to execute adb command")
}


fn get_ip() -> String {
    let ip_path = paths::ip();
    let raw_ip = fs::read_to_string(ip_path).expect("Failed to read device IP file");
    raw_ip.trim().to_string()
}
