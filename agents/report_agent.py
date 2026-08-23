"""
Report Agent.

Per Blueprint Section 4.1: takes the full incident trace across all
agents, outputs closure report, audit log, KPI update.

Per LLD Section 5 Step 6: original alarms, RCA reasoning, simulated
options considered, decision taken, and outcome - vendor-tagged.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).parent.parent / "mediation"))
from mapper import get_native_trace


def close_incident(incident: dict, rca_result: dict, sim_result: dict,
                    schedule_result: dict) -> dict:
    native = get_native_trace(incident["incident_id"])

    return {
        "incident_id": incident["incident_id"],
        "closed_at": datetime.now(timezone.utc).isoformat(),
        "vendor": incident["vendor"],
        "ring": incident["ring"],
        "native_alarm_ref": native.get("vendorNotes") or native.get("extra") if native else None,
        "rca_reasoning": {
            "hypothesis": rca_result["top_hypothesis"],
            "confidence": rca_result["confidence"],
            "supporting_context": rca_result["supporting_context"],
        },
        "simulation_considered": {
            "proposed_action": sim_result["proposed_action"],
            "blast_radius": sim_result["blast_radius"],
            "cross_domain": sim_result["cross_domain"],
            "layers_validated": sim_result["layers_validated"],
        },
        "decision": sim_result["recommendation"],
        "outcome": {
            "change_window": schedule_result["change_window"],
            "technician_dispatched": schedule_result["technician_dispatch_required"],
        },
    }


if __name__ == "__main__":
    from alarm_agent import correlate
    from rca_agent import analyse
    from simulation_agent import simulate
    from schedule_agent import schedule
    from mapper import normalise_ciena, _load

    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")
    incident = correlate([alarm])[0]
    rca_result = analyse(incident)
    sim_result = simulate(incident, rca_result).model_dump()
    schedule_result = schedule(incident, rca_result, sim_result)

    import json
    print(json.dumps(close_incident(incident, rca_result, sim_result, schedule_result),
                      indent=2, default=str))
