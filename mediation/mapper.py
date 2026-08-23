"""
Mediation / Normalisation Layer.

Implements LLD Section 3.1:
  Step 1 - collect raw data from each vendor's NBI, native format
  Step 2 - map onto common TAPI + OpenConfig-based severity/field model
  Step 3 - publish the normalised model (NormalisedAlarmObject)
  Step 4 - keep a mapping table back to the original vendor-native alarm

Note: "MCP" here is Ciena's Manage/Control/Plan platform, not Model
Context Protocol - the two are unrelated and easy to confuse.
"""

import json
from pathlib import Path

from contracts import NormalisedAlarmObject

FIXTURES = Path(__file__).parent / "fixtures"

# Step 4: mapping table, incident_id -> native alarm reference, for audit
_native_alarm_trace: dict[str, dict] = {}


def _severity_from_huawei(sev: str) -> str:
    return {"CRITICAL": "Critical", "MAJOR": "Major",
            "MINOR": "Minor", "WARNING": "Warning"}.get(sev, "Warning")


def _severity_from_ciena(sev: str) -> str:
    return {"CR": "Critical", "MJ": "Major",
            "MN": "Minor", "WN": "Warning"}.get(sev, "Warning")


def _severity_from_nokia(sev: str) -> str:
    return {"critical": "Critical", "major": "Major",
            "minor": "Minor", "warning": "Warning"}.get(sev, "Warning")


def normalise_huawei(raw: dict, incident_id: str) -> NormalisedAlarmObject:
    obj = NormalisedAlarmObject(
        incident_id=incident_id,
        source_ring="Ring 1",
        source_vendor="Huawei",
        native_alarm_ref=raw["alarmId"],
        severity_normalised=_severity_from_huawei(raw["alarmSeverity"]),
        affected_layer=raw["objectLayer"],
        timestamp=raw["occurTime"],
    )
    _native_alarm_trace[incident_id] = raw
    return obj


def normalise_ciena(raw: dict, incident_id: str) -> NormalisedAlarmObject:
    obj = NormalisedAlarmObject(
        incident_id=incident_id,
        source_ring="Ring 2",
        source_vendor="Ciena",
        native_alarm_ref=raw["eventId"],
        severity_normalised=_severity_from_ciena(raw["severity"]),
        affected_layer=raw["serviceLayer"],
        timestamp=raw["raisedAt"],
    )
    _native_alarm_trace[incident_id] = raw
    return obj


def normalise_nokia(raw: dict, incident_id: str) -> NormalisedAlarmObject:
    obj = NormalisedAlarmObject(
        incident_id=incident_id,
        source_ring="Ring 3",
        source_vendor="Nokia",
        native_alarm_ref=raw["faultId"],
        severity_normalised=_severity_from_nokia(raw["perceivedSeverity"]),
        affected_layer=raw["layerRate"],
        timestamp=raw["timeRaised"],
    )
    _native_alarm_trace[incident_id] = raw
    return obj


def get_native_trace(incident_id: str) -> dict | None:
    """Step 4 lookup - audit trail back to the original vendor alarm."""
    return _native_alarm_trace.get(incident_id)


def _load(fixture_name: str) -> dict:
    return json.loads((FIXTURES / fixture_name).read_text())


if __name__ == "__main__":
    # Quick manual check against all three vendor fixtures.
    huawei_raw = _load("huawei_nce_alarm.json")
    ciena_raw = _load("ciena_mcp_alarm.json")
    nokia_raw = _load("nokia_nsp_alarm.json")

    incidents = [
        normalise_huawei(huawei_raw, "INC-0001"),
        normalise_ciena(ciena_raw, "INC-0002"),   # Ring 2 demo scenario
        normalise_nokia(nokia_raw, "INC-0003"),
    ]

    for inc in incidents:
        print(inc.model_dump_json(indent=2))
        trace = get_native_trace(inc.incident_id)
        note = trace.get("vendorNotes") or trace.get("extra")
        print("native ref ->", note)
        print()
