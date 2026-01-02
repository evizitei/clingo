# Clingo: A grounder and solver for logic programs

## Important: this is a private fork (not upstream)

This repository is **not** the main clingo repository and these changes are **not intended to be merged upstream**.

Upstream clingo 6 is expected to have proper async grounding capabilities (see
https://github.com/potassco/clingo/pull/580) based on the original discussion in
https://github.com/potassco/clingo/issues/570.

This fork is purely a hack to allow **interrupting grounding in clingo 5.x** via a deterministic “compute budget”.
If you need to wire this fork into a separate Python project for local/CI/container use, start with `INTEGRATION.md`.

Clingo is part of the [Potassco](https://potassco.org) project for *Answer Set
Programming* (ASP).  ASP offers a simple and powerful modeling language to
describe combinatorial problems as *logic programs*.  The *clingo* system then
takes such a logic program and computes *answer sets* representing solutions to
the given problem.  To get an idea, check our [Getting
Started](https://potassco.org/doc/start/) page and the [online
version](https://potassco.org/clingo/run/) of clingo.

Please consult the following resources for further information:

  - [**Downloading source and binary releases**](https://github.com/potassco/clingo/releases)
  - [**Installation and software requirements**](INSTALL.md)
  - [**Contributing**](CONTRIBUTING.md)
  - [Changes between releases](CHANGES.md)
  - [Documentation](https://github.com/potassco/guide/releases)
  - [Potassco clingo page](https://potassco.org/clingo/)

Clingo is distributed under the [MIT License](LICENSE.md).
