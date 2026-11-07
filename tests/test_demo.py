"""Tests for PlantOps demo logic, sample data only."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from plantops import room
from plantops.triage import check_inputs, proposal_message, propose_work_order
from plantops.work_order import (
    APPROVAL_PROMPT,
    FINAL_OUTCOME,
    approve,
    decline,
    log_outcome,
    mark_work_done,
    verify,
)


class TestTriage(unittest.TestCase):
    def test_inputs_all_present(self):
        inputs = check_inputs()
        self.assertIn("register", inputs)
        self.assertIn("weather", inputs)
        self.assertIn("irrigation", inputs)
        self.assertIn("care_log", inputs)

    def test_top_item_is_s02(self):
        order, reasons = propose_work_order()
        self.assertEqual(order.order_id, "WO-SAMPLE-001")
        self.assertEqual(order.plant_id, "S-02")
        self.assertEqual(len(reasons), 4)
        self.assertEqual(order.status, "Draft")

    def test_proposal_ends_with_approval_prompt(self):
        order, reasons = propose_work_order()
        message = proposal_message(order, reasons)
        self.assertTrue(message.endswith("Approve this work order? Reply Approve or Decline in this room."))


class TestApprovalGate(unittest.TestCase):
    def test_approve_moves_to_manager_approved(self):
        order, _ = propose_work_order()
        self.assertTrue(approve(order, "Approve"))
        self.assertEqual(order.status, "Manager approved")
        self.assertFalse(order.schedule_changed)
        self.assertFalse(order.vendor_dispatched)
        self.assertFalse(order.payment_made)

    def test_other_reply_does_not_approve(self):
        order, _ = propose_work_order()
        self.assertFalse(approve(order, "Yes, go ahead"))
        self.assertEqual(order.status, "Draft")

    def test_decline_stops(self):
        order, _ = propose_work_order()
        self.assertTrue(decline(order, "Decline", "Not now"))
        self.assertEqual(order.status, "Declined")
        self.assertFalse(approve(order, "Approve"))

    def test_full_flow_to_closed_and_logged(self):
        order, _ = propose_work_order()
        self.assertTrue(approve(order, "Approve"))
        self.assertTrue(mark_work_done(order))
        self.assertTrue(verify(order))
        self.assertEqual(order.status, "Closed")
        self.assertTrue(log_outcome(order, "S-02 watered, Zone B checked."))
        self.assertIn("S-02", order.outcome)


class TestPhase2Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "state.json")
        self.run_room("reset")

    def run_room(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            room.main(list(args), self.path)
        return out.getvalue()

    def test_reasons_come_from_all_four_inputs(self):
        _, reasons = propose_work_order()
        self.assertTrue(reasons[0].startswith("Register: S-02"))
        self.assertIn("next 2 days", reasons[1])
        self.assertIn("Zone B", reasons[2])
        self.assertIn("low flow", reasons[2])
        self.assertIn("2026-10-20", reasons[3])
        self.assertIn("2026-11-02", reasons[3])

    def test_gate_is_exact_word(self):
        for reply in ("approve", "APPROVE", "Approve it", "Yes"):
            order, _ = propose_work_order()
            self.assertFalse(approve(order, reply), reply)
            self.assertEqual(order.status, "Draft")
        order, _ = propose_work_order()
        self.assertFalse(decline(order, "decline"))
        self.assertEqual(order.status, "Draft")

    def test_gate_only_in_draft(self):
        order, _ = propose_work_order()
        approve(order, "Approve")
        self.assertFalse(decline(order, "Decline"))
        self.assertEqual(order.status, "Manager approved")

    def test_room_approve_path_to_closed(self):
        self.assertIn(APPROVAL_PROMPT, self.run_room("triage"))
        self.assertIn("Approve or Decline", self.run_room("reply", "Looks good"))
        self.assertIn("Manager approved", self.run_room("reply", "Approve"))
        self.run_room("done", "S-02 watered, Zone B checked.")
        out = self.run_room("verify")
        self.assertIn("Final status: Closed", out)
        self.assertIn(FINAL_OUTCOME, out)
        state = room.load_state(self.path)
        order = state["order"]
        self.assertEqual(order["status"], "Closed")
        self.assertFalse(order["schedule_changed"])
        self.assertFalse(order["vendor_dispatched"])
        self.assertFalse(order["payment_made"])
        statuses = [e["status"] for e in state["log"]]
        self.assertEqual(
            statuses,
            ["Draft", "Manager approved", "Work done", "Manager verified", "Closed", "Closed"],
        )

    def test_room_decline_path(self):
        self.run_room("triage")
        out = self.run_room("reply", "Decline, not this week")
        self.assertIn("Declined", out)
        state = room.load_state(self.path)
        order = state["order"]
        self.assertEqual(order["status"], "Declined")
        self.assertFalse(order["schedule_changed"])
        self.assertFalse(order["vendor_dispatched"])
        self.assertFalse(order["payment_made"])
        self.assertIn(
            {"order_id": "WO-SAMPLE-001", "status": "Declined", "note": "not this week"},
            state["log"],
        )
        self.assertIn("Approve is required", self.run_room("done", "watered"))
        self.assertIn("not waiting for approval", self.run_room("reply", "Approve"))


if __name__ == "__main__":
    unittest.main()
