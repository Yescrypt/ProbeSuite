#!/usr/bin/env python3
"""
ProBeSuite - Scanning Module
Network scanning and enumeration tools
"""

__version__ = "2.0"
__author__ = "ProbeSuite Team"

# Import main scanner classes
try:
    from scanning.active.active_menu import ActiveScanner, main as active_main
    from scanning.passive.passive_menu import PassiveScanner, main as passive_main
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from active.active_menu import ActiveScanner, main as active_main
    from passive.passive_menu import PassiveScanner, main as passive_main

__all__ = [
    'ActiveScanner',
    'PassiveScanner',
    'active_main',
    'passive_main'
]