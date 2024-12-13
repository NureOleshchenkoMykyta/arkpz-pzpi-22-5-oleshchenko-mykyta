struct user_data {
    username: String,
    userId: u32,
}
fn getData() -> user_data {
    user_data {
    username: String::from("Alice"),
    userId: 1,
    }
}


fn main() {let x=5;println!("x = {}",x);}


let numbers = vec![1, 2, 3, 4];
let mut sum = 0;
for num in numbers {
    sum += num;
}


fn divide(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("Division by zero");
    }
    a / b
}

fn main() {
    match divide(10, 0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => println!("Error: {}", e),
    }
}


fn sum_array(arr: &[i32]) -> i32 {
    let mut sum = 0;
    for &num in arr {
        sum += num;
    }
    sum
}

fn max_array(arr: &[i32]) -> i32 {
    let mut max = arr[0];
    for &num in arr {
        if num > max {
            max = num;
    }
    max
}

fn main() {
    let numbers = [1, 2, 3, 4, 5];
    println!("Sum: {}", sum_array(&numbers));
    println!("Max: {}", max_array(&numbers));
}


