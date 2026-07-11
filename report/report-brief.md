# START HERE — Context brief for writing the portfolio report

You are helping write the **portfolio report** for the TU Wien course
*Knowledge Graphs* (VU 192.116, 2026S). This document gives you everything you
need. Read it fully before writing.

**Your job:** turn `main.tex` (a clean, minimal LaTeX skeleton with prose and
real numbers already in place — plain `article` class, Times, no custom design)
into the final report. Improve wording, expand where thin, keep it concise, and
make sure every claimed learning outcome (LO) has an explicit inline `(LOx)`
tag. Keep the plain style — do **not** add colour, custom macros or heavy
formatting. Do **not** invent numbers; every figure you need is in this brief or
in `main.tex`. Where a figure/screenshot is needed, leave the `% TODO ...`
marker — those are produced outside this chat.

---

## 1. Project in one paragraph

*A Temporal Football Knowledge Graph for Tactical Pattern Discovery and Team
Style Comparison.* We build a temporal knowledge graph (Neo4j property graph)
from StatsBomb open football event data (Premier League 2015/16), formalise
three tactical patterns as graph queries **and** recursive Datalog rules,
materialise the matches back into the graph as derived knowledge, and use them
to compare the playing styles of all 20 teams through an interactive Streamlit
dashboard. A PyKEEN embedding experiment complements the symbolic pipeline.
Team: **Tim Greß (12412672), Jan Tölken (12432831)**, mode **6 ECTS**.

## 2. Required structure (from the official "Portfolio Example Structure" PDF)

The report follows this structure 1:1 (already reflected in `main.tex`):

1. **Scenario** (≤1 page) — 1.1 domain, 1.2 the service
2. **KG Construction** — 2.1 datasets, 2.2 technologies/architecture, 2.3 how
   the KG was constructed (with 3 concrete mapping examples)
3. **ML-based Representation** — the embeddings; how they evolve the KG; limits
4. **Logic-based Representation** — patterns as rules (5 examples, ≥1 recursive,
   ≥1 creating objects); how they evolve the KG; limits
5. **Reflection** (≤1.5 pages) — 5.1 service outcome, 5.2 data-model comparison,
   5.3 connections between KGs/ML/AI

**Hard submission rules:**
- Final PDF filename must end in **`-structured.pdf`**.
- Include the filled **cover pages** (pro forma) before the report — brief
  formulations are in `cover-pages-notes.md`.
- ZIP with code+data, folders named **`2 - construction`**, **`3 - ML`**,
  **`4 - logic`**, **`5 - reflection`**, each with a `readme.md`.

## 3. LO strategy — we claim exactly 10, no slack

Every claimed LO needs an explicit inline `(LOx)` tag in the report text.

| LO | Claim | Where in report |
|----|-------|-----------------|
| LO1 KG embeddings | basic | §3.1 |
| LO2 logical knowledge, recursion, object creation | basic (+ possible exceed) | §4.1 |
| LO3 GNNs | **excluded** (allowed) | — |
| LO4 compare data models | basic | §5.2 |
| LO5 architecture | basic | §2.2 |
| LO6 scalable reasoning | basic | §3.3, §4.3 |
| **LO7 create a KG** (schema mapping) | **EXCEED** | §2.3 |
| LO8 evolve a KG (completion + derived) | basic | §3.2, §4.2 |
| LO9 real-world applications | basic | §1.1 |
| LO10 financial KGs | **excluded** (allowed) | — |
| **LO11 provide services** | **EXCEED** | §1.2, §5.1 |
| LO12 KG↔ML↔AI connections | basic | §5.3 |

Grade logic: ≥10 LOs at basic + exceed in ≥2 = grade 1. Our two exceeds are
**LO7** (complete documented schema design + mapping + verification) and
**LO11** (systematic 20-team style comparison + interactive dashboard). LO2
(Datalog depth) is a spare exceed candidate.

**Lecturer calibration (important):** the LO list is "to guide your thinking,
not a checklist". Many LOs are fine at one honest paragraph (LO4, LO5, LO6,
LO8, LO9, LO12). Do not pad. Bad empirical results don't hurt if the LO is
demonstrated. Keep the writing succinct — the structure PDF repeatedly says
"succinctly".

## 4. All the hard numbers (do not invent others)

**KG contents** (verified 1:1 against source JSON):
- 380 matches, **1,313,773 events**, 71,884 possessions, 644 players, 20 teams,
  9 zones.
- **33 distinct StatsBomb event types.** Top: Pass 368,619 (28.1%), Ball
  Receipt* 340,314 (25.9%), Carry 276,949 (21.1%), Pressure 115,402 (8.8%),
  Ball Recovery 40,943, Duel 32,290, Clearance 21,645, Block 14,839, Dribble
  13,721, Goal Keeper 11,777, Miscontrol 10,786, Dispossessed 10,520, Shot
  9,908, Foul Committed 9,512, Foul Won 9,112, Interception 8,920, Dribbled
  Past 8,771, then admin types (Substitution, Half Start/End, Starting XI,
  Tactical Shift, 50/50, Shield, Referee Ball-Drop, Bad Behaviour, Error,
  Player Off/On, Offside, Own Goal For/Against).
- 15 of the 33 types get a subtype label (Pass, Shot, Carry, Pressure, Ball
  Receipt*, Ball Recovery, Interception, Duel, Dribble, Clearance, Block,
  Dispossessed, Foul Committed, Foul Won, Goal Keeper); the other 18 stay
  plain `:Event` nodes (schema-evolution point for LO8).

**Pattern instances** (materialised as `:PatternInstance` nodes):
- **P1 Pressing Regain: 9,121** · **P2 Fast Transition: 979** · **P3 Wide
  Build-Up: 6,998**.
- Parameters: P1 minX=60, Δt=5s, ≤10 NEXT hops; P2 shot within 15s and ≥30
  units forward progress from own half; P3 ≥3 wide-middle-third events then
  wide final-third entry, Regular Play only.

**Validation vs StatsBomb's own signals:**
- P2 vs `From Counter` label: 30.5% of P2 are so labelled vs a **1.8% base
  rate** (~17× enrichment); 69.7% of From-Counter possessions with a shot are
  captured.
- P1 vs `counterpress` flag: 39.6% vs 36.9% baseline (weak — expected;
  different anchor semantics; report honestly).
- High-press success (P1 regains / high presses): Tottenham 23.0%, Man City
  22.7%, Leicester 21.3%, Liverpool 21.2%, … league average **19.6%**.
- Directness metric: **Leicester #1 at 0.052 vs 0.038** for the next team
  (they were the counter-attacking champions this exact season).

**Datalog cross-validation (LO2):** the Soufflé/DuckDB recursive rules
reproduce the Cypher counts **exactly** — 9,121 = 9,121 and 979 = 979, per
match, zero deviations.

**LO6 performance:** after PROFILE analysis, single-property `match_id`
indexes + one `USING INDEX` hint made P1 **4×**, P2 **4×**, P3 **13×** faster
at identical results. (Earlier war story: a subtype-label lookup bypassed the
`:Event(event_id)` unique index → quadratic slowdown, fixed → ~5,000 events/s.)

**Embeddings (LO1/LO8/LO12):** 9,300 triples, 596 entities, 4 relations
(plays_for 561, plays_position 2,179, passes_to 5,774, exhibits_pattern 786),
dim 64, 150 epochs, 80/10/10, filtered eval:

| Model | MRR | Hits@1 | Hits@3 | Hits@10 |
|-------|-----|--------|--------|---------|
| TransE | 0.255 | 0.021 | 0.394 | 0.721 |
| ComplEx | 0.265 | 0.120 | 0.334 | 0.553 |

TransE's near-zero Hits@1 = classic 1-to-N weakness. LO12 cross-check:
nearest embedding neighbour shares the Phase-4 style cluster for **9/20 teams
(ComplEx)** vs a **~4/20 random baseline** (TransE 5/20 ≈ chance).

## 5. What each attached file is

- `main.tex` — the clean report skeleton to finish. **Primary working file.**
- `schema.md` — full KG schema + the data-model comparison table (LO4/LO7).
- `patterns.md` — the formal P1/P2/P3 definitions and metric definitions.
- `handover.md` — running notes / all results with commands.
- `courseaims.txt` — the authoritative LO definitions (quote wording from here).
- `KG - Portfolio - Example-Structure.pdf` — the structure this report follows.

The **cover pages** (pro forma) are filled separately, not by this chat; use the
LO strategy table in Section 3 above for the per-LO one-liners and the
basic/exceed ticks.

## 6. Still to be produced OUTSIDE this chat (leave TODO markers)

- Architecture diagram (Fig. 1).
- 1–2 dashboard screenshots + the style-metric table as a figure.
- 5 concrete embedding examples + one true-positive and one false-positive
  link prediction (a small script generates these).
- Cover pages filled with real page numbers (after final compile), hours,
  reuse declaration.
- StatsBomb attribution logo in data figures.

## 7. Tone

Academic but concise; the structure PDF says "succinctly" everywhere.
Reflection ≤1.5 pages, Scenario ≤1 page. Prefer one honest paragraph over
padding. Tag every claimed LO inline.
