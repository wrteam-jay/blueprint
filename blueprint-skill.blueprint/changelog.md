# Changelog

## 2.0 — 2026-03-04

**Tier 3 (Authoritative).** Requirements expanded from 12 to 30 with verified sources and testability criteria. All 7 scenarios deepened with comprehensive error paths. Stories verified — every story has a delivering scenario.

**Requirements expanded:**
- Added requirements from resolved decisions (DEC-8 through DEC-14): one blueprint per system, extensible panel, active staleness detection, current version only, adaptive approach, writing philosophy, solo developer workflow
- Added cross-reference consistency requirements (actors ↔ scenarios, entities ↔ scenarios, stories ↔ scenarios)
- Added contradiction handling, audit integrity, and approach/writing quality requirements
- Every requirement now has a named source (decision or skill constraint) and a testability statement

**Scenarios deepened:**
- Elicit: added multi-session handling, cross-phase contradiction detection, verification checkpoint rejection, implementation drift redirect
- Distill: updated for solo-developer workflow (DEC-14), added implicit impossible states, scattered business logic, permanent workarounds, large codebase handling
- Review: added fundamental problem escalation, systematic implementation leakage, stale content detection
- Audit: added systematic issue grouping, scope mismatch detection, tier mismatch, dependent findings
- Propose: removed multi-blueprint reference (DEC-8), added purpose-changing proposals, terminology introduction, requirement conflicts, bug-report redirect
- Update: added staleness-triggered updates, multiple simultaneous changes, cascade detection, mini-distillation fallback
- Scaffold: added scope validation, content-creation redirect

**Section statuses:** All sections now Complete or Active. Blueprint promoted to Tier 3.

---

## 1.1 — 2026-03-04

**Open questions resolved.** All 6 initial open questions walked through with spec owner and resolved into decisions (DEC-8 through DEC-14).

**Resolved:**
- Q-1 → DEC-8: One blueprint per system (no cross-blueprint conflicts)
- Q-2 → DEC-9: Panel is extensible (9 defaults, users can add more)
- Q-3 → DEC-10: Active staleness detection (skill checks, surfaces major issues to owner)
- Q-4 → DEC-11: Document current version only (history lives in git)
- Q-5 → DEC-12: Adaptive documentation approach (top-down default, adapts to context)
- Q-5 (granularity) → DEC-13: Writing philosophy (dual representation, respect reader, invisible things matter)
- Q-6 → DEC-14: Author as Domain Expert in solo workflows

**Decision Log:** 7 → 14 decisions.
**Open Questions:** 6 → 0.

---

## 1.0 — 2026-03-04

**Initial distillation.** Blueprint created by distilling the blueprint skill's own codebase (14 files across root skill, 7 sub-skills, 5 references, and 1 shared module).

**Sections completed:**
- Context (Complete) — problem statement validated with spec owner
- Scope (Complete) — in-scope, adjacent, and out-of-scope defined
- Actors & Roles (Complete) — five actors identified: Spec Author, Spec Owner, Blueprint Reader, Domain Expert, Panellist
- Terminology (Complete) — 17 terms defined
- User Stories (Draft) — 14 stories across four categories
- Scenarios (Draft) — 7 scenarios covering all sub-skills
- Domain Model (Draft) — 8 entities with states, invariants, and relationships
- Requirements (Draft) — 12 requirements with sources and tests
- Decision Log (Active) — 7 decisions with rationale
- Open Questions (Active) — 6 questions with owners
- Changelog (Active) — this entry

**Tier:** 2 (Workable) — enough for implementation discussions. Requirements need source verification and testability review for Tier 3.

**Method:** Distillation (code reading + spec owner consultation). Sources: all 14 skill files read; context statement validated directly with spec owner.
