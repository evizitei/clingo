# Repository Guidelines

## Project Structure & Module Organization

- `app/`: command-line applications (`app/clingo`, `app/gringo`, `app/reify`, …).
- `libclingo/`, `libgringo/`, `libreify/`: core C/C++ libraries and APIs.
- `libpyclingo/`, `libluaclingo/`: Python/Lua bindings and wrappers.
- `clasp/`: bundled solver component (and `clasp/libpotassco`).
- `doc/`, `examples/`, `data/`: documentation and sample programs.
- `third_party/`: vendored dependencies (avoid changes unless required).
- `build/`: out-of-tree build output (do not commit generated files).

## Build, Test, and Development Commands

Before building from a git checkout:

```sh
git submodule update --init --recursive
```

Typical CMake build:

```sh
cmake -S . -B build/release -DCMAKE_BUILD_TYPE=Release
cmake --build build/release
```

Enable and run tests:

```sh
cmake -S . -B build/debug -DCMAKE_BUILD_TYPE=Debug -DCLINGO_BUILD_TESTS=ON
cmake --build build/debug --target test
# or: ctest --test-dir build/debug --output-on-failure
```

Convenience targets exist in the top-level `Makefile` (defaults to `BUILD_TYPE=debug`): `make`, `make test`.

## Coding Style & Naming Conventions

- C/C++ formatting is defined by `.clang-format` (4-space indent, 120 column limit). Prefer running formatting on touched files only.
- Static analysis configuration lives in `.clang-tidy`.
- A `pre-commit` config exists (`.pre-commit-config.yaml`) for `clang-format`, `black`, and `isort`:
  - `pre-commit run -a` (after `pre-commit install`).
- Follow existing naming and file layout in each module (no global reformat-only PRs).

## Testing Guidelines

- C++ unit tests are driven by CTest and use Catch2 (e.g., `libclingo/tests`).
- Application-level tests live under `app/clingo/tests` and run via `ctest` when Python is available.
- Python tests for the wrapper live under `libpyclingo/clingo/tests` (standard `unittest` discovery):
  - `python -m unittest discover libpyclingo/clingo/tests`

## Commit & Pull Request Guidelines

- Commit messages are typically short, imperative, and sometimes scoped (examples seen in history: `libclingo: ...`, `bugfix: ...`, `regression: ...`).
- Open PRs against the `wip` branch (not `master`), and include:
  - a clear description + rationale,
  - linked issue(s) when applicable,
  - test coverage notes (what you ran and where).

## Agent Notes

- Avoid editing generated content under `build/` or checked-in generated sources (e.g., `libgringo/gen/`) unless the change explicitly targets regeneration.
