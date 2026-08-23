"""
Schedule Agent.

Per Blueprint Section 4.1: takes the validated remediation and
confidence score, outputs a change window and technician/resource
assignment.

Per LLD Section 5 Step 5: even when protection (HERS/MS-SPRing/SNCP)
auto-restores service, a physical fault like a fibre cut still needs
a technician dispatched to actually fix it - the protection switch
buys time, it doesn't repair anything.
"""


def needs_physical_repair(rca_result: dict) -> bool:
    return "fibre cut" in rca_result["top_hypothesis"].lower() or \
           "cut" in rca_result["top_hypothesis"].lower()


def schedule(incident: dict, rca_result: dict, sim_result: dict) -> dict:
    physical_repair_needed = needs_physical_repair(rca_result)

    if sim_result["recommendation"] == "Auto-proceed":
        change_window = "Immediate - protection already restoring service"
    else:
        change_window = "Next available maintenance window - pending human approval"

    return {
        "incident_id": incident["incident_id"],
        "change_window": change_window,
        "technician_dispatch_required": physical_repair_needed,
        "dispatch_reason": "physical fibre repair needed alongside protection switch"
                            if physical_repair_needed else None,
        "auto_proceeded": sim_result["recommendation"] == "Auto-proceed",
    }


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent / "mediation"))
    from alarm_agent import correlate
    from rca_agent import analyse
    from simulation_agent import simulate
    from mapper import normalise_ciena, _load

    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")
    incident = correlate([alarm])[0]
    rca_result = analyse(incident)
    sim_result = simulate(incident, rca_result).model_dump()

    print(schedule(incident, rca_result, sim_result))
