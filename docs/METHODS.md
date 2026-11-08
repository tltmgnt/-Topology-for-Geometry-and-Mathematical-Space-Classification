# Methods, limits, and implementation curriculum

## Exact algebra

Close each supplied simplex under nonempty faces. Order cells lexicographically within each dimension. The GF(2) boundary matrix has a 1 for each codimension-one face. Integer bit vectors and XOR elimination compute exact matrix ranks, without floating-point tolerances.

For dimension d, `b_d = n_d - rank(boundary_d) - rank(boundary_(d+1))`. Every boundary composition is checked to vanish. Alternating cell and Betti sums must agree. These are implementation invariants, not evidence that the captured complex represents an external space faithfully.

## Surface recognition

Recognition requires dimension exactly two, every edge incident to one or two triangles, and every vertex link a connected cycle (interior) or path (boundary). Isolated vertices, dangling edges, pinched vertices and higher-dimensional simplices prevent recognition. Orientation constraints propagate across shared edges. A conflict means nonorientability. Boundary components are components of the boundary-edge graph.

For a connected recognized compact triangulated surface, the classification theorem determines its family from orientability, boundary count b and Euler characteristic chi: orientable genus g=(2-b-chi)/2, or nonorientable crosscaps k=2-b-chi. This restricted use does not extend classification to arbitrary complexes. See Allen Hatcher, *Algebraic Topology*, §2.1 (simplicial homology): https://pi.math.cornell.edu/~hatcher/AT/ATpage.html .

## ResearchOS adapter boundary

The report is domain validation evidence, identified by captured input and requirement hashes. PASS is the conjunction of explicitly requested combinatorial checks. A generated assertion still needs claim registration, provenance authentication, externally independent reproduction, scoped adversarial evaluation, governance and review before any broader assurance promotion. Local deterministic replay is useful for integrity, but it is not independent reproduction. No clinical, financial, equipment, or deployment authorization follows from this tool.

## Six-week curriculum

| Week | Topic | Exercise | Evidence of learning |
|---|---|---|---|
| 1 | Abstract complexes and closure | Encode point, circle, disk, sphere | Explain why edges alone do not fill a triangle |
| 2 | Chain groups and boundary operators | Derive boundary matrices by hand | Verify boundary squared is zero |
| 3 | GF(2) linear algebra and homology | Compute circle and sphere ranks | Reconcile Betti and Euler counts |
| 4 | Manifolds, links, and orientability | Compare annulus and Möbius triangulations | Same GF(2) Betti numbers, different orientability |
| 5 | Reproducibility and attacks | Alter a report and recompute its manifest | Explain why replay rejects it and why hashes do not authenticate origin |
| 6 | Epistemic control and experiment design | Propose an assertion and validation policy | Separate model correctness, representation fidelity, and external validity |

Capstone: create a new synthetic complex, state expected invariants before running analysis, produce and verify the bundle, introduce a genuine counterexample, and document what would require external evidence. Proposed extensions include integral homology, persistent homology, per-component surface classification, certified proof exports, and TECT event-ledger integration. They are not implemented here.
