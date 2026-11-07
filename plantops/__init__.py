"""PlantOps Agent, sample demo package.

Sample data only. No live building, irrigation, vendor, or payment
connections. See docs/plantops-demo-spec.md for the locked scope.
"""

from .data import (
    CARE_LOG,
    IRRIGATION,
    PLANTS,
    WEATHER,
    get_care_log,
    get_irrigation,
    get_register,
    get_weather,
)
from .triage import propose_work_order
from .work_order import WorkOrder, approve, decline, log_outcome, mark_work_done, verify

__all__ = [
    "CARE_LOG",
    "IRRIGATION",
    "PLANTS",
    "WEATHER",
    "WorkOrder",
    "approve",
    "decline",
    "get_care_log",
    "get_irrigation",
    "get_register",
    "get_weather",
    "log_outcome",
    "mark_work_done",
    "propose_work_order",
    "verify",
]
