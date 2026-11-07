"""Room tools for the Switch agent, sample data only.

The PlantOps Agent in the Switch room runs one command per manager
message. State is kept in a local JSON file so the work order survives
between messages. No real irrigation, vendor, or payment connection.

Run:
  python3 -m plantops.room triage        tag and triage, print the proposal
  python3 -m plantops.room reply "TEXT"  manager reply, Approve or Decline
  python3 -m plantops.room checklist     after Approve, tag sample-crew, post the checklist
  python3 -m plantops.room photo --uploaded yes|no --readable yes|no [--seen "TEXT"] "NOTE"
                                         worker photo step and condition note
  python3 -m plantops.room suggest       suggestions, how to steps, tools
  python3 -m plantops.room done [--photo] "NOTE"
                                         work done, --photo when photo proof is uploaded
  python3 -m plantops.room verify        manager verifies, close and log outcome
  python3 -m plantops.room status        current work order record
  python3 -m plantops.room log           work order log
  python3 -m plantops.room reset         clear sample state for a new run
"""

import json
import os
import sys

from .triage import proposal_message, propose_work_order
from .work_order import (
    APPROVAL_PROMPT,
    FINAL_OUTCOME,
    WorkOrder,
    approve,
    decline,
    log_outcome,
    mark_work_done,
    record_checklist,
    record_photo,
    verify,
)
from .worker import checklist_message, suggestion_message

STATE_FILE = os.environ.get(
    "PLANTOPS_STATE", os.path.join(os.path.dirname(__file__), "..", ".plantops-state.json")
)


def load_state(path=STATE_FILE):
    if not os.path.exists(path):
        return {"order": None, "log": []}
    with open(path) as handle:
        return json.load(handle)


def save_state(state, path=STATE_FILE):
    with open(path, "w") as handle:
        json.dump(state, handle, indent=2)


def _order(state):
    return WorkOrder.from_dict(state["order"]) if state["order"] else None


def _flags(order):
    return (
        f"schedule_changed {order.schedule_changed}, "
        f"vendor_dispatched {order.vendor_dispatched}, "
        f"payment_made {order.payment_made}"
    )


def cmd_triage(state):
    order, reasons = propose_work_order()
    state["order"] = order.to_dict()
    state["log"].append({"order_id": order.order_id, "status": "Draft", "note": "Proposed after triage."})
    return proposal_message(order, reasons)


def cmd_reply(state, text):
    order = _order(state)
    if order is None:
        return "No open work order. Tag me to check Sample Building 1 first."
    if order.status != "Draft":
        return f"{order.order_id} is {order.status}, not waiting for approval."
    reason = None
    # "Decline, not this week" keeps the reason; the decision word must lead.
    head, _, rest = text.strip().partition(",")
    if head.strip() == "Decline" and rest.strip():
        text, reason = "Decline", rest.strip()
    if approve(order, text, state["log"]):
        state["order"] = order.to_dict()
        return (
            f"{order.order_id} status: Manager approved.\n"
            "Next: check Zone B low flow, water S-02 manually, recheck soil in 24 hours.\n"
            "No payment and no vendor dispatch in this demo. Post work done when finished.\n"
            f"{_flags(order)}"
        )
    if decline(order, text, reason, state["log"]):
        state["order"] = order.to_dict()
        return (
            f"{order.order_id} status: Declined. Logged: {order.outcome}\n"
            "Stopping here. No work, no irrigation change.\n"
            f"{_flags(order)}"
        )
    return f"I need the exact word Approve or Decline to proceed. {APPROVAL_PROMPT}"


def cmd_checklist(state):
    order = _order(state)
    if order is None or not record_checklist(order, state["log"]):
        status = order.status if order else "none"
        return f"Checklist not posted, work order status is {status}. Manager Approve is required first."
    state["order"] = order.to_dict()
    return checklist_message(order)


def cmd_photo(state, args):
    """photo --uploaded yes|no --readable yes|no [--seen "TEXT"] NOTE"""
    opts = {"--uploaded": "no", "--readable": "no", "--seen": None}
    words = []
    args = list(args)
    while args:
        word = args.pop(0)
        if word in opts and args:
            opts[word] = args.pop(0)
        else:
            words.append(word)
    order = _order(state)
    uploaded = opts["--uploaded"] == "yes"
    readable = opts["--readable"] == "yes"
    if order is None or not record_photo(order, " ".join(words), uploaded, readable, state["log"]):
        status = order.status if order else "none"
        return f"Condition note not stored, work order status is {status}. Approve and a condition note are required."
    state["order"] = order.to_dict()
    state["photo_seen"] = opts["--seen"] if order.photo_readable else None
    return f"{order.order_id} condition note stored in the work order log."


def cmd_suggest(state):
    order = _order(state)
    if order is None or order.status != "Manager approved" or not order.condition_note:
        return "No condition note stored yet. Worker, post the condition note first."
    message = suggestion_message(
        order, order.condition_note, order.photo_readable, state.get("photo_seen")
    )
    state["log"].append({"order_id": order.order_id, "status": order.status, "note": "Suggestions posted."})
    return message


def cmd_done(state, args):
    args = list(args)
    photo_proof = "--photo" in args
    note = " ".join(a for a in args if a != "--photo") or None
    order = _order(state)
    if order is None or not mark_work_done(order, note, state["log"], photo_proof):
        status = order.status if order else "none"
        return f"Work done not accepted, work order status is {status}. Approve is required first."
    state["order"] = order.to_dict()
    proof = "Photo proof noted. " if photo_proof else ""
    return f"{order.order_id} status: Work done. {proof}Please verify in this room."


def cmd_verify(state):
    order = _order(state)
    if order is None or not verify(order, state["log"]):
        status = order.status if order else "none"
        return f"Verification not accepted, work order status is {status}."
    log_outcome(order, FINAL_OUTCOME, state["log"])
    state["order"] = order.to_dict()
    return (
        f"{order.order_id} Manager verified.\n"
        f"Logged outcome: {order.outcome}\n"
        f"Final status: {order.status}\n"
        f"{_flags(order)}"
    )


def main(argv=None, path=STATE_FILE):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__)
        return 2
    command, args = argv[0], argv[1:]
    if command == "reset":
        save_state({"order": None, "log": []}, path)
        print("Sample state cleared.")
        return 0
    state = load_state(path)
    if command == "triage":
        out = cmd_triage(state)
    elif command == "reply":
        out = cmd_reply(state, " ".join(args))
    elif command == "checklist":
        out = cmd_checklist(state)
    elif command == "photo":
        out = cmd_photo(state, args)
    elif command == "suggest":
        out = cmd_suggest(state)
    elif command == "done":
        out = cmd_done(state, args)
    elif command == "verify":
        out = cmd_verify(state)
    elif command == "status":
        out = json.dumps(state["order"], indent=2)
    elif command == "log":
        out = "\n".join(f"{e['order_id']} | {e['status']} | {e['note']}" for e in state["log"])
    else:
        print(__doc__)
        return 2
    save_state(state, path)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
