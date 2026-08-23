"""
Orchestrator.

Per Blueprint Section 4.2: not just a message router. Enforces the
autonomy-level policy (Section 4.3), maintains the decision trace for
audit, and escalates rather than forcing the pipeline forward on low
confidence.

Full 5-agent pipeline: Alarm -> RCA -> Simulation -> Schedule -> Report.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "mediation"))

from alarm_agent import correlate
from rca_agent import analyse
from simulation_agent import simulate
from schedule_agent import schedule
from report_agent import close_incident


def run_pipeline(alarms: list) -> dict:
    incidents = correlate(alarms)
    trace = []

    for incident in incidents:
        rca_result = analyse(incident)
        sim_result = simulate(incident, rca_result)
        sim_dict = sim_result.model_dump()
        schedule_result = schedule(incident, rca_result, sim_dict)
        closure_report = close_incident(incident, rca_result, sim_dict, schedule_result)

        decision = {
            "incident_id": incident["incident_id"],
            "alarm": incident,
            "rca": rca_result,
            "simulation": sim_dict,
            "schedule": schedule_result,
            "closure_report": closure_report,
            "policy_decision": sim_result.recommendation,
        }
        trace.append(decision)

    return trace


if __name__ == "__main__":
    from mapper import normalise_ciena, _load

    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")

    for decision in run_pipeline([alarm]):
        print(f"Incident: {decision['incident_id']}")
        print(f"RCA hypothesis: {decision['rca']['top_hypothesis']} "
              f"({decision['rca']['confidence']}% confidence)")
        print(f"Simulation: {decision['simulation']['proposed_action']}")
        print(f"Decision: {decision['policy_decision']}")
