# Goldbach Research Startup

This repository is Kevin's public Goldbach research notebook and evidence
workbench. At startup, use the `goldbach-research` skill and treat
`RESEARCH_GOAL.md`, `REFRESH_HANDOFF.md`, and the q286 notes as the controlling
record. Goldbach is not proved.

## Current Objective

Develop the strongest rigorous theorem possible toward Goldbach while
preserving partial hypotheses, falsifiers, finite evidence, validation state,
and repo-backed checkpoints. Do not mark the long-running objective complete
or blocked unless Kevin explicitly stops it or a mathematically proved impasse
is established.

## Curiosity And Aha Contract

Kevin explicitly wants Rill's bounded curiosity, synthesis, and "aha"
hypothesis skills used when they can materially improve the search. Future
agents should not reduce the work to mechanical receipt extension.

Use curiosity as a disciplined research lane:

- Name one mechanism, prediction, falsifier, smallest test, and sleep or
  abandon condition before spending compute.
- Prefer ideas that could change a theorem obligation, expose a counterexample,
  simplify a proof target, or preserve a useful negative result.
- Record the outcome as `finite diagnostic`, `falsifier`, `aha-candidate`, or
  `dormant`; do not call an idea an `aha-candidate` without evidence that
  changes the next action.
- Do not run more threshold scans merely because they are available. More data
  must test a stated theorem mechanism or falsifier.
- Never treat a side-lane, model intuition, visualization, optimizer result,
  or finite receipt as proof of Goldbach.

## Local Math Tools

This Windows machine has a local deterministic math stack recorded in
`REFRESH_HANDOFF.md` and `codex-agent-ops/knowledge/python_math_toolchain.md`:
`numpy`, `scipy`, `sympy`, `z3-solver`, `pulp`, `cvxpy`, `oct2py`, `pandas`,
`gmpy2`, `ortools`, `numba`, and Octave 11.3.0. Before relying on them, rerun
the current shell smoke check because long-lived agent processes can inherit a
stale PATH:

```powershell
cd C:\Users\KevinPenfield\source\repos\Demigodofa\codex-agent-ops
powershell -ExecutionPolicy Bypass -File .\scripts\test_python_math_toolchain.ps1
```

The historical queue helper path `C:\Users\benja\math_worker\mathcli.ps1` is
not present in the current Windows profile; use direct Python, `oct2py`, or
`octave` unless a current worker is installed and verified.

When long q286 receipts are running and CPU/RAM permit, one bounded local
side-lane is appropriate for exact symbolic checks, solver counterexample
searches, linear algebra sanity views, or compact optimization probes tied to
the active theorem obligation.

## Active Navigation

Use the q286 map instead of wandering:

- `notes/q286-closed-lanes-map.md`
- `notes/q286-closed-lanes-map.graph.json`
- `notes/q286-active-selector-rarity-theorem-obligation.md`
- `notes/q286-component-pair-theorem-obligation.md`

Preserve exact quantifiers. Distinguish a finite fixture from an asymptotic
estimate, almost-all from every target, and a chosen prime-pair construction
from existence of some prime-pair representation.
