// RustAuditAI Sample File: Optimal RQI (Grade A+ Idiomatic & Robust)
// Expected Score: 100.00 / 100 | Grade: A+
//
// Key Characteristics:
// - Safety Score = 100.0 (Zero unsafe keywords, blocks, or raw pointers)
// - Performance Score = 100.0 (Zero unnecessary clones or heap allocations)
// - Maintainability Score = 100.0 (Clean functional iterator pipeline, low cyclomatic complexity)
// - Security Score = 100.0 (Zero unchecked indexing or unhandled panic paths)
// - Penalty Applied: False
// - Zero quality deductions

pub fn sum_even_squares(numbers: &[i32]) -> i64 {
    numbers
        .iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| (n as i64) * (n as i64))
        .sum()
}
