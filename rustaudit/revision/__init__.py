"""
Intra-procedural Code Revision & Patch Control Package (SRS §4.6.7).
Provides persistent revision tracking, historical snapshots, and rollback functionality.
"""

from .manager import RevisionManager, CodeRevision, get_revision_manager

__all__ = ["RevisionManager", "CodeRevision", "get_revision_manager"]
