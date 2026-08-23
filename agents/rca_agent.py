"""
RCA Agent.

Per Blueprint Section 4.1: takes the correlated alarm plus
historical/knowledge context, outputs ranked root-cause hypotheses.
Reuses the existing NOC RAG Assistant as its reasoning core - not
rebuilt here. rag_lookup() below is a stub standing in for that call;
swapping it for the real NOC RAG Assistant API is a later, separate
integration step, not something to fake further in this session.
"""


def rag_lookup(incident: dict) -> list[str]:
    """
    Stub for the NOC RAG Assistant call. Real version would query the
    vector DB for similar past incidents/vendor docs. Returns a
    couple of plausible context snippets for the demo scenario only.
    """
    if incident["vendor"] == "Ciena" and incident["ring"] == "Ring 2":
        return [
            "Ciena 6500 LOS-P on a working span, not at a gateway node, "
            "historically correlates with a physical fibre cut rather than "
            "a card or port failure.",
            "Past ticket history for Ring 2 shows HERS protection restores "
            "service within seconds for single-span cuts when the "
            "protection path itself is healthy.",
        ]
    return ["No closely matching historical context found for this incident."]


def analyse(incident: dict) -> dict:
    context = rag_lookup(incident)

    # v1: simple rule-of-thumb ranking, not a real LLM call yet.
    # Good enough for the Ring 2 demo scenario; a real RCA Agent would
    # rank multiple hypotheses by confidence using the retrieved context.
    if incident["affected_layer"] == "OTN" and incident["vendor"] == "Ciena":
        hypothesis = "Fibre cut on Ring 2 span"
        confidence = 85
    else:
        hypothesis = "Unclassified fault - needs manual investigation"
        confidence = 20

    return {
        "incident_id": incident["incident_id"],
        "top_hypothesis": hypothesis,
        "confidence": confidence,
        "supporting_context": context,
    }


if __name__ == "__main__":
    from alarm_agent import correlate
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent / "mediation"))
    from mapper import normalise_ciena, _load

    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")
    incident = correlate([alarm])[0]

    print(analyse(incident))
