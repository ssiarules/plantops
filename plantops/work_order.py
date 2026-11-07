"""Work order and approval gate. No irrigation, vendor, or payment action
happens without a manager Approve message in the room.
"""

STATUSES = [
    "Draft",
    "Manager approved",
    "Work done",
    "Manager verified",
    "Closed",
    "Declined",
]

APPROVAL_PROMPT = "Approve this work order? Reply Approve or Decline in this room."

FINAL_OUTCOME = (
    "S-02 watered, Zone B low flow checked, recheck in 24 hours, "
    "next care 2026-11-10 for S-02 in the sample log."
)

# Sample work order log, one entry per status change. In memory for the
# CLI demo; plantops.room keeps it in a local JSON file between messages.
WORK_ORDER_LOG = []


class WorkOrder:
    """A single demo work order."""

    def __init__(self, order_id, site, plant_id, action, reasons=None):
        self.order_id = order_id
        self.site = site
        self.plant_id = plant_id
        self.action = action
        self.reasons = list(reasons or [])
        self.status = "Draft"
        self.schedule_changed = False
        self.vendor_dispatched = False
        self.payment_made = False
        self.outcome = None
        # Phase 4 worker view, set after Approve only.
        self.checklist_posted = False
        self.condition_note = None
        self.photo_uploaded = False
        self.photo_readable = False
        self.done_photo_proof = False

    def to_dict(self):
        """Return a plain record for logging."""
        return {
            "order_id": self.order_id,
            "site": self.site,
            "plant_id": self.plant_id,
            "action": self.action,
            "reasons": list(self.reasons),
            "status": self.status,
            "schedule_changed": self.schedule_changed,
            "vendor_dispatched": self.vendor_dispatched,
            "payment_made": self.payment_made,
            "outcome": self.outcome,
            "checklist_posted": self.checklist_posted,
            "condition_note": self.condition_note,
            "photo_uploaded": self.photo_uploaded,
            "photo_readable": self.photo_readable,
            "done_photo_proof": self.done_photo_proof,
        }

    @classmethod
    def from_dict(cls, record):
        """Rebuild a work order from a logged record."""
        order = cls(
            record["order_id"],
            record["site"],
            record["plant_id"],
            record["action"],
            record.get("reasons"),
        )
        order.status = record["status"]
        order.schedule_changed = record["schedule_changed"]
        order.vendor_dispatched = record["vendor_dispatched"]
        order.payment_made = record["payment_made"]
        order.outcome = record["outcome"]
        order.checklist_posted = record.get("checklist_posted", False)
        order.condition_note = record.get("condition_note")
        order.photo_uploaded = record.get("photo_uploaded", False)
        order.photo_readable = record.get("photo_readable", False)
        order.done_photo_proof = record.get("done_photo_proof", False)
        return order


def _log(order, note, log=None):
    entry = {"order_id": order.order_id, "status": order.status, "note": note}
    (WORK_ORDER_LOG if log is None else log).append(entry)
    return entry


def work_order_log(log=None):
    """Return a copy of the sample work order log."""
    return [dict(entry) for entry in (WORK_ORDER_LOG if log is None else log)]


def _is_approve(reply):
    return reply.strip() == "Approve"


def _is_decline(reply):
    return reply.strip() == "Decline"


def approve(order, reply, log=None):
    """Move Draft to Manager approved only on the exact word Approve."""
    if order.status != "Draft":
        return False
    if _is_approve(reply):
        order.status = "Manager approved"
        _log(order, "Manager replied Approve in the room.", log)
        return True
    return False


def decline(order, reply, reason=None, log=None):
    """Move Draft to Declined only on the exact word Decline, and stop."""
    if order.status != "Draft":
        return False
    if _is_decline(reply):
        order.status = "Declined"
        order.outcome = reason or "Declined by manager in chat, no action taken."
        _log(order, order.outcome, log)
        return True
    return False


def mark_work_done(order, note=None, log=None, photo_proof=False):
    """Move Manager approved to Work done. No schedule change is made."""
    if order.status != "Manager approved":
        return False
    order.status = "Work done"
    order.done_photo_proof = photo_proof
    note = note or "Manager posted work done."
    if photo_proof:
        note += " Photo proof uploaded in the room."
    _log(order, note, log)
    return True


def record_checklist(order, log=None):
    """Mark the worker checklist posted, only after Manager approved."""
    if order.status != "Manager approved":
        return False
    order.checklist_posted = True
    _log(order, "Worker checklist posted, sample-crew tagged.", log)
    return True


def record_photo(order, note, uploaded, readable, log=None):
    """Store the worker photo step and condition note, after Approve only."""
    if order.status != "Manager approved" or not note.strip():
        return False
    order.condition_note = note.strip()
    order.photo_uploaded = uploaded
    order.photo_readable = uploaded and readable
    if not uploaded:
        photo = "no photo uploaded"
    elif order.photo_readable:
        photo = "photo uploaded and read"
    else:
        photo = "photo uploaded, could not be read"
    _log(order, f"Worker condition note: {order.condition_note} ({photo}).", log)
    return True


def verify(order, log=None):
    """Move Work done to Manager verified, then to Closed, with a log."""
    if order.status != "Work done":
        return False
    order.status = "Manager verified"
    _log(order, "Manager verified the work in the room.", log)
    order.status = "Closed"
    _log(order, "Work order closed.", log)
    return True


def log_outcome(order, outcome, log=None):
    """Log the outcome, only for a Closed or Declined work order."""
    if order.status not in ("Closed", "Declined"):
        return False
    order.outcome = outcome
    _log(order, f"Outcome: {outcome}", log)
    return True
