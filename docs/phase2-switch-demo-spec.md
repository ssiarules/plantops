# Phase 2: Switch demo spec, PlantOps Agent

Status: Spec only. Sample data only. No real building data.

## Locked plan this phase follows

At submission, copy only final code, README, demo script, and sample data into a fresh public repo, with one clean initial commit. No build comments and no private notes in the public copy.

The public submission shows manager to PlantOps Agent communication.

## Goal

Run the locked demo in the real private Switch Mattermost room, and record it. One sample site, one work order, one approval, one logged outcome.

Room: plantops-sample-building-1, private.
Sample site: Sample Building 1.
Work order: WO-SAMPLE-001.
Top plant: S-02, Lobby planter B, sample ficus, dry soil, drooping leaves, overdue since Oct 27, 2026, Zone B low flow.

## Room rules, paste exactly into the room setup

1. PlantOps Agent checks the plant register, weather, irrigation status, and past care log before it proposes anything.
2. PlantOps Agent proposes one prioritized work order, with reasons, and asks for approval in chat.
3. No irrigation change, vendor dispatch, or payment happens without a manager Approve in chat.
4. After work is done, the manager verifies in chat, then PlantOps Agent logs the outcome.
5. Sample data only. No real building data in this room.

## Agent prompt, for the Switch room agent

You are PlantOps Agent, a plant operations assistant for Sample Building 1. Use the sample tools in this repo: plant_register, weather, irrigation_status, past_care_log, work_order_log. When the manager tags you and asks you to check Sample Building 1, run triage in this order: register, weather, irrigation, overdue care. Propose one work order, WO-SAMPLE-001, for S-02, with four reasons, and end with the exact approval prompt below. Do nothing that changes irrigation, dispatches a vendor, or spends money until the manager replies Approve in this room. If the manager replies Decline, log Declined and stop. After work done and manager verification, log the outcome and close the work order.

Approval prompt, exact wording:
Approve this work order? Reply Approve or Decline in this room.

## Demo run, in order

Scene 1, problem: Manager posts a short problem note in the room. Example: Lobby planter B looks dry, leaves are drooping.
Scene 2, tag and triage: Manager tags PlantOps Agent and asks it to check Sample Building 1. Agent replies with the triage result and WO-SAMPLE-001, ending with the approval prompt.
Scene 3, approval in chat: Manager replies Approve, in the room, not in a side channel. Agent confirms Manager approved, and lists what will happen next, with no payment and no vendor dispatch in this core demo.
Scene 4, work done and logged outcome: Manager posts work done, then verifies in the room. Agent logs the outcome and closes the work order. Final logged outcome wording: S-02 watered, Zone B low flow checked, recheck in 24 hours, next care 2026-11-10 for S-02 in the sample log.

## Decline path test, required, separate from the main recording

Run the same triage once, then reply Decline instead of Approve. Expected result: work order status Declined, schedule_changed False, vendor_dispatched False, payment_made False, and a Declined entry in the work order log. Do not record the Decline test as if it were the main Approve demo. Report both runs separately.

## Recording checklist

Record the real room, not slides pretending to be a room. Capture, in order: problem note, tag, triage reply with reasons, approval prompt, Approve reply, work done note, verification, logged outcome with Final status Closed.
Keep the recording under the demo length needed for the final video, and keep sample labels visible in the recording.

## Acceptance checks, report pass or fail for each

1. Triage uses all four inputs: register, weather, irrigation, past care log.
2. Proposal is WO-SAMPLE-001 for S-02, with four reasons, and ends with the exact approval prompt.
3. Approve only works on the exact word Approve, in Draft status. Decline only works on the exact word Decline, in Draft status.
   Note, approved Nov 2: "Decline, <reason>" is also accepted. The decision word must lead, exact case, and the text after the comma is a logged reason only. Approve stays the exact word alone. See docs/switch-room-setup.md, Approval reply format.
4. No schedule change, vendor dispatch, or payment happens in the core demo flow.
5. Decline path test passes, as listed above.
6. Final status after Approve, work done, and verification is Closed, with the logged outcome wording above.
7. No real building data, no real names, no keys, and no internal build comments appear in the demo recording or in the files prepared for the public copy.

## Reporting back, plain language, no key values

Files changed, pass or fail for each acceptance check, the Decline test result, blockers, and the recording file location. Do not push to a public repo, do not deploy, and do not submit, until Jhonson gives a separate go for each of those actions.

## Clean public copy checklist, for submission time only, not now

Copy only: README.md, plantops code, tests, docs/demo-script.md, docs/sample-data.md, docs/plantops-demo-spec.md, and this Phase 2 spec, after removing any internal notes. Do not copy: GitHub issues, GitHub comments, build notes, or any file with private names or keys. Verify the fresh public repo by cloning it in a clean folder and running the demo and tests there, before submitting its link.
