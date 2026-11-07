"""Tests for the Phase 4 worker checklist, sample data only."""

import io
import os
import re
import tempfile
import unittest
from contextlib import redirect_stdout

from plantops import room
from plantops.work_order import FINAL_OUTCOME
from plantops.worker import UNREADABLE

NOTE = "Soil dry at finger test, leaves drooping, no standing water, Zone B flow low."


class TestWorkerChecklist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "state.json")
        self.run_room("reset")
        self.run_room("triage")

    def run_room(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            room.main(list(args), self.path)
        return out.getvalue()

    def state(self):
        return room.load_state(self.path)

    def test_checklist_blocked_before_approve(self):
        self.assertIn("Approve is required", self.run_room("checklist"))
        self.assertFalse(self.state()["order"]["checklist_posted"])

    def test_checklist_blocked_after_decline(self):
        self.run_room("reply", "Decline")
        self.assertIn("Approve is required", self.run_room("checklist"))
        self.assertIn("Approve and a condition note are required", self.run_room("photo", "--uploaded", "yes", NOTE))

    def test_checklist_after_approve_in_order(self):
        self.run_room("reply", "Approve")
        out = self.run_room("checklist")
        self.assertTrue(out.startswith("@sample-crew assigned: WO-SAMPLE-001, S-02, Lobby planter B"))
        self.assertIn("Checklist: WO-SAMPLE-001, S-02, Lobby planter B, sample ficus.", out)
        self.assertIn("- Area: Lobby planter B, Sample Building 1, Zone B.", out)
        self.assertIn("- Condition on proposal: dry soil, drooping leaves, overdue since Oct 27, 2026, Zone B low flow.", out)
        order = [out.index(f"{n}. [ ] {word}") for n, word in
                 enumerate(["Soil", "Leaves", "Drainage", "Pot and roots", "Irrigation", "Photo"], 1)]
        self.assertEqual(order, sorted(order))
        self.assertTrue(self.state()["order"]["checklist_posted"])

    def test_photo_stored_in_log(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "yes", "--readable", "no", NOTE)
        state = self.state()
        self.assertEqual(state["order"]["condition_note"], NOTE)
        self.assertTrue(state["order"]["photo_uploaded"])
        self.assertFalse(state["order"]["photo_readable"])
        self.assertTrue(any(NOTE in e["note"] and "could not be read" in e["note"] for e in state["log"]))

    def test_photo_fallback_unreadable(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "yes", "--readable", "no", "--seen", "leaves drooping", NOTE)
        out = self.run_room("suggest")
        self.assertIn(UNREADABLE, out)
        self.assertNotIn("In the photo:", out)
        self.assertNotIn("leaves drooping in the photo", out)

    def test_photo_readable_is_referenced(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "yes", "--readable", "yes",
                      "--seen", "leaves drooping, soil surface dry.", NOTE)
        out = self.run_room("suggest")
        self.assertIn("In the photo: leaves drooping, soil surface dry.", out)
        self.assertNotIn(UNREADABLE, out)

    def test_readable_without_upload_falls_back(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "no", "--readable", "yes", "--seen", "made up", NOTE)
        out = self.run_room("suggest")
        self.assertIn(UNREADABLE, out)
        self.assertNotIn("made up", out)

    def test_suggestion_has_next_how_tool_no_diagnosis(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "yes", NOTE)
        out = self.run_room("suggest")
        self.assertIn("Suggestions only, not a diagnosis.", out)
        self.assertIn("Next: It looks like drooping leaves with dry soil, water manually and recheck.", out)
        self.assertIn("How to:\n  1. ", out)
        self.assertIn("\nTools:\n", out)
        self.assertRegex(out, r"\n- watering can: \w.+")
        self.assertIn("Do not change the irrigation schedule", out)
        for banned in ("http", "www.", "buy", "diagnosed", "disease", "deficiency", "pest", "aphid", "mealybug"):
            self.assertNotIn(banned, out.lower().replace("not a diagnosis", ""), banned)
        self.assertNotIn("Manager, please review", out)

    def test_escalation_triggers_posted_to_manager(self):
        self.run_room("reply", "Approve")
        note = "Sticky residue spreading to S-01, leaves yellowing fast, standing water in tray, leak at Zone B valve."
        self.run_room("photo", "--uploaded", "no", note)
        out = self.run_room("suggest")
        self.assertIn("Manager, please review in this room:", out)
        for label in ("sticky residue spreading to more plants", "leaves yellowing fast", "standing water", "irrigation leak"):
            self.assertIn(label, out)
        self.assertIn("Do not water now", out)
        self.assertIn("leaf wipe cloth: ", out)

    def test_negated_phrases_do_not_trigger(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "no", "Soil moist, no standing water, no leak, not sticky.")
        out = self.run_room("suggest")
        self.assertNotIn("Manager, please review", out)
        self.assertNotIn("Do not water now", out)
        self.assertNotIn("leaf wipe cloth", out)

    def test_worse_after_watering_escalates(self):
        self.run_room("reply", "Approve")
        self.run_room("photo", "--uploaded", "no", "Soil moist, plant looks worse after watering.")
        self.assertIn("plant looks worse after watering", self.run_room("suggest"))

    def test_full_worker_flow_to_closed(self):
        self.run_room("reply", "Approve")
        self.run_room("checklist")
        self.run_room("photo", "--uploaded", "yes", "--readable", "no", NOTE)
        self.run_room("suggest")
        self.assertIn("Photo proof noted.", self.run_room(
            "done", "--photo", "Work done, S-02 watered, Zone B checked, soil moist at recheck."))
        out = self.run_room("verify")
        self.assertIn("Final status: Closed", out)
        self.assertIn(f"Logged outcome: {FINAL_OUTCOME}", out)
        order = self.state()["order"]
        self.assertEqual(order["status"], "Closed")
        self.assertTrue(order["done_photo_proof"])
        self.assertFalse(order["schedule_changed"])
        self.assertFalse(order["vendor_dispatched"])
        self.assertFalse(order["payment_made"])

    def test_suggest_needs_condition_note(self):
        self.run_room("reply", "Approve")
        self.assertIn("post the condition note first", self.run_room("suggest"))


class TestNoRealData(unittest.TestCase):
    def test_no_real_names_or_keys_in_repo_files(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pattern = re.compile(r"api[_-]?key|password\s*=|sk-[a-z0-9]{8}", re.I)
        hits = []
        for folder in ("plantops", "tests", "docs"):
            for dirpath, _, files in os.walk(os.path.join(root, folder)):
                for name in files:
                    if name.endswith((".py", ".md")) and name != "test_phase4.py":
                        with open(os.path.join(dirpath, name)) as handle:
                            if pattern.search(handle.read()):
                                hits.append(name)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
