"""
Alarm Agent.

Per Blueprint Section 4.1: takes the normalised, de-duplicated,
correlated alarm object as its output. Input here is whatever the
mediation layer already normalised (see mediation/mapper.py) - this
agent's job is correlation, not translation, so it doesn't touch
vendor-native formats at all.

For v1, "correlation" is deliberately simple: alarms on the same ring
within a short time window get grouped into one incident. A real
version would also correlate across rings via the mediation layer's
gateway-node awareness (LLD Section 3.2) - out of scope for now.
"""

import sys
from pathlib import Path
from datetime import timedelta

sys.path.append(str(Path(__file__).parent.parent / "mediation"))

from contracts import NormalisedAlarmObject

CORRELATION_WINDOW = timedelta(seconds=30)


def correlate(alarms: list[NormalisedAlarmObject]) -> dict:
    """
    Groups alarms from the same ring that occurred within the
    correlation window into a single incident. Returns the incident
    as a plain dict since it's Alarm Agent -> RCA Agent internal
    state, not one of the two locked data contracts.
    """
    if not alarms:
        raise ValueError("no alarms to correlate")

    by_ring: dict[str, list[NormalisedAlarmObject]] = {}
    for a in alarms:
        by_ring.setdefault(a.source_ring, []).append(a)

    incidents = []
    for ring, ring_alarms in by_ring.items():
        ring_alarms.sort(key=lambda a: a.timestamp)
        group = [ring_alarms[0]]
        for a in ring_alarms[1:]:
            if a.timestamp - group[-1].timestamp <= CORRELATION_WINDOW:
                group.append(a)
            else:
                incidents.append(_build_incident(group))
                group = [a]
        incidents.append(_build_incident(group))

    return incidents


def _build_incident(group: list[NormalisedAlarmObject]) -> dict:
    severities = ["Critical", "Major", "Minor", "Warning"]
    worst = min(group, key=lambda a: severities.index(a.severity_normalised))
    return {
        "incident_id": worst.incident_id,
        "ring": worst.source_ring,
        "vendor": worst.source_vendor,
        "highest_severity": worst.severity_normalised,
        "affected_layer": worst.affected_layer,
        "alarm_count": len(group),
        "first_seen": min(a.timestamp for a in group),
        "member_alarms": [a.native_alarm_ref for a in group],
    }


if __name__ == "__main__":
    from mapper import normalise_ciena, _load

    # Ring 2 demo scenario - Ciena fibre cut, single alarm for now.
    ciena_raw = _load("ciena_mcp_alarm.json")
    alarm = normalise_ciena(ciena_raw, "INC-0002")

    for incident in correlate([alarm]):
        print(incident)
