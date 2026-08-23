# OptiCore AI

A small multi-agent system for network operations, built while I move from 20 years in DWDM/OTN transmission engineering into AI architecture. This is my second AI project, after an earlier RAG assistant for NOC troubleshooting, and my first one that actually takes autonomous action instead of just answering questions.

**Live demo:** https://opticore-ai-production.up.railway.app/ui

## What it does

Five agents, one orchestrator, one job each. An alarm comes in from a vendor system, gets correlated into an incident, investigated for root cause, checked against a mocked digital twin before anything is recommended, scheduled if it needs a technician, and closed out with a full audit trail. All the steps I used to do manually at 2am during an outage.

The scenario it's built around is a fibre cut on a 3 ring network, one ring each on Huawei, Ciena, and Nokia gear. That's deliberate. A single vendor demo doesn't prove much, real networks are messier than that.

## How it's put together

mediation/ - normalises Huawei NCE, Ciena MCP, and Nokia NSP alarm formats into one shape
agents/ - alarm, rca, simulation, schedule, report agents, plus the orchestrator
api/ - fastapi app, serves the json endpoint and the dashboard
frontend/ - the dashboard itself, plain html and js, no framework
twin/ - empty for now, see limitations below


Quick note since it trips people up: MCP shows up twice in this repo meaning two different things. Ciena MCP is their Manage, Control, Plan platform. Model Context Protocol is the AI industry standard for connecting agents to tools. Completely unrelated, just an unfortunate naming collision.

## Running it locally

pip install pydantic fastapi uvicorn
cd agents
python orchestrator.py


Or as an actual API:
cd api
uvicorn main:app --reload


Then open `http://127.0.0.1:8000/ui`

## What's real and what's mocked

Being upfront about this rather than letting it look more finished than it is:

- Alarm correlation, RCA reasoning, the orchestrator's auto-proceed/escalate decision, and the full audit trail are all real logic, tested end to end.
- The RCA agent's RAG lookup is currently a stub with hardcoded context. Wiring it to my actual NOC RAG Assistant is next.
- The digital twin's topology/emulation layer is a mocked JSON result, not a live ContainerLab run. That's a v1.1 follow up, not a blocker for now.
- The physical/optical layer (OSNR, impairments) isn't built at all yet, it's documented as future work.
- The confidence threshold for auto-proceed vs escalate is hardcoded at 80. I picked that because it sits just under the 85 the demo scenario scores, wanted something I could actually defend rather than a round number.
- Only tested against the one Ring 2 scenario so far, not the full topology.

## Hosting

Running on Railway right now using the free trial credit, which is fine for a personal project but isn't meant to be permanent. If it ever goes quiet, it's because the credit ran out, not because the project's abandoned. Render's free tier is the fallback if that happens, same Dockerfile, one line change.

## Where this is going

Wiring the real RAG assistant into the RCA agent, then a real ContainerLab run for the emulation layer. No fixed timeline, this is something I chip away at alongside work.

---

TODO: the schedule agent's technician dispatch logic only checks for "fibre cut" as a keyword in the RCA hypothesis right now, which is a bit brittle. Works for this scenario, would need generalising before a second scenario gets added.
