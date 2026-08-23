# OptiCore AI

Working repo for my Digital Twin / multi-agent network ops project. Still early days, updating this as I go instead of writing a big README upfront.

## Where things stand

Mediation layer is done. It takes alarms from three different vendor formats (Huawei, Ciena, Nokia, all fake/synthetic for now) and turns them into one common shape. Tested it against a Ciena fibre-cut scenario on Ring 2, which is what most of this repo is built around right now.

On top of that, alarm correlation and root cause agents are working too. Alarm agent groups related alarms into one incident, then RCA agent picks that up and returns a hypothesis. Right now it's hardcoded logic plus a stub for the real RAG lookup, not a live LLM call yet. Ran both end to end on the Ring 2 case and got a sensible answer out.

twin, api and frontend folders are still empty. That's next.

## Folder layout

- mediation/ - vendor normalisation (contracts.py, fixtures, mapper.py)
- agents/ - alarm_agent.py and rca_agent.py live here now
- twin/, api/, frontend/ - not started yet

## Running it
