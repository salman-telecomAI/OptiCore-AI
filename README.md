# OptiCore AI — Session 1

Just my working notes for now, not a proper README yet. Will clean this up once more of the pipeline is actually built.

## What's in here

`/mediation` is the only real folder right now — vendor normalisation layer, took the whole first session. Everything else (`/agents`, `/twin`, `/api`, `/frontend`) is empty on purpose, they're for later sessions.

Inside mediation:
- `contracts.py` has the two data objects (NormalisedAlarmObject and SimulationResultObject), field names copied straight from my LLD doc so I don't drift from the spec while coding.
- `fixtures/` has three fake alarms, one per vendor (Huawei, Ciena, Nokia) — the Ciena one is the actual scenario I'm building the whole demo around, a fibre cut on Ring 2.
- `mapper.py` takes all three vendor formats and turns them into one common shape. Ran it locally, output looked right.

## Next up

Alarm + RCA agents. Haven't started those yet.

TODO: still need to decide the exact confidence-score threshold for the L2→L3 escalation logic — not going to just make one up, want a number I can actually defend if someone asks about it.
