# Testing Local Clingo Python Extension

This guide explains how to test your locally built Clingo Python extension during development.

## Quick Start

1. **Build the project** with Python support:
   ```bash
   mkdir build && cd build
   cmake .. -DCLINGO_BUILD_WITH_PYTHON=ON
   make -j$(nproc)
   cd ..
   ```

2. **Run the test setup**:
   ```bash
   # Option 1: Source the script to set up your environment
   source test_local_clingo.sh
   python3 -c "import clingo; print('Success!')"

   # Option 2: Run commands through the script
   ./test_local_clingo.sh python3 test_clingo.py
   ```

## How It Works

The setup uses two key components:

### 1. Environment Variables
- **PYTHONPATH**: Points to the built Python extension and wrapper files
- **DYLD_LIBRARY_PATH** (macOS): Points to the built libclingo shared library

### 2. File Structure
```
build/bin/
├── libclingo.dylib              # Built shared library
└── python/
    ├── _clingo.*.so            # Built Python extension
    └── clingo -> ../../libpyclingo/clingo/  # Symlink to Python wrapper
```

## Testing Your Changes

### Basic Functionality Test
```bash
source test_local_clingo.sh
python3 test_clingo.py
```

### Interactive Testing
```bash
source test_local_clingo.sh
python3
>>> import clingo
>>> ctl = clingo.Control()
>>> ctl.add("base", [], "a :- not b. b :- not a.")
>>> ctl.ground([("base", [])])
>>> with ctl.solve(yield_=True) as handle:
...     for model in handle:
...         print([str(atom) for atom in model.symbols(shown=True)])
```

### Running Existing Tests
```bash
source test_local_clingo.sh
cd libpyclingo
python3 -m unittest discover clingo/tests/
```

## Files Created

- `test_local_clingo.sh`: Setup script for environment variables
- `test_clingo.py`: Comprehensive test of the local extension
- `debug_clingo_location.py`: Debug script to verify library locations
- `build/bin/python/clingo`: Symlink to Python wrapper files

## Troubleshooting

### Import Errors
If you get import errors, check:
1. The extension was built: `ls build/bin/python/_clingo*.so`
2. The shared library exists: `ls build/bin/libclingo.dylib`
3. Environment variables are set: `echo $PYTHONPATH`

### Wrong Library Being Used
Use the debug script to verify:
```bash
source test_local_clingo.sh
python3 debug_clingo_location.py
```

### Library Loading Errors
On macOS, you might need to ensure the library can be found:
```bash
export DYLD_FALLBACK_LIBRARY_PATH="$PWD/build/bin:$DYLD_FALLBACK_LIBRARY_PATH"
```

## Development Workflow

1. Make changes to C++ code in `libclingo/src/`
2. Rebuild: `make -C build`
3. Test changes: `source test_local_clingo.sh && python3 your_test.py`

Note: the grounding `timeout` parameter is a deterministic grounding budget (in thousands of queue items), not seconds.
