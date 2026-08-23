# OptiCore AI — Session 1 scaffold

Working notes only. This is not the public-facing README — that gets
rewritten by hand at the end (Docs + Humanization session). Do not
polish this file further with AI.

## Layout
- `/agents` — Alarm, RCA, Simulation, Schedule, Report agents + Orchestrator (later sessions)
- `/mediation` — vendor normalisation layer (this session)
- `/twin` — Batfish/ContainerLab/Suzieq integration (later sessions)
- `/api` — FastAPI endpoints (later session)
- `/frontend` — minimal single-page UI (later session)

## What's built so far (Session 1)
- `mediation/contracts.py` — NormalisedAlarmObject, SimulationResultObject
  (field names verbatim from LLD Section 6)
- `mediation/fixtures/` — synthetic Huawei NCE, Ciena MCP, Nokia NSP alarms
  - `ciena_mcp_alarm.json` is the Ring 2 fibre-cut demo scenario (LLD Section 5)
- `mediation/mapper.py` — Steps 1-4 of the mediation layer (LLD 3.1):
  collect native → map to common severity/field model → produce
  NormalisedAlarmObject → keep native trace for audit

Run it: `cd mediation && python3 mapper.py`

## Not built yet
- Alarm/RCA/Simulation/Schedule/Report agents, Orchestrator, twin layers,
  API, frontend, Docker, deploy — all in later sessions.
- Layer 0 (physical/optical) is documented future work per Blueprint v1.0,
  not built at all.
