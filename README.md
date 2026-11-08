# Topology for Geometry and Mathematical Space Classification

An offline Python research toolkit for **finite abstract simplicial complexes**. Computes exact boundary ranks and Betti numbers over GF(2), checks boundary composition and Euler–Poincaré consistency, and recognizes triangulated compact 2-manifolds using edge incidence and vertex links. Connected recognized surfaces receive orientability, boundary-component count, and genus or crosscap classification.

This is a bounded implementation, not a classifier of arbitrary mathematical spaces. Equal Betti numbers do not establish homeomorphism; GF(2) homology omits integral torsion. Disconnected surfaces have no single reported genus. No embedding, geometry reconstruction, physical validation, model API, or external execution is performed.

## Run end to end

Python 3.10+; standard-library runtime, no API keys.

```sh
python -m pip install .
mkdir -p runs
geometry-topology analyze examples/sphere.json --requirements examples/requirements.json --output runs/sphere
geometry-topology verify runs/sphere
geometry-topology compare runs/sphere runs/sphere
python -m unittest discover -s tests -v
python tests/check_installed.py
```

Open `runs/sphere/review.html` for an escaped static review. A bundle contains the captured complex, requirements, report, HTML, and byte/hash manifest. Verification recomputes all files and rejects altered results even when the manifest is rehashed. This establishes consistency with this engine, not source authenticity or independent scientific reproduction. Output directories are created exclusively; existing results are never overwritten. Verification is version-specific.

CLI exit codes: **0** checks satisfied, **1** encoded requirements failed, **2** invalid input, invalid bundle, or I/O error. A consistent FAIL bundle remains FAIL on verification.

## Input contract

`schema_version: 1`, nonempty `name` (≤200 characters), and `simplices`: 1–512 nonempty vertex lists. A simplex has 1–4 distinct string vertex IDs (≤64 characters each). At most 128 vertices and 4096 simplices after downward closure. Generators may include redundant faces. Coordinates and ordering have no geometric meaning. Requirements explicitly specify four expected Betti numbers or null, and booleans `require_surface` and `require_orientable`.

## Verification and research status

Tests cover known spaces (disk, sphere, torus, annulus, Möbius strip, 3-sphere), nonmanifold counterexamples, every simple graph on four vertices, all 512 three-column GF(2) rank cases, strict parsing, replay, tampering, escaped HTML, and CLI behavior. CI installs the package and exercises its entry point outside the source tree on Python 3.10, 3.12, and 3.13. Only the synthetic sphere bundle is uploaded, retained for seven days. No scheduled triggers are added.

- [Mathematical scope and curriculum](docs/METHODS.md)
- [ResearchOS / TECT concept paper](docs/researchos/TECT_WHITE_PAPER.md)
- [ResearchOS integration status](docs/researchos/INTEGRATION.md)
- [Machine-readable integration manifest](docs/researchos/integration.json)

The ResearchOS paper defines a proposed cross-domain assurance architecture. This repository implements a domain validator and reproducible local evidence bundle; it does not implement all TECT lifecycle, identity, governance, or independent-evaluation services. Performance objectives in the paper remain research targets.

License: original Apache-2.0 license retained.
