struct UserData {
    username: String,
    user_id: u32,
}
fn get_data() -> UserData {
    UserData {
    username: String::from("Alice"),
    user_id: 1,
    }
}


fn main() {
    let x = 5;
    println!("x = {}", x);
}


mod utils;
fn main() {
    utils::greet("Alice");
}

pub fn greet(name: &str) {
    println!("Hello, {}!", name);
}


let numbers = vec![1, 2, 3, 4];
let sum: i32 = numbers.iter().sum();


/// Додає два числа.
///
/// # Приклад
/// ```
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
fn add(a: i32, b: i32) -> i32 {
    a + b
}
#[cfg(test)]
mod {
    use super::*;
    #[test]
    fn test_add() {
    assert_eq!(add(2, 3), 5);
tests
 
    }
}


fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
    return Err(String::from("Division by zero"));
    }
    Ok(a / b)
}

fn main() {
    match divide(10, 0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => println!("Error: {}", e),
    }
}


fn process_array<F>(arr: &[i32], operation: F) -> i32
where
    F: Fn(i32, i32) -> i32,
{
    arr.iter().copied().reduce(operation).unwrap_or(0)
}

fn main() {
    let numbers = [1, 2, 3, 4, 5];

    let sum = process_array(&numbers, |a, b| a + b); // Використовуємо + для суми
    let max = process_array(&numbers, |a, b| a.max(b)); // Використовуємо max для максимуму

    println!("Sum: {}", sum); // Сума: 15
    println!("Max: {}", max); // Максимум: 5
}
