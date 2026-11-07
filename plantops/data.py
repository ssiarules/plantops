"""Sample data only. No real building data."""

PLANTS = [
    {
        "id": "S-01",
        "location": "Lobby planter A",
        "type": "Sample ficus",
        "condition": "Good, leaves firm",
        "last_care": "2026-10-28",
        "next_care": "2026-11-10",
        "flagged": False,
        "overdue": False,
    },
    {
        "id": "S-02",
        "location": "Lobby planter B",
        "type": "Sample ficus",
        "condition": "Flagged, dry soil, drooping leaves",
        "last_care": "2026-10-20",
        "next_care": "Overdue, was 2026-10-27",
        "flagged": True,
        "overdue": True,
    },
    {
        "id": "S-03",
        "location": "Hallway planter",
        "type": "Sample snake plant",
        "condition": "Good",
        "last_care": "2026-10-30",
        "next_care": "2026-11-13",
        "flagged": False,
        "overdue": False,
    },
    {
        "id": "S-04",
        "location": "Meeting room planter",
        "type": "Sample pothos",
        "condition": "Fair, light yellowing on 2 leaves",
        "last_care": "2026-10-25",
        "next_care": "2026-11-06",
        "flagged": False,
        "overdue": False,
    },
    {
        "id": "S-05",
        "location": "Kitchen planter",
        "type": "Sample peace lily",
        "condition": "Good",
        "last_care": "2026-10-29",
        "next_care": "2026-11-12",
        "flagged": False,
        "overdue": False,
    },
]

WEATHER = [
    {"day": "Day 1", "note": "Hot and dry, high 88, no rain, dry wind."},
    {"day": "Day 2", "note": "Hot and dry, high 90, no rain."},
    {"day": "Day 3", "note": "Cooler, high 78, light rain possible."},
]

IRRIGATION = [
    {
        "zone": "Zone A, Lobby",
        "last_run": "2026-10-30",
        "next_run": "2026-11-03",
        "status": "OK",
    },
    {
        "zone": "Zone B, Lobby planters S-01 and S-02",
        "last_run": "2026-10-26",
        "next_run": "2026-11-03",
        "status": "Flagged, low flow on last run, check before changing schedule.",
    },
    {
        "zone": "Zone C, Hallway and meeting rooms",
        "last_run": "2026-10-30",
        "next_run": "2026-11-04",
        "status": "OK",
    },
]

CARE_LOG = [
    {"date": "2026-10-20", "entry": "S-02 watered, soil dry at check, 1 gallon, outcome good for 3 days."},
    {"date": "2026-10-26", "entry": "Zone B irrigation run, low flow noted, no schedule change made."},
    {"date": "2026-10-28", "entry": "S-01 watered, outcome good."},
    {"date": "2026-10-30", "entry": "Zone A and Zone C runs, outcome OK."},
    {"date": "2026-11-02", "entry": "S-02 check, soil dry again, drooping leaves noted, no action taken yet, awaiting manager decision."},
]


def get_register():
    """Return a copy of the sample plant register."""
    return [dict(plant) for plant in PLANTS]


def get_weather():
    """Return a copy of the sample weather."""
    return [dict(day) for day in WEATHER]


def get_irrigation():
    """Return a copy of the sample irrigation status."""
    return [dict(zone) for zone in IRRIGATION]


def get_care_log():
    """Return a copy of the sample past care log."""
    return [dict(entry) for entry in CARE_LOG]
