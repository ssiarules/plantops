# Phase 4: Worker checklist spec, third view, PlantOps Agent

Status: Spec only. Build needs Jhonson's separate go, after the clean core video recording is secured. Do not change the core demo, and do not break the merged Phase 2 code.

Sample data only. No real building data, no real building photos, no real floor plans, no real building names, no real person names, no keys.

## What Phase 4 adds, and what it does not change

PlantOps already has two views: manager approves, and nursery or service provider services clients. Phase 4 adds the third view: the person actually doing the work on site, the worker, in the same Switch room.

Core demo stays unchanged: manager tags PlantOps Agent, agent proposes WO-SAMPLE-001, manager replies Approve, work is done, manager verifies, agent logs outcome, Final status Closed. Decline stays in code and tests only, no video clip.

Phase 4 extends that flow after Approve, before work done, with a worker checklist, a photo step, and a suggestion step. It does not add payment, vendor dispatch, or automatic diagnosis.

## Roles in one room

Room: plantops-sample-building-1, private, Switch built-in chat, local server, no separate Mattermost signup.
- Manager: approves in chat, verifies in chat.
- PlantOps Agent: proposes, generates the checklist, replies with suggestions, logs the outcome.
- Worker, sample crew: receives the checklist, does the checks, uploads a photo, posts a condition note, posts work done with photo proof.
- Sample crew member name for the demo: sample-crew, not a real person. The worker must be a member of the room to be tagged there, otherwise the tag goes nowhere.

## Flow, in order

1. Manager tags PlantOps Agent, agent proposes WO-SAMPLE-001 for S-02, manager replies Approve. This is the core demo, unchanged.
2. Agent posts the work order document link or file, and tags the worker in the room: @sample-crew, with a short assignment note: WO-SAMPLE-001, S-02, Lobby planter B, check Zone B low flow, water manually, recheck soil in 24 hours.
3. Agent posts the worker checklist, for S-02 only, in the room, in checklist form, not as a long paragraph. See checklist format below.
4. Worker goes to Lobby planter B, does the checks in order, takes a photo of S-02, uploads the photo in the room, and posts a short condition note, for example: Soil dry at finger test, leaves drooping, no standing water, Zone B flow low.
5. Agent replies with suggestions based on that condition note and photo, if the photo can be read. See suggestion rules below. The reply includes how to do the next step, step by step, and what tool is needed, with a short tool definition, no brands, no shopping links.
6. Worker does the suggested work, posts work done in the room, with a photo as proof, for example: Work done, S-02 watered, Zone B checked, soil moist at recheck.
7. Manager posts Verified in the room, from the worker photo and note, not from chat text alone.
8. Agent logs the outcome and closes the work order: S-02 watered, Zone B low flow checked, recheck in 24 hours, next care 2026-11-10 for S-02 in the sample log. Final status Closed. schedule_changed False, vendor_dispatched False, payment_made False, in the core demo.

## Worker checklist format, for S-02, sample only

Checklist title: WO-SAMPLE-001, S-02, Lobby planter B, sample ficus.
- Area: Lobby planter B, Sample Building 1, Zone B.
- Condition on proposal: dry soil, drooping leaves, overdue since Oct 27, 2026, Zone B low flow.
- Checks, in order, tick one by one:
  1. Soil: finger test, dry, moist, or wet, and depth.
  2. Leaves: drooping, yellowing, spots, sticky residue, or normal.
  3. Drainage: standing water, damp tray, or dry tray.
  4. Pot and roots: pot size, drainage holes clear or blocked, roots visible or not.
  5. Irrigation: Zone B flow, low, normal, or off, and any leak.
  6. Photo: take one clear photo of the plant and one of the soil surface, upload both in the room, or one photo if only one is possible.
- After the checks, post the condition note in the room, in this form: Soil, leaves, drainage, irrigation, photo uploaded yes or no.

## Photo step, and fallback

- Worker uploads the photo in the Switch room, as a file in the chat, and posts the condition note in the same message thread if possible, otherwise immediately after.
- Agent tries to read the photo, if its tool can read images. If it can, the suggestion reply may refer to what is visible in the photo, in plain words, for example: leaves drooping in the photo, soil surface dry.
- If the agent cannot read the photo, it must say so plainly in the room, and base the suggestion on the worker condition note alone. Do not invent photo details. Do not claim a photo was read when it was not.
- Photo files in the public copy, if any, must be sample photos only, clearly labeled sample, never real building photos.

## Suggestion rules, suggestions, not diagnosis

- Agent suggestions are next checks and next care steps, not a definitive diagnosis. Do not name a pest, disease, or nutrient deficiency for certain from one photo or note.
- Allowed wording: It looks like dry soil, check again in 24 hours. It looks like drooping leaves with dry soil, water manually and recheck. Sticky residue noted, check leaves top and underside, clean gently if needed, and tell the manager if it spreads.
- Escalation triggers, tell the manager in the room if any of these appear: sticky residue spreading to more plants, leaves yellowing fast, standing water, irrigation leak, or a plant that looks worse after watering.
- Every suggestion reply must include: what to do next, how to do it in short steps, and what tool is needed, with a short definition of that tool. Example tools, sample only, no brands: moisture finger test, watering can, drainage tray check, leaf wipe cloth. No shopping links, no brand names.
- How tos open inline in the checklist view, or as short steps in the room reply, not as a separate long document the worker has to hunt for.

## Work order document, Phase 3 link

Phase 4 uses the Phase 3 work order document, if Phase 3 is built, as the file the worker works from. The document must contain: WO-SAMPLE-001, Sample Building 1, S-02, Lobby planter B, condition, action, approved by manager in chat, date, cost cap, sample, none in the core demo, and the checklist from this spec. If Phase 3 is not built yet, the checklist in the room is the work order for Phase 4, and the document is a later addition, not a blocker.

## Room commands, after build go

Extend plantops/room.py, do not rewrite the core gate:
- checklist: post the S-02 checklist for the open approved work order, only after Manager approved, not in Draft.
- photo: accept a worker photo note, in the form: photo uploaded, plus condition note, and store it in the work order log.
- suggest: reply with suggestions, how to steps, and tool, based on the stored condition note, and on the photo if readable, with the suggestion rules above, and with escalation triggers if present.
- done: worker work done, with photo proof noted, only after Manager approved, not before.
- verify: manager verification, only after work done, then log outcome and close, as in Phase 2.
- Keep the exact word Approve and Decline gate unchanged. Keep schedule_changed, vendor_dispatched, and payment_made False in the core demo.

## Acceptance checks, report pass or fail for each

1. Checklist is generated only after Approve, for S-02, Lobby planter B, with area, condition, and checks in order.
2. Worker photo step is stored in the work order log, with condition note, and the agent says plainly if a photo could not be read.
3. Suggestion reply includes next step, how to steps, and tool with a short definition, no brands, no shopping links, and no definitive diagnosis.
4. Escalation triggers, if present in the condition note, are posted to the manager in the room.
5. Work done with photo proof, then manager Verified, then logged outcome, Final status Closed, with the exact outcome wording from Phase 2.
6. No schedule change, vendor dispatch, or payment in the core Phase 4 flow.
7. No real building data, no real building photos, no real names, no keys, no build comments, in code, docs, checklist, or any sample photo used.
8. Core demo still passes, 12 of 12 Phase 2 tests, plus new Phase 4 tests, with no regression in the Approve, Decline, or Closed logic.

## Video, for Phase 4, separate from core video

Core video stays Approve to Closed only, no Decline clip, no Phase 4 clip mixed in. If a Phase 4 video is made, it is a second, clearly labeled video or second scene, after the core video, showing: checklist posted, worker photo uploaded, suggestion reply, work done with photo proof, manager verification, Closed. Do not mix Phase 4 into the core video unless Jhonson gives a separate go for a combined video.

## What not to build in Phase 4

- No automatic pest or disease diagnosis from a photo.
- No payment, no vendor dispatch, no purchase order, in the Phase 4 core.
- No real building tracker code, plant data, photos, or floor plans, copied into PlantOps.
- No public push, no deploy, no submission, until Jhonson gives a separate go for each.

## Report back, plain language, no key values

Files changed, pass or fail for each acceptance check, photo fallback test result, blockers, and whether the core tests still pass. Do not merge yourself, do not push to a public repo, do not deploy, do not submit, until Jhonson gives a separate go for each.
