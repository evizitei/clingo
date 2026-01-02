#!/usr/bin/env python3
"""
Debug script to check where Clingo is being loaded from
"""

import sys
import os

def debug_import_location():
    print("Python sys.path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    print()

    print("PYTHONPATH environment:")
    pythonpath = os.environ.get('PYTHONPATH', '')
    if pythonpath:
        for path in pythonpath.split(':'):
            print(f"  {path}")
    else:
        print("  (not set)")
    print()

    print("DYLD_LIBRARY_PATH environment:")
    dyld_path = os.environ.get('DYLD_LIBRARY_PATH', '')
    if dyld_path:
        for path in dyld_path.split(':'):
            print(f"  {path}")
    else:
        print("  (not set)")
    print()

    try:
        import clingo
        print(f"Clingo module file: {clingo.__file__}")
        print(f"Clingo package: {clingo}")

        # Try to find the _clingo module
        import clingo._internal
        print(f"Internal module: {clingo._internal}")

        if hasattr(clingo._internal, '_lib'):
            lib = clingo._internal._lib
            print(f"Library object: {lib}")
            if hasattr(lib, '__file__'):
                print(f"Library file: {lib.__file__}")

        # Try to check the actual _clingo module
        try:
            import _clingo
            print(f"_clingo module: {_clingo}")
            print(f"_clingo file: {_clingo.__file__}")
        except ImportError as e:
            print(f"Could not import _clingo directly: {e}")

    except Exception as e:
        print(f"Error during import debugging: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_import_location()