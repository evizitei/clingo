#!/usr/bin/env python3
"""
Test script to verify that the locally built Clingo Python extension works correctly.
This script tests basic functionality and verifies we're using the local build.
"""

import sys
import os

def test_clingo_import():
    """Test that we can import clingo successfully."""
    print("Testing Clingo import...")
    try:
        import clingo
        print("✓ Successfully imported clingo")
        return True
    except ImportError as e:
        print(f"✗ Failed to import clingo: {e}")
        return False

def test_clingo_version():
    """Test getting Clingo version information."""
    print("\nTesting Clingo version...")
    try:
        import clingo
        print(f"✓ Clingo version: {clingo.version()}")
        return True
    except Exception as e:
        print(f"✗ Failed to get version: {e}")
        return False

def test_basic_functionality():
    """Test basic Clingo functionality."""
    print("\nTesting basic functionality...")
    try:
        import clingo

        # Ensure we are testing the locally built extension (it adds the timeout argument).
        try:
            import _clingo  # pylint: disable=import-error
            if 'build/bin/python' not in _clingo.__file__:
                print("✗ Not using locally built extension; run via './test_local_clingo.sh python3 test_clingo.py'")
                return False
        except Exception as e:
            print(f"✗ Could not verify local extension: {e}")
            return False

        # Create a control object
        ctl = clingo.Control()
        print("✓ Created Control object")

        # Add a simple program
        ctl.add("base", [], "a :- not b. b :- not a.")
        print("✓ Added program")

        # Ground the program
        ctl.ground([("base", [])], timeout=0.0)
        print("✓ Grounded program")

        # add and ground impossible program
        ctl.add("impossible", [], """nat(0). nat(S) :- nat(P), S = P + 1.""")
        try:
            # timeout is a deterministic grounding budget (in thousands of queue items)
            ctl.ground([("impossible", [])], timeout=0.001)
        except RuntimeError as e:
            # Check if this is specifically a GroundingInterrupt exception
            if "Grounding budget exceeded" in str(e):
                print("✓ Grounding budget exceeded exception caught as expected")
                return True
            else:
                print(f"✗ Unexpected RuntimeError: {e}")
                raise e

        # Solve and collect models
        models = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                models.append([str(atom) for atom in model.symbols(shown=True)])

        print(f"✓ Found {len(models)} models: {models}")
        return False

    except Exception as e:
        print(f"✗ Failed basic functionality test: {e}")
        return False

def test_library_location():
    """Test that we're using the expected library location."""
    print("\nChecking library location...")
    try:
        # Try to get the actual _clingo module location
        import _clingo
        ext_file = _clingo.__file__
        print(f"✓ Using extension from: {ext_file}")

        # Check if it's our local build
        if 'build/bin/python' in ext_file:
            print("✓ Confirmed: Using locally built extension")
            return True
        else:
            print("⚠ Warning: Not using locally built extension")
            return False
    except ImportError:
        try:
            import clingo._internal
            # Fallback to checking the lib object
            ext_file = str(clingo._internal._lib)
            print(f"✓ Using extension (lib object): {ext_file}")
            print("✓ Successfully loaded local clingo extension")
            return True
        except Exception as e:
            print(f"✗ Could not determine library location: {e}")
            return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing locally built Clingo Python extension")
    print("=" * 60)

    tests = [
        test_clingo_import,
        test_clingo_version,
        test_library_location,
        test_basic_functionality,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your local Clingo build is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
