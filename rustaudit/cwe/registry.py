"""
MITRE Common Weakness Enumeration (CWE) Catalog & Tagging Registry for RustAuditAI.
Standardizes security weaknesses, code quality defects, severity classifications, and remediation paths.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class CWEDefinition:
    """
    Metadata representation of an official MITRE Common Weakness Enumeration (CWE).
    """
    cwe_id: str
    name: str
    description: str
    category: str
    default_severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    url: str
    remediation: str


@dataclass
class CWETag:
    """
    Localized instance of a CWE weakness identified within a specific Rust subroutine.
    """
    cwe_id: str
    name: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    category: str
    url: str
    line_number: Optional[int] = None
    statement_code: Optional[str] = None
    message: str = ""
    remediation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cwe_id": self.cwe_id,
            "name": self.name,
            "cwe_name": self.name,
            "severity": self.severity,
            "category": self.category,
            "url": self.url,
            "cwe_url": self.url,
            "line_number": self.line_number,
            "statement_code": self.statement_code,
            "message": self.message,
            "description": self.message,
            "remediation": self.remediation,
        }


class CWERegistry:
    """
    Centralized registry of MITRE CWE taxonomy definitions mapped to Rust program analysis indicators.
    """

    CATALOG: Dict[str, CWEDefinition] = {
        "CWE-119": CWEDefinition(
            cwe_id="CWE-119",
            name="Improper Restriction of Operations within the Bounds of a Memory Buffer",
            description="The software performs operations on a memory buffer, but it can read from or write to a memory location outside the intended boundary.",
            category="Memory Safety",
            default_severity="HIGH",
            url="https://cwe.mitre.org/data/definitions/119.html",
            remediation="Eliminate `unsafe` blocks and raw pointer manipulations; replace with safe reference abstractions (`&T`, `&mut T`) and bounded standard library types.",
        ),
        "CWE-476": CWEDefinition(
            cwe_id="CWE-476",
            name="NULL Pointer Dereference",
            description="A NULL or dangling pointer dereference occurs when the application dereferences a pointer that it expects to be valid, but is NULL or invalid.",
            category="Memory Safety",
            default_severity="HIGH",
            url="https://cwe.mitre.org/data/definitions/476.html",
            remediation="Avoid raw pointer conversions (`.as_ptr()`, `.as_mut_ptr()`); use safe Rust references or `NonNull<T>` with explicit non-null checks.",
        ),
        "CWE-416": CWEDefinition(
            cwe_id="CWE-416",
            name="Use After Free",
            description="Referencing memory after it has been freed can cause a program to crash, use unexpected values, or execute arbitrary code.",
            category="Memory Safety",
            default_severity="CRITICAL",
            url="https://cwe.mitre.org/data/definitions/416.html",
            remediation="Rely on Rust's borrow checker to manage lifetimes; avoid manual deallocation or storing raw pointer aliases across move boundaries.",
        ),
        "CWE-252": CWEDefinition(
            cwe_id="CWE-252",
            name="Unchecked Return Value",
            description="The software does not check the return value from a method or function, which can prevent it from detecting unexpected states or conditions.",
            category="Error Handling & Logic",
            default_severity="MEDIUM",
            url="https://cwe.mitre.org/data/definitions/252.html",
            remediation="Replace unvalidated `.unwrap()` and `.expect()` invocations with pattern matching (`match`, `if let`), `?` error propagation, or `.unwrap_or()`.",
        ),
        "CWE-129": CWEDefinition(
            cwe_id="CWE-129",
            name="Improper Validation of Array Index",
            description="The product uses an untrusted or unvalidated input value as an index, which may result in an out-of-bounds read or write causing a runtime panic.",
            category="Defensive Security",
            default_severity="MEDIUM",
            url="https://cwe.mitre.org/data/definitions/129.html",
            remediation="Use defensive `.get(index)` slice access returning `Option<&T>` instead of direct indexing `arr[index]` to prevent runtime panic crashes.",
        ),
        "CWE-400": CWEDefinition(
            cwe_id="CWE-400",
            name="Uncontrolled Resource Consumption",
            description="The product does not properly control the allocation or maintenance of a limited system resource, such as memory or CPU cycles.",
            category="Resource Management",
            default_severity="MEDIUM",
            url="https://cwe.mitre.org/data/definitions/400.html",
            remediation="Avoid unnecessary deep memory duplicates (`.clone()`); pass values by reference (`&T`, `&str`) to minimize memory bandwidth overhead.",
        ),
        "CWE-770": CWEDefinition(
            cwe_id="CWE-770",
            name="Allocation of Resources Without Limits or Throttling",
            description="The software allocates a resource without imposing any limits on the amount of resource that can be allocated.",
            category="Resource Management",
            default_severity="HIGH",
            url="https://cwe.mitre.org/data/definitions/770.html",
            remediation="Avoid micro-heap allocations (`Box::new`, `Vec::new`, `String::from`) inside tight loop scopes; pre-allocate capacity with `with_capacity()`.",
        ),
        "CWE-710": CWEDefinition(
            cwe_id="CWE-710",
            name="Improper Adherence to Coding Standards",
            description="The software does not follow the coding conventions or rules of the implementation language or framework, degrading maintainability.",
            category="Complexity & Maintainability",
            default_severity="LOW",
            url="https://cwe.mitre.org/data/definitions/710.html",
            remediation="Decompose high-complexity routines (McCabe V(G) > 5) into smaller, focused helper functions with clear single responsibilities.",
        ),
        "CWE-1075": CWEDefinition(
            cwe_id="CWE-1075",
            name="Unconditional Control Flow Transfer",
            description="The program contains control flow structures that transfer control unconditionally or in a convoluted manner, creating structural traps.",
            category="Complexity & Maintainability",
            default_severity="LOW",
            url="https://cwe.mitre.org/data/definitions/1075.html",
            remediation="Simplify nested loop headers and deep branching layouts; refactor into functional iterators (`.map()`, `.filter()`, `.fold()`).",
        ),
        "CWE-676": CWEDefinition(
            cwe_id="CWE-676",
            name="Use of Potentially Dangerous Function",
            description="The program invokes an inherently dangerous function or language feature that cannot be guaranteed to be safe.",
            category="Defensive Security",
            default_severity="CRITICAL",
            url="https://cwe.mitre.org/data/definitions/676.html",
            remediation="Remove `unsafe fn` declarations; isolate unsafe foreign function interfaces (FFI) behind strictly validated, safe RAII wrapper structs.",
        ),
        "CWE-703": CWEDefinition(
            cwe_id="CWE-703",
            name="Improper Check or Handling of Exceptional Conditions",
            description="The software does not properly anticipate or handle exceptional conditions that may arise during execution.",
            category="Error Handling & Logic",
            default_severity="MEDIUM",
            url="https://cwe.mitre.org/data/definitions/703.html",
            remediation="Implement comprehensive `Result<T, E>` error propagation and handle all possible failure variants without resorting to process-aborting panics.",
        ),
    }

    # Detection Key to CWE Mapping
    DETECTION_MAP: Dict[str, str] = {
        "unsafe_scope": "CWE-676",
        "unsafe_block": "CWE-119",
        "unsafe_operation": "CWE-119",
        "raw_pointer": "CWE-476",
        "clone_hotspot": "CWE-400",
        "clone_in_loop": "CWE-400",
        "heap_allocation": "CWE-400",
        "loop_allocation": "CWE-770",
        "complexity_high": "CWE-710",
        "complexity_moderate": "CWE-710",
        "statement_density": "CWE-710",
        "length_exceeded": "CWE-710",
        "param_count": "CWE-710",
        "unwrap_panic": "CWE-252",
        "unchecked_index": "CWE-129",
        "defensive_boundary": "CWE-119",
        "loop_backedge": "CWE-1075",
        "use_after_free": "CWE-416",
    }

    @classmethod
    def get_definition(cls, cwe_id: str) -> Optional[CWEDefinition]:
        return cls.CATALOG.get(cwe_id)

    @classmethod
    def get(cls, cwe_id: str) -> Optional[CWEDefinition]:
        return cls.get_definition(cwe_id)

    @classmethod
    def create_tag(
        cls,
        cwe_id: str,
        line_number: Optional[int] = None,
        statement_code: Optional[str] = None,
        message: Optional[str] = None,
        severity: Optional[str] = None,
        remediation: Optional[str] = None,
    ) -> CWETag:
        definition = cls.CATALOG.get(cwe_id)
        if not definition:
            # Fallback for generic/unrecognized CWE
            return CWETag(
                cwe_id=cwe_id,
                name="Security Weakness",
                severity=severity or "MEDIUM",
                category="General Quality",
                url=f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html",
                line_number=line_number,
                statement_code=statement_code,
                message=message or f"Detected potential issue associated with {cwe_id}",
                remediation=remediation or "Review code against Rust idioms.",
            )

        return CWETag(
            cwe_id=definition.cwe_id,
            name=definition.name,
            severity=severity or definition.default_severity,
            category=definition.category,
            url=definition.url,
            line_number=line_number,
            statement_code=statement_code,
            message=message or definition.description,
            remediation=remediation or definition.remediation,
        )

    @classmethod
    def tag_from_detection(
        cls,
        detection_key: str,
        line_number: Optional[int] = None,
        statement_code: Optional[str] = None,
        custom_message: Optional[str] = None,
        severity_override: Optional[str] = None,
    ) -> CWETag:
        cwe_id = cls.DETECTION_MAP.get(detection_key, "CWE-710")
        return cls.create_tag(
            cwe_id=cwe_id,
            line_number=line_number,
            statement_code=statement_code,
            message=custom_message,
            severity=severity_override,
        )
