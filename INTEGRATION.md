## Integrating This clingo Fork Into Another Python Repo

This repository is a fork of clingo with non-upstream changes. If you need the **Python API** (`import clingo`) but
cannot distribute wheels (publicly or privately) and must support **macOS (local dev)** and **Linux (containers/CI)**,
the most reliable pattern is to **vendor the fork and build/install it from source** into the Python environment used by
your app.

### Constraints Assumed

- You must use the Python API (not just calling the `clingo` binary).
- You will not publish wheels to any package index (including private indexes).
- You need macOS support for local development.
- CI runs on GitHub and must use this fork.
- Deployment runs on Modal via a container image (Linux).

### Recommended Strategy (Source Build + Install, Pinned by Submodule)

**Summary**

- Vendor the fork in your target repo (prefer `git submodule` so you can pin a commit).
- Build the Python extension with CMake using the *same Python interpreter* as your app environment.
- `cmake --install` into that environment (venv on macOS/CI; system prefix in containers).
- Ensure your app never accidentally imports upstream/system `clingo`.

This is intentionally “boring”: no wheel hosting, no VCS `pip install`, no runtime `PYTHONPATH` hacks.

---

## Step-by-Step: Adopt In A Target Repo

### 1) Vendor the fork

In the target repo:

```sh
git submodule add <GIT_URL_TO_THIS_FORK> vendor/clingo
git submodule update --init --recursive
```

Pin updates by updating the submodule commit and committing the target repo change.

If your org prefers not to use submodules, `git subtree` also works (same build steps; different update workflow).

### 2) Add a single “build vendor clingo” command

The target repo should have one blessed command (Make task or script) that:

1. Configures CMake for the vendored clingo.
2. Builds the Python module.
3. Installs it into the active Python environment.

The critical rule is: **the Python used at runtime must match `Python_EXECUTABLE` used for the build+install**.

#### Example (venv local dev / CI)

Run inside an activated venv:

```sh
python -c 'import sys; print(sys.executable)'
```

Then:

```sh
PYTHON="$(python -c 'import sys; print(sys.executable)')"
VENV_PREFIX="$(python -c 'import sys, pathlib; print(pathlib.Path(sys.executable).resolve().parents[1])')"

cmake -S vendor/clingo -B build/vendor-clingo \
  -DPython_EXECUTABLE="$PYTHON" \
  -DCMAKE_BUILD_TYPE=Release \
  -DPYCLINGO_INSTALL=prefix \
  -DCMAKE_INSTALL_PREFIX="$VENV_PREFIX"

cmake --build build/vendor-clingo -j 8
cmake --install build/vendor-clingo
```

Notes:

- `PYCLINGO_INSTALL=prefix` installs into the Python site-packages under `CMAKE_INSTALL_PREFIX`.
- For a venv, `CMAKE_INSTALL_PREFIX` should be the venv root (the parent of `bin/python`).

#### Example (Linux container image)

In a Dockerfile you typically install into `/usr/local`:

```sh
cmake -S vendor/clingo -B /tmp/build/vendor-clingo \
  -DPython_EXECUTABLE=/usr/bin/python3 \
  -DCMAKE_BUILD_TYPE=Release \
  -DPYCLINGO_INSTALL=prefix \
  -DCMAKE_INSTALL_PREFIX=/usr/local

cmake --build /tmp/build/vendor-clingo -j "$(nproc)"
cmake --install /tmp/build/vendor-clingo
```

### 3) Ensure the app imports the vendored clingo

Avoid installing upstream `clingo` into your app environment.

Add a small sanity check in your app (or tests) that fails if the wrong module is imported:

```python
import clingo
path = getattr(clingo, "__file__", "")
assert path, "clingo import produced no __file__"
```

Recommended: assert `path` points into your venv or container prefix you control (not system locations you don’t).

### 4) GitHub Actions CI (macOS + Linux)

Run the same build+install step in CI and cache the build directory:

- Cache key should include:
  - OS
  - Python version
  - clingo submodule commit
  - CMake build type/options

At minimum, cache `build/vendor-clingo/` and restore it before building.

### 5) Modal deployment (container)

Build the fork into the image during image build, then install your app.

High-level order in the Dockerfile:

1. Install toolchain deps (CMake, compiler, Python headers).
2. Copy `vendor/clingo` (or `git submodule update --init --recursive` in build context).
3. Build+install clingo Python bindings into the image Python.
4. Install your app and run.

---

## Operational Tradeoffs (Why This Pattern)

- **Pros**
  - No wheel hosting required.
  - Exact fork version pinned by submodule commit.
  - Works on macOS and Linux containers with consistent semantics.
  - Uses the normal Python import path (`import clingo`) once installed.

- **Cons**
  - You must maintain build toolchains in dev/CI/container.
  - Builds can be slow without caching.
  - Cross-platform issues (rpath / SDK / Python minor versions) must be handled in your scripts.

---

## Troubleshooting Checklist

- `import clingo` fails:
  - Confirm you built with the same Python you run: compare `Python_EXECUTABLE` vs `sys.executable`.
  - Confirm install prefix: venv root for local; `/usr/local` (or similar) for containers.
  - Confirm the extension exists in site-packages under `clingo/` (e.g., `_clingo*.so` / `_clingo*.dylib`).

- Wrong clingo imported:
  - Ensure upstream `clingo` is not installed in the environment.
  - Print `clingo.__file__` and verify it’s under your controlled prefix.

- Builds are too slow in CI:
  - Cache the CMake build directory.
  - Reduce matrix (pin Python minor versions) if possible.
