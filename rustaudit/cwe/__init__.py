"""
CWE (Common Weakness Enumeration) Identification Tagging Subsystem for RustAuditAI.
Provides standardized security weakness classification, severity indexing, and MITRE catalog mappings.
"""

from .registry import CWEDefinition, CWETag, CWERegistry

__all__ = ["CWEDefinition", "CWETag", "CWERegistry"]
