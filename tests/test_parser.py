import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rustaudit.parser import RustParser

def test_rust_parser():
    parser = RustParser()
    sample_path = Path(__file__).parent / "samples" / "sample_func.rs"
    
    result = parser.parse_file(str(sample_path))
    assert result.success is True
    assert len(result.functions) == 2
    
    fn1 = result.functions[0]
    assert fn1.name == "process_user_data"
    assert fn1.clone_count >= 1
    assert fn1.unsafe_block_count >= 1
    assert fn1.allocation_count >= 1
    
    fn2 = result.functions[1]
    assert fn2.name == "calculate_metrics"
    assert fn2.loop_count >= 1

    print("[OK] All RustParser tests passed successfully!")
    print(f"Parsed {len(result.functions)} functions from {sample_path.name}:")
    for fn in result.functions:
        print(f" - fn {fn.name}: clone={fn.clone_count}, unsafe={fn.unsafe_block_count}, alloc={fn.allocation_count}, loop={fn.loop_count}, branch={fn.branch_count}")

if __name__ == "__main__":
    test_rust_parser()
