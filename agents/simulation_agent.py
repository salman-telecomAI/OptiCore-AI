"""
Digital Twin / Simulation Agent.

Per Blueprint Section 4.1: takes the proposed remediation from RCA
Agent, outputs predicted impact, blast radius, confidence score - the
safety gate before anything touches production.

v1 scope (Blueprint v2.0 Section 2): Layer 0 not built (future work).
Layer 1 (Batfish) and Layer 3 (Suzieq) mocked, not wired to real
tools yet. Layer 2 (ContainerLab) mocked as a JSON-style result, not
a live container run. This matches the locked v1 build scope - real
Batfish/ContainerLab/Suzieq integration is a v1.1 follow-up.

Logic follows the LLD Section 5 worked example: check local HERS
protection first, only simulate a cross-ring reroute via GW 2<->3 if
HERS looks degraded or capacity-constrained.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "mediation"))
from contracts import SimulationResultObject


def check_local_protection(incident: dict) -> dict:
    """
    Mocked Layer 2 (Topology/Emulation) check. Real version would run
    this against ContainerLab. For the Ring 2 demo scenario, HERS is
    healthy - hardcoded here since there's no live twin yet.
    """
    if incident["ring"] == "Ring 2":
        return {"protection_scheme": "HERS", "healthy": True, "restores_service": True}
    return {"protection_scheme": "unknown", "healthy": False, "restores_service": False}


def simulate_cross_ring_reroute(incident: dict) -> dict:
    """
    Mocked cross-ring reroute simulation via the relevant gateway node.
    Only called when local protection isn't enough on its own.
    """
    return {
        "path": "GW 2<->3 into Ring 3",
        "feasible": True,
        "added_blast_radius": "Ring 3 gateway node capacity",
    }


def simulate(incident: dict, rca_result: dict) -> SimulationResultObject:
    local = check_local_protection(incident)

    if local["healthy"] and local["restores_service"]:
        proposed_action = f"Activate {local['protection_scheme']} protection"
        blast_radius = "Single span, local ring only"
        cross_domain = False
        layers_validated = [1, 2]
    else:
        reroute = simulate_cross_ring_reroute(incident)
        proposed_action = f"Reroute via {reroute['path']}"
        blast_radius = f"Local span plus {reroute['added_blast_radius']}"
        cross_domain = True
        layers_validated = [1, 2, 3]

    # Confidence carried over from RCA hypothesis for v1 - a real
    # Simulation Agent would compute its own score from the twin run,
    # not just reuse the RCA confidence, but this is enough for the
    # Ring 2 demo path.
    confidence_score = rca_result["confidence"]

    recommendation = "Auto-proceed" if confidence_score >= CONFIDENCE_THRESHOLD else "Escalate to human"

    return SimulationResultObject(
        proposed_action=proposed_action,
        confidence_score=confidence_score,
        blast_radius=blast_radius,
        layers_validated=layers_validated,
        cross_domain=cross_domain,
        recommendation=recommendation,
    )


# L2->L3 autonomy policy threshold (Blueprint Section 4.3 / 6).
# 80 chosen because it matches/exceeds the confidence level of a
# well-understood, previously-seen fault pattern (the Ring 2 case
# below scores 85) - not an arbitrary round number.
CONFIDENCE_THRESHOLD = 80


if __name__ == "__main__":
    from alarm_agent import correlate
    from rca_agent import analyse
    from mapper import normalise_ciena, _load

    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")
    incident = correlate([alarm])[0]
    rca_result = analyse(incident)

    result = simulate(incident, rca_result)
    print(result.model_dump_json(indent=2))
