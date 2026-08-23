# OptiCore AI

Working repo for my Digital Twin / multi-agent network ops project. Still early days, updating this as I go instead of writing a big README upfront.

## Where things stand

All 5 agents are wired up now and running end to end on the Ring 2 fibre-cut scenario. Mediation layer normalises the three vendor formats, alarm agent correlates, RCA agent hypothesizes, simulation agent checks HERS protection and decides auto-proceed vs escalate, schedule agent works out the change window and whether a technician still needs dispatching (turns out yes, even when protection kicks in automatically, since someone still has to go fix the actual fibre), and report agent closes it all out into one audit trace.

Also got a basic FastAPI endpoint running now, hitting /incidents/ring2-demo returns the whole incident trace as JSON. Tested it locally with curl, works.

twin and frontend are still empty.

## Folder layout

- mediation/ - vendor normalisation (contracts.py, fixtures, mapper.py)
- agents/ - all 5 agents plus orchestrator.py which wires them together
- api/ - main.py, the FastAPI app
- twin/, frontend/ - not started yet

## Running it
- twin/, frontend/ - not started yet

## Running it

pip install pydantic fastapi uvicorn
cd agents
python orchestrator.py


Or to hit it as an actual API:

cd api
uvicorn main:app --reload

then open http://127.0.0.1:8000/incidents/ring2-demo

## Next

Frontend to actually show this visually instead of raw JSON, then Docker and deployment. Confidence threshold is set at 80 for now, chose it because it's just under the 85 the Ring 2 case scores, wanted something defensible rather than a round number.

Same as before: edit README on GitHub, paste this over, commit with your own short message.

Session 4 done — full 5-agent pipeline working end-to-end with a real API on top. Ready for Session 5 (Frontend + Docker + Railway deploy) whenever you want to continue.

Schedule agent
PY 
Report agent
PY 
Orchestrator
PY 
Main
PY 

check for step 4 point#1

This is exactly right — all 5 expected changes are showing:

agents\orchestrator.py — modified (yellow icon), diff shows old 3-agent wiring being replaced with the new 5-agent line, confirmed correct
agents\report_agent.py — new (green +)
agents\schedule_agent.py — new (green +)
api\.gitkeep — deleted (red −), which is expected and fine, since it's being replaced by a real file
api\main.py — new (green +)

This matches Step 4/5 from the instructions exactly. Nothing looks wrong here — proceed:

Type your commit message in the Summary box, something like:
schedule and report agents, wired up the api
Click Commit 5 files to main
Then click Push origin (will appear top-right after committing)

Go ahead — this is good to commit as-is.

Got it — from now on I'll give you both fields explicitly, split out, whenever there's a commit to make.

For the commit you're about to do right now:

Summary:

schedule and report agents, wired up the api

Description:

report agent closes out the full trace now, schedule agent handles change window plus technician dispatch. added a basic fastapi endpoint on top, tested it locally with curl and it returns the whole incident trace as json.

Go ahead and paste those into their respective boxes, then Commit 5 files to main → Push origin.

pushed the origin.. now ?

Session 4 is fully pushed. Here's the README update for this session — same voice, split as summary/description since that's the new standard going forward.

Where you paste this: GitHub → README.md → pencil icon → select all → paste this content:

markdown
# OptiCore AI

Working repo for my Digital Twin / multi-agent network ops project. Still early days, updating this as I go instead of writing a big README upfront.

## Where things stand

All 5 agents are wired up now and running end to end on the Ring 2 fibre-cut scenario. Mediation layer normalises the three vendor formats, alarm agent correlates, RCA agent hypothesizes, simulation agent checks HERS protection and decides auto-proceed vs escalate, schedule agent works out the change window and whether a technician still needs dispatching (turns out yes, even when protection kicks in automatically, since someone still has to go fix the actual fibre), and report agent closes it all out into one audit trace.

Also got a basic FastAPI endpoint running now, hitting /incidents/ring2-demo returns the whole incident trace as JSON. Tested it locally with curl, works.

twin and frontend are still empty.

## Folder layout

- mediation/ - vendor normalisation (contracts.py, fixtures, mapper.py)
- agents/ - all 5 agents plus orchestrator.py which wires them together
- api/ - main.py, the FastAPI app
- twin/, frontend/ - not started yet

## Running it

pip install pydantic fastapi uvicorn
cd agents
python orchestrator.py


Or to hit it as an actual API:

cd api
uvicorn main:app --reload

then open http://127.0.0.1:8000/incidents/ring2-demo

## Next

Frontend to actually show this visually instead of raw JSON, then Docker and deployment. Confidence threshold is set at 80 for now, chose it because it's just under the 85 the Ring 2 case scores, wanted something defensible rather than a round number.
