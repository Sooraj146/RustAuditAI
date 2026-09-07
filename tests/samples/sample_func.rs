// Sample Rust function for testing RustAuditAI parser

pub fn process_user_data(data: &str) -> String {
    let mut result = String::from(data);
    let duplicate = result.clone();
    
    if data.len() > 10 {
        let boxed_val = Box::new(duplicate);
        return format!("Processed: {}", boxed_val);
    }

    unsafe {
        let ptr = data.as_ptr();
        println!("Raw pointer address: {:?}", ptr);
    }

    result
}

fn calculate_metrics(values: Vec<i32>) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}
