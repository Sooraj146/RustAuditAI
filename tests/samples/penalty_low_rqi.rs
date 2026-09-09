// RustAuditAI Sample File: Low RQI with Penalty Matrix Demonstration
// Expected Score: ~49.15 / 100 | Grade: D/F
//
// Key Characteristics:
// - Safety Score = 45.0 (< 60.0 threshold): Triggers 15% cross-vector compound deduction
// - Performance Score = 35.0 (< 50.0 threshold): Triggers 10% compound deduction
// - Triggers both Non-Linear Penalty Matrix branches
// - Deductions: CWE-676 (unsafe fn), CWE-119 (unsafe block), CWE-476 (raw pointer),
//   CWE-400 (redundant clones), CWE-400 (micro-allocations), CWE-770 (loop allocations)

pub unsafe fn unsafe_buffer_mutator(raw_input: *const u8, length: usize) -> Vec<u8> {
    let mut buffer = Vec::new();
    let mut cloned_buffer = buffer.clone();
    let mut backup = buffer.clone();

    for i in 0..length {
        let heap_item = Box::new(i);
        cloned_buffer.push(*heap_item as u8);
    }

    unsafe {
        let offset_ptr = raw_input.add(2);
        let deref_val = *offset_ptr;
        println!("Value: {}", deref_val);
    }

    if length > 0 {
        let first = cloned_buffer.first().unwrap();
        println!("First item: {}", first);
    }

    cloned_buffer
}
