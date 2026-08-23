"""
FastAPI layer.

Wraps the orchestrator pipeline in HTTP endpoints. v1 only exposes
the Ring 2 demo scenario - a real version would accept arbitrary
incoming vendor alarms, not just replay one fixture.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "agents"))
sys.path.append(str(Path(__file__).parent.parent / "mediation"))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from orchestrator import run_pipeline
from mapper import normalise_ciena, _load

app = FastAPI(title="OptiCore AI - v1 demo API")


@app.get("/")
def root():
    return {"status": "ok", "demo_endpoint": "/incidents/ring2-demo", "ui": "/ui"}


@app.get("/incidents/ring2-demo")
def ring2_demo():
    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")
    trace = run_pipeline([alarm])
    return trace


frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=frontend_dir, html=True), name="ui")
