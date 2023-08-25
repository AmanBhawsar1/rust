use actix_web::{web, App, HttpResponse, HttpServer};
use serde::{Deserialize, Serialize};
use std::fs;
use std::process::Command;
use std::io::Result;

#[derive(Debug, Serialize, Deserialize)]
struct MyData {
    // Define your data structure here, similar to the JSON in data.json
    // For example:
    // field1: String,
    // field2: i32,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Start Actix Web server
    let server = HttpServer::new(|| {
        App::new()
            .route("/data", web::get().to(get_data))
            .route("/data", web::put().to(put_data))
    })
    .bind("127.0.0.1:8000")?
    .run();

    // Run the server asynchronously
    let server_result = server.await;

    // Handle server result
    match server_result {
        Ok(_) => println!("Server has started."),
        Err(err) => eprintln!("Server error: {:?}", err),
    }

    // Perform a GET request using curl
    let get_output = Command::new("curl")
        .arg("http://127.0.0.1:8000/data")
        .output()?;
    
    // Print the response from the GET request
    println!("GET Response:\n{}", String::from_utf8_lossy(&get_output.stdout));

    // Define the JSON data for the PUT request
    let json_data = r#"{"field1": "new_value", "field2": 42}"#;

    // Perform a PUT request using curl
    let put_output = Command::new("curl")
        .arg("-X")
        .arg("PUT")
        .arg("-H")
        .arg("Content-Type: application/json")
        .arg("-d")
        .arg(json_data)
        .arg("http://127.0.0.1:8000/data")
        .output()?;
    
    // Print the response from the PUT request
    println!("PUT Response:\n{}", String::from_utf8_lossy(&put_output.stdout));

    Ok(())
}

async fn get_data() -> HttpResponse {
    if let Ok(content) = fs::read_to_string("/home/aman/Downloads/data.json") {
        HttpResponse::Ok()
            .content_type("application/json")
            .body(content)
    } else {
        HttpResponse::NotFound().body("Not Found")
    }
}

async fn put_data(new_data: web::Json<MyData>) -> HttpResponse {
    // You can put your original put_data logic here
    // ...

    HttpResponse::NoContent().into()
}

#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::http::{StatusCode};
    use actix_web::{test, App};

    #[actix_web::test]
    async fn test_get_data() {
        let app = App::new().route("/data", web::get().to(get_data));
        let mut app = test::init_service(app).await;

        let req = test::TestRequest::get().uri("/data").to_request();
        let resp = test::call_service(&mut app, req).await;

        assert_eq!(resp.status(), StatusCode::OK);
        // Add more assertions as needed
    }

    // Add more test cases as needed
}
