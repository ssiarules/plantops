"""Triage logic, plain language, sample data only.

Order: flagged condition first, then weather risk, then irrigation
fault, then overdue care. Proposes only the top item.
"""

from .data import get_care_log, get_irrigation, get_register, get_weather
from .work_order import APPROVAL_PROMPT, WorkOrder


def propose_work_order():
    """Propose WO-SAMPLE-001 for the top flagged plant, or None."""
    plants = get_register()
    flagged = [plant for plant in plants if plant["flagged"]]
    if not flagged:
        return None, []
    # Longest overdue first among flagged plants; S-02 is the demo top item.
    top = sorted(flagged, key=lambda p: p["overdue"], reverse=True)[0]

    weather = get_weather()
    dry_days = [day for day in weather if "no rain" in day["note"]]
    rain_day = next((day["day"] for day in weather if "rain possible" in day["note"]), None)
    weather_reason = f"Weather: hot and dry for the next {len(dry_days)} days"
    weather_reason += f", do not wait for {rain_day} rain." if rain_day else "."

    zone = next(z for z in get_irrigation() if top["id"] in z["zone"])
    zone_name = zone["zone"].split(",")[0]
    irrigation_reason = f"Irrigation: {zone_name} last run {zone['last_run']}, {zone['status']}"

    history = [e for e in get_care_log() if e["entry"].startswith(top["id"])]
    care_reason = "Care log: " + " Then ".join(f"{e['date']}, {e['entry']}" for e in history)

    reasons = [
        f"Register: {top['id']}, {top['location']}, {top['condition']}, {top['next_care']}.",
        weather_reason,
        irrigation_reason,
        care_reason,
    ]
    order = WorkOrder(
        order_id="WO-SAMPLE-001",
        site="Sample Building 1",
        plant_id=top["id"],
        action="Check Zone B low flow, water S-02 manually, recheck soil in 24 hours.",
        reasons=reasons,
    )
    return order, reasons


def proposal_message(order, reasons):
    """Build the chat proposal message, ending with the approval prompt."""
    lines = [
        f"Proposed work order {order.order_id}, {order.site}, plant {order.plant_id}.",
        f"Action: {order.action}",
        "Why:",
    ]
    lines.extend(f"- {reason}" for reason in reasons)
    lines.append("What this is not: not a schedule change, not a vendor dispatch, not a payment.")
    lines.append(APPROVAL_PROMPT)
    return "\n".join(lines)


def check_inputs():
    """Return all four sample inputs, for tests and for the demo script."""
    return {
        "register": get_register(),
        "weather": get_weather(),
        "irrigation": get_irrigation(),
        "care_log": get_care_log(),
    }
