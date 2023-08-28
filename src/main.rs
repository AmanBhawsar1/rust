use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::Write;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Data {
    key: String,
    value: String,
}

async fn read_data() -> impl Responder {
    let file_content = fs::read_to_string("/home/aman/Downloads/data.json").unwrap();
    let data: Vec<Data> = serde_json::from_str(&file_content).unwrap();
    HttpResponse::Ok().json(data)
}

async fn add_data(new_data: web::Json<Data>) -> impl Responder {
    let mut file_content = fs::read_to_string("/home/aman/Downloads/data.json").unwrap();
    let mut data: Vec<Data> = serde_json::from_str(&file_content).unwrap();

    data.push(new_data.into_inner()); // Move inner value into data vector

    save_data(&data);
    HttpResponse::Ok().body("Data added")
}

async fn update_data(updated_data: web::Json<Data>) -> impl Responder {
    let mut file_content = fs::read_to_string("/home/aman/Downloads/data.json").unwrap();
    let mut data: Vec<Data> = serde_json::from_str(&file_content).unwrap();
    
    if let Some(existing_data) = data.iter_mut().find(|d| d.key == updated_data.key) {
        existing_data.value = updated_data.value.clone();
        save_data(&data);
        HttpResponse::Ok().body("Data updated")
    } else {
        HttpResponse::NotFound().body("Data not found")
    }
}

fn save_data(data: &[Data]) {
    let updated_content = serde_json::to_string(data).unwrap();
    let mut file = fs::File::create("/home/aman/Downloads/data.json").unwrap();
    file.write_all(updated_content.as_bytes()).unwrap();
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(web::resource("/read").route(web::get().to(read_data)))
            .service(web::resource("/add").route(web::post().to(add_data)))
            .service(web::resource("/update").route(web::post().to(update_data)))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
