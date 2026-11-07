"""Worker checklist, photo step, and suggestions, sample data only.

Third view: the worker on site, in the same room. Runs only after a
manager Approve. Suggestions are next checks and care steps, not a
diagnosis. No payment, no vendor dispatch, no schedule change.
"""

from .data import get_register

WORKER = "sample-crew"

CHECKS = [
    "Soil: finger test, dry, moist, or wet, and depth.",
    "Leaves: drooping, yellowing, spots, sticky residue, or normal.",
    "Drainage: standing water, damp tray, or dry tray.",
    "Pot and roots: pot size, drainage holes clear or blocked, roots visible or not.",
    "Irrigation: Zone B flow, low, normal, or off, and any leak.",
    "Photo: take one clear photo of the plant and one of the soil surface, upload both in the room, or one photo if only one is possible.",
]

# Short plain definitions, no brands, no shopping links.
TOOLS = {
    "moisture finger test": "push one finger about 2 inches into the soil and feel if it is dry, moist, or wet.",
    "watering can": "a can with a spout, so water goes slowly onto the soil, not the leaves.",
    "drainage tray check": "look at the tray under the pot for standing water after watering.",
    "leaf wipe cloth": "a soft damp cloth to wipe leaves gently, top and underside.",
}

# Phrases in the condition note that the manager must hear about in the room.
ESCALATIONS = {
    "spreading": "sticky residue spreading to more plants",
    "yellowing fast": "leaves yellowing fast",
    "standing water": "standing water",
    "leak": "irrigation leak",
    "worse after watering": "plant looks worse after watering",
}

UNREADABLE = (
    "I could not read the photo, so this suggestion is based on the condition note alone. "
    "I am not describing anything in the photo."
)


def _plant(plant_id):
    return next(p for p in get_register() if p["id"] == plant_id)


def checklist_message(order):
    """Assignment tag plus the S-02 checklist, in checklist form."""
    plant = _plant(order.plant_id)
    lines = [
        f"@{WORKER} assigned: {order.order_id}, {order.plant_id}, {plant['location']}, "
        "check Zone B low flow, water manually, recheck soil in 24 hours.",
        "",
        f"Checklist: {order.order_id}, {order.plant_id}, {plant['location']}, {plant['type'].lower()}.",
        f"- Area: {plant['location']}, {order.site}, Zone B.",
        "- Condition on proposal: dry soil, drooping leaves, overdue since Oct 27, 2026, Zone B low flow.",
        "- Checks, in order, tick one by one:",
    ]
    lines.extend(f"  {number}. [ ] {check}" for number, check in enumerate(CHECKS, 1))
    lines.append(
        "- After the checks, post the condition note in this room: "
        "Soil, leaves, drainage, irrigation, photo uploaded yes or no."
    )
    return "\n".join(lines)


def _has(text, phrase):
    """True if phrase appears without "no" or "not" right before it.

    "no standing water" in a condition note is not standing water.
    """
    start = text.find(phrase)
    while start != -1:
        before = text[:start].rstrip().rsplit(" ", 1)[-1].strip(",.")
        if before not in ("no", "not"):
            return True
        start = text.find(phrase, start + 1)
    return False


def escalations(note):
    """Return escalation triggers found in a condition note."""
    text = note.lower()
    return [label for phrase, label in ESCALATIONS.items() if _has(text, phrase)]


def _steps(note):
    """Return (next step, how to steps, tools) for the condition note."""
    text = note.lower()
    standing = _has(text, "standing water")
    dry = _has(text, "dry") and "soil" in text
    steps, tools = [], []
    if standing:
        next_step = "It looks like water is not draining. Do not water now, check drainage and tell the manager."
        steps += [
            "Empty the tray under the pot.",
            "Check the drainage holes are clear.",
            "Recheck the soil in 24 hours before any watering.",
        ]
        tools += ["drainage tray check", "moisture finger test"]
    elif dry:
        next_step = (
            "It looks like drooping leaves with dry soil, water manually and recheck."
            if "droop" in text
            else "It looks like dry soil, water manually and check again in 24 hours."
        )
        steps += [
            "Do the finger test first, and note the depth that is dry.",
            "Water slowly at the soil, not the leaves, until water just reaches the tray.",
            "Wait 10 minutes, then empty any water left in the tray.",
            "Recheck the soil in 24 hours.",
        ]
        tools += ["moisture finger test", "watering can", "drainage tray check"]
    else:
        next_step = "No clear problem in the note. Leave it as is and check again in 24 hours."
        steps += ["Do the finger test again in 24 hours.", "Post a new condition note if anything changes."]
        tools += ["moisture finger test"]
    if _has(text, "sticky"):
        steps += [
            "Sticky residue noted, check leaves top and underside.",
            "Clean gently with a damp cloth if needed, and tell the manager if it spreads.",
        ]
        tools.append("leaf wipe cloth")
    if "low" in text and ("flow" in text or "zone b" in text):
        steps.append("Zone B flow is low. Do not change the irrigation schedule, the manager decides that.")
    return next_step, steps, tools


def suggestion_message(order, note, photo_readable, photo_seen=None):
    """Suggestion reply: next step, how to steps, tool with definition."""
    next_step, steps, tools = _steps(note)
    lines = [f"Suggestions for {order.order_id}, {order.plant_id}. Suggestions only, not a diagnosis."]
    if photo_readable and photo_seen:
        lines.append(f"In the photo: {photo_seen}")
    else:
        lines.append(UNREADABLE)
    lines.append(f"Next: {next_step}")
    lines.append("How to:")
    lines.extend(f"  {number}. {step}" for number, step in enumerate(steps, 1))
    lines.append("Tools:")
    lines.extend(f"- {tool}: {TOOLS[tool]}" for tool in tools)
    found = escalations(note)
    if found:
        lines.append(f"Manager, please review in this room: {', '.join(found)}.")
    lines.append(f"@{WORKER} post work done with a photo when finished.")
    return "\n".join(lines)
