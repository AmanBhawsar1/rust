use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Serialize, Deserialize, Clone)] // Add the Clone trait
struct Employee {
    userId: String,
    jobTitleName: String,
    firstName: String,
    lastName: String,
    preferredFullName: String,
    employeeCode: String,
    region: String,
    phoneNumber: String,
    emailAddress: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct MyDataWrapper {
    Employees: Vec<Employee>,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/data", web::get().to(get_data))
            .route("/data", web::put().to(put_data))
            .route("/data", web::post().to(post_data))
            .route("/data", web::delete().to(delete_data))
    })
    .bind("127.0.0.1:8000")?
    .run()
    .await
}

async fn get_data() -> impl Responder {
    if let Ok(content) = fs::read_to_string("/home/aman/Downloads/data.json") {
        HttpResponse::Ok()
            .content_type("application/json")
            .body(content)
    } else {
        HttpResponse::NotFound().body("Not Found")
    }
}

async fn put_data(data: web::Json<MyDataWrapper>) -> impl Responder {
    let mut existing_data = load_existing_data();
    
    for updated_employee in &data.Employees {
        if let Some(index) = existing_data.iter().position(|e| e.userId == updated_employee.userId) {
            existing_data[index] = updated_employee.clone();
        }
    }
    
    save_data(&existing_data);

    HttpResponse::Ok().body("Data updated successfully")
}

async fn post_data(data: web::Json<MyDataWrapper>) -> impl Responder {
    let mut existing_data = load_existing_data();
    existing_data.extend(data.Employees.iter().cloned());
    save_data(&existing_data);

    HttpResponse::Created().body("Data added successfully")
}

async fn delete_data(data: web::Json<MyDataWrapper>) -> impl Responder {
    let mut existing_data = load_existing_data();
    existing_data.retain(|item| !data.Employees.iter().any(|employee| employee.userId == item.userId));
    save_data(&existing_data);

    HttpResponse::Ok().body("Data deleted successfully")
}

fn load_existing_data() -> Vec<Employee> {
    if let Ok(content) = fs::read_to_string("/home/aman/Downloads/data.json") {
        serde_json::from_str::<MyDataWrapper>(&content)
            .map(|wrapper| wrapper.Employees)
            .unwrap_or_default()
    } else {
        Vec::new()
    }
}

fn save_data(data: &[Employee]) {
    let wrapper = MyDataWrapper { Employees: data.to_vec() };
    if let Ok(updated_content) = serde_json::to_string(&wrapper) {
        if let Err(err) = fs::write("/home/aman/Downloads/data.json", updated_content) {
            println!("Error saving data: {}", err);
        }
    }
}
