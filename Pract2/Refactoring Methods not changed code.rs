  fn process_orders(orders: Vec<(u32, f32)>, discount_rate: f32) {
    let mut total = 0.0;
    for (quantity, price) in &orders {
        let mut item_total = *quantity as f32 * price;
        if item_total > 100.0 {
            item_total -= item_total * discount_rate;
        }
        println!("Processed item: ${}", item_total);
        total += item_total;
    }
    println!("Total: ${}", total);
}


  fn calculate(value: f64, v: f64, t: f64) -> f64 {
    let result = value * (v + t).sin();
    result
}


  
  fn determine_shipping_cost(weight: f32, distance: f32) -> f32 {
    if weight > 10.0 {
        if distance > 500.0 {
            return weight * 1.5;
        } else {
            return weight * 1.2;
        }
    } else {
        if distance > 500.0 {
            return weight * 1.0;
        } else {
            return weight * 0.8;
        }
    }
}
