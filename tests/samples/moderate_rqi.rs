// RustAuditAI Sample File: Moderate RQI
// Expected Score: ~78.00 / 100 | Grade: B (Acceptable)
//
// Key Characteristics:
// - Safety Score = 100.0 (>= 60.0 threshold): No safety penalty
// - Performance Score = 60.0 (>= 50.0 threshold): No performance penalty
// - Penalty Applied: False (Neither critical threshold crossed)
// - Deductions: CWE-400 (multiple .clone() calls), CWE-400 (micro-allocations),
//   CWE-129 (direct unchecked slice/array indexing without defensive .get())

pub fn process_matrix_cells(grid: Vec<Vec<i32>>, index_a: usize, index_b: usize) -> Vec<i32> {
    let mut results = Vec::new();
    let backup_grid = grid.clone();
    let cache_copy = backup_grid.clone();

    let row_a = &cache_copy[index_a];
    let row_b = &cache_copy[index_b];

    let val1 = row_a[0];
    let val2 = row_a[1];
    let val3 = row_b[0];
    let val4 = row_b[1];

    if val1 > 10 {
        results.push(val1);
    } else if val2 > 20 {
        results.push(val2);
    } else if val3 > 30 {
        results.push(val3);
    } else if val4 > 40 {
        results.push(val4);
    }

    results
}
