# Topology compatibility and curriculum v2 — -Topology-for-Geometry-and-Mathematical-Space-Classification

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | specialized mathematical tool |
| Minimum useful mathematics | Finite simplicial homology over GF(2) and combinatorial surface recognition |
| Relationships to preserve | Downward closure, boundary maps, vertex links and edge incidence |
| Concrete operation / capstone | Compare disk, sphere, torus and a nonmanifold; verify boundary composition and Euler–Poincare consistency |
| Necessity and scope boundary | Equal Betti numbers do not prove homeomorphism; GF(2) omits integral torsion and disconnected surfaces have no single genus |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with finite simplicial homology over gf(2) and combinatorial surface recognition and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify downward closure, boundary maps, vertex links and edge incidence. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain finite simplicial homology over gf(2) and combinatorial surface recognition. | Compare disk, sphere, torus and a nonmanifold; verify boundary composition and Euler–Poincare consistency. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

The table is a guided selection of source lines, not an assertion that the whole repository is covered. Line numbers refer to the inspected source blob `2dd9ae7e97ef0bec26cb37976f919f4dcd4d850f` in [geometry_topology/analysis.py](../../geometry_topology/analysis.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [7](../../geometry_topology/analysis.py#L7) | `def canonical(value):` | State the input/output contract and trace one normal and one failing case. |
| [8](../../geometry_topology/analysis.py#L8) | `return (json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2) + '\n').encode()` | Predict the returned value and distinguish a computed result from authorization. |
| [11](../../geometry_topology/analysis.py#L11) | `def rank(columns):` | State the input/output contract and trace one normal and one failing case. |
| [22](../../geometry_topology/analysis.py#L22) | `return len(pivots)` | Predict the returned value and distinguish a computed result from authorization. |
| [25](../../geometry_topology/analysis.py#L25) | `def components(vertices, edges):` | State the input/output contract and trace one normal and one failing case. |
| [41](../../geometry_topology/analysis.py#L41) | `return result` | Predict the returned value and distinguish a computed result from authorization. |
| [44](../../geometry_topology/analysis.py#L44) | `def parse_complex(value):` | State the input/output contract and trace one normal and one failing case. |
| [45](../../geometry_topology/analysis.py#L45) | `if not isinstance(value, dict) or set(value) != {'schema_version', 'name', 'simplices'} or type(value['schema_version']) is not int or value['schema_version'] != 1:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [46](../../geometry_topology/analysis.py#L46) | `raise ValueError('expected schema_version 1, name, simplices')` | Construct the triggering input and explain why rejection preserves the contract. |
| [48](../../geometry_topology/analysis.py#L48) | `raise ValueError('bounded nonempty name required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [51](../../geometry_topology/analysis.py#L51) | `raise ValueError('require 1..512 generating simplices')` | Construct the triggering input and explain why rejection preserves the contract. |
| [55](../../geometry_topology/analysis.py#L55) | `raise ValueError('simplex must have 1..4 vertices (dimension <=3)')` | Construct the triggering input and explain why rejection preserves the contract. |
| [57](../../geometry_topology/analysis.py#L57) | `raise ValueError('distinct bounded vertex identifiers required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [63](../../geometry_topology/analysis.py#L63) | `raise ValueError('closure exceeds 4096 simplices')` | Construct the triggering input and explain why rejection preserves the contract. |
| [66](../../geometry_topology/analysis.py#L66) | `raise ValueError('at most 128 vertices')` | Construct the triggering input and explain why rejection preserves the contract. |
| [67](../../geometry_topology/analysis.py#L67) | `return levels` | Predict the returned value and distinguish a computed result from authorization. |
| [70](../../geometry_topology/analysis.py#L70) | `def boundary(levels, dimension):` | State the input/output contract and trace one normal and one failing case. |
| [72](../../geometry_topology/analysis.py#L72) | `return [0] * len(levels[0])` | Predict the returned value and distinguish a computed result from authorization. |
| [74](../../geometry_topology/analysis.py#L74) | `return [sum(1 << index[face] for face in combinations(cell, dimension)) for cell in levels[dimension]]` | Predict the returned value and distinguish a computed result from authorization. |
| [77](../../geometry_topology/analysis.py#L77) | `def surface_info(levels):` | State the input/output contract and trace one normal and one failing case. |
| [80](../../geometry_topology/analysis.py#L80) | `return {'recognized': False, 'reason': 'requires a pure two-dimensional complex'}` | Predict the returned value and distinguish a computed result from authorization. |
| [86](../../geometry_topology/analysis.py#L86) | `return {'recognized': False, 'reason': 'edge incidence is not one or two'}` | Predict the returned value and distinguish a computed result from authorization. |
| [93](../../geometry_topology/analysis.py#L93) | `return {'recognized': False, 'reason': 'vertex link is empty or disconnected'}` | Predict the returned value and distinguish a computed result from authorization. |
| [97](../../geometry_topology/analysis.py#L97) | `return {'recognized': False, 'reason': 'vertex link is not a path or cycle'}` | Predict the returned value and distinguish a computed result from authorization. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_geometry.py](../../tests/test_geometry.py)
- [tests/test_researchos.py](../../tests/test_researchos.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. Equal Betti numbers do not prove homeomorphism; GF(2) omits integral torsion and disconnected surfaces have no single genus.
